# -- huggingface libs
import huggingface_hub
from diffusers import (
    ControlNetModel,
    StableDiffusionXLControlNetPipeline,
    DDPMScheduler,
    AutoencoderKL
)
from diffusers import DDIMScheduler, DPMSolverMultistepScheduler
from diffusers.utils import load_image
from safetensors.torch import load_file
from huggingface_hub import hf_hub_download

# -- other supportive libs
import torch
import torch.nn.functional as F
import cv2
import numpy as np
import os
import gc
import random
import time
import logging
import asyncio
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

from api.core.config import Config

logger = logging.getLogger(__name__)


# - Helper functions
def make_inpaint_condition(init_image, mask_image):
    """Make the out-painting condition for the model inference"""

    init_image = np.array(init_image.convert("RGB")).astype(np.float32) / 255.0
    mask_image = np.array(mask_image.convert("L")).astype(np.float32) / 255.0
    assert init_image.shape[0:1] == mask_image.shape[0:1], "image and image_mask must have the same image size"
    init_image[mask_image > 0.5] = -1.0  # set as masked pixel
    init_image = np.expand_dims(init_image, 0).transpose(0, 3, 1, 2)
    init_image = torch.from_numpy(init_image)

    return init_image
    

def paste_fg_over_image(gen_image: Image.Image, orig_image: Image.Image, fg_mask: Image.Image)->Image.Image:
    """Add foreground object seamlessly to the generated image"""

    fg_mask = fg_mask.convert("L")
    fg_mask = fg_mask.resize(gen_image.size, Image.NEAREST)
    orig_image = orig_image.resize(gen_image.size)
    gen_image = gen_image.convert("RGBA")
    orig_image = orig_image.convert("RGBA")
    gen_image.paste(orig_image, (0, 0), fg_mask)
    return gen_image.convert("RGB")


def sharpen_latents(latents, strength=0.5, alpha=0.7):
    """
    Enhances details in diffusion model latents using latent-space sharpening
    
    Args:
        latents: Input latent tensor (shape: [batch, channels, height, width])
        strength: Sharpening intensity (0.0-1.0)
        alpha: Original vs sharpened mix ratio (0.0 = all original, 1.0 = all sharpened)
    
    Returns:
        Modified latent tensor with enhanced details
    """
    # Ensure values stay reasonable for diffusion model
    min_val, max_val = -10.0, 10.0  # Typical latent value range for SDXL model
    
    # Create sharpening kernel adapted for latent space
    sharpen_kernel = torch.tensor([
        [0.0, -0.5, 0.0],
        [-0.5, 3.0, -0.5],
        [0.0, -0.5, 0.0]
    ], dtype=latents.dtype, device=latents.device) * strength

    # Normalize kernel to maintain latent distribution
    kernel = sharpen_kernel / sharpen_kernel.abs().sum()
    
    # Reshape kernel for depthwise convolution
    kernel = kernel.repeat(latents.shape[1], 1, 1, 1)  # [channels, 1, 3, 3]
    
    # Apply depthwise convolution to all latent channels
    sharpened = F.conv2d(
        latents,
        kernel,
        padding=1,
        groups=latents.shape[1]  # Process each channel separately
    )
    
    # Mix original and sharpened latents
    modified_latents = alpha * sharpened + (1 - alpha) * latents
    
    # Maintain stable latent value range
    return modified_latents.clamp(min_val, max_val)


def soft_clamp_tensor(input_tensor, threshold=3.5, boundary=4):
    """Shrinking towards the mean (will also remove outliers)"""

    if max(abs(input_tensor.max()), abs(input_tensor.min())) < 4:
        return input_tensor
    channel_dim = 1

    max_vals = input_tensor.max(channel_dim, keepdim=True)[0]
    max_replace = ((input_tensor - threshold) / (max_vals - threshold)) * (boundary - threshold) + threshold
    over_mask = (input_tensor > threshold)

    min_vals = input_tensor.min(channel_dim, keepdim=True)[0]
    min_replace = ((input_tensor + threshold) / (min_vals + threshold)) * (-boundary + threshold) - threshold
    under_mask = (input_tensor < -threshold)

    return torch.where(over_mask, max_replace, torch.where(under_mask, min_replace, input_tensor))


def center_tensor(input_tensor, channel_shift=1, full_shift=1, channels=[0, 1, 2, 3]):
    """Center tensor (balance colors)"""

    for channel in channels:
        input_tensor[0, channel] -= input_tensor[0, channel].mean() * channel_shift
    return input_tensor - input_tensor.mean() * full_shift


def maximize_tensor(input_tensor, boundary=4, channels=[0, 1, 2]):
    """Maximize/normalize tensor"""

    min_val = input_tensor.min()
    max_val = input_tensor.max()

    normalization_factor = boundary / max(abs(min_val), abs(max_val))
    input_tensor[0, channels] *= normalization_factor

    return input_tensor


def callback(pipe, step_index, timestep, cbk):
    """Callback for the image generation pipeline to change the intermediate results on the fly"""

    if timestep > 950:
        threshold = max(cbk["latents"].max(), abs(cbk["latents"].min())) * 0.998
        cbk["latents"] = soft_clamp_tensor(cbk["latents"], threshold*0.998, threshold)
    # if timestep > 700:
    #     cbk["latents"] = center_tensor(cbk["latents"], 0.8, 0.8)
    if timestep > 1 and timestep < 100:
        # cbk["latents"] = center_tensor(cbk["latents"], 0.6, 1.0)
        cbk["latents"] = maximize_tensor(cbk["latents"])
        cbk["latents"] = sharpen_latents(cbk["latents"], alpha=0.1)
    return cbk


def flush():
    """Free up the GPU memory"""
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.reset_max_memory_allocated()
    torch.cuda.reset_peak_memory_stats()


# - Main classes
class ModelManager:
    """Thread-safe model manager for model inference."""
    
    _instance = None
    _initialized = False
    # Singleton pattern 
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance
    
    
    def __init__(self):
        if not self._initialized:
            self.session = None
            self.input_name = None
            self.output_name = None
            self.model_loaded = False
            self.load_time = None
            self.executor = ThreadPoolExecutor(max_workers=Config.MAX_WORKERS)
            self._initialized = True
    
    
    def load_pipeline(self):
        """Load pipeline with optimization."""
        try:
            start_time = time.time()

            # huggingface login
            huggingface_hub.login(Config.HF_TOKEN) #! Need to change this!
            
            # Check if model file exists
            # if not os.path.exists(Config.MODEL_PATH):
            #     raise FileNotFoundError(f"Model file not found: {Config.MODEL_PATH}")
            
            
            # Load the model #! Need to change how the models are loaded, instead of hf account base approach
            controlnet_canny = ControlNetModel.from_pretrained(
                                    "Vimax97/sdxl-canny-edge_v3",
                                    subfolder="checkpoint-2000/controlnet",
                                    weight_name="diffusion_pytorch_model.safetensors",
                                    torch_dtype=torch.float16,
                                )
            vae = AutoencoderKL.from_pretrained('madebyollin/sdxl-vae-fp16-fix', torch_dtype=torch.float16)                                

            controlnet_inpaint = ControlNetModel.from_pretrained(
                                    "Vimax97/sdxl-controlnet-bg-inpaint-v1",
                                    use_safetensors=True,
                                    torch_dtype=torch.float16
                                )
            # -- load the SDXL model along with controlnet models
            pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
                                    "SG161222/RealVisXL_V4.0",
                                    vae=vae,
                                    controlnet=[controlnet_inpaint, controlnet_canny], 
                                    torch_dtype=torch.float16
                                )                                
            # -- load the ip-adapter model
            pipe.load_ip_adapter(
                "Vimax97/ip-adapter-plus_sdxl_test",
                subfolder="sdxl_models",
                weight_name="ip-adapter-plus_sdxl_vit-h.safetensors",
                image_encoder_folder="sdxl_models/image_encoder",
            )                 
            # pipe.enable_model_cpu_offload() # comment this, when you have enough VRAM

            # -- load the LoRA weights
            resadapter_model_name = "resadapter_v2_sdxl"
            pipe.load_lora_weights(
                hf_hub_download(repo_id="jiaxiangc/res-adapter", subfolder=resadapter_model_name, filename="pytorch_lora_weights.safetensors"), 
                adapter_name="res_adapter",
                ) # load lora weights
            pipe.set_adapters(["res_adapter"], adapter_weights=[1.0])
            pipe.unet.load_state_dict(
                load_file(hf_hub_download(repo_id="jiaxiangc/res-adapter", subfolder=resadapter_model_name, filename="diffusion_pytorch_model.safetensors")),
                strict=False,
                ) # load norm weights

            pipe.load_lora_weights("Vimax97/sdxl-bg_v2", weight_name="pytorch_lora_weights.safetensors", adapter_name="bg_v2", adapter_weights=5.0)

            # -- switch to DDPM Karras scheduler
            pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
            pipe.scheduler.use_karras_sigmas = True  # Enable Karras noise schedule
            pipe.scheduler.config.noise_offset = 0.05  # Adjust as needed
            pipe.set_ip_adapter_scale(1.0) # only image-prompt is considered
        
            self.pipe = pipe
            
            self.load_time = time.time() - start_time
            self.model_loaded = True
            
            logger.info(f"The pipeline is loaded successfully in {self.load_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to load the pipeline: {e}")
            self.model_loaded = False
            raise

    
    def _generate_image(self, prompt, image, mask, ip_image, steps=25, width=1024, height=1024):
        # generate a seed
        seed = random.randint(0, 100_000_000)
        generator = torch.Generator(device="cuda").manual_seed(seed)

        mask_org = mask.copy()

        # get image, mask for ip-adapter
        # IP-Adapter reference image (style/identity source)
        ip_image = ip_image.convert("RGB")
        ip_image = ip_image.resize((224, 224))  # IP-Adapter expects 224x224

        # get canny-edge
        image_np = np.array(mask_org)
        canny_edges = cv2.Canny(image_np, 100, 200)
        canny_edges = cv2.cvtColor(canny_edges, cv2.COLOR_GRAY2RGB)
        control_canny_image = Image.fromarray(canny_edges)
        
        # get inpainting mask
        mask_arr = Image.fromarray(255 - np.array(mask))
        control_inpaint_image = make_inpaint_condition(image, mask_arr)

        generated_image = self.pipe(
            prompt,
            negative_prompt="text, low quality, bad quality, sketches, bleeding to mask area, yellow tint, yellow cast, warm tones, leaking colors, no ground contact, levitating, unrealistic placement, Logo,Watermark,Text,Ugly,Morbid,Extra fingers,Poorly drawn hands,Mutation,Blurry,Extra limbs,Gross proportions,Missing arms,Mutated hands,Long neck,Duplicate,Mutilated,Mutilated hands,Poorly drawn face,Deformed,Bad anatomy,Cloned face,Malformed limbs,Missing legs,Too many fingers",
            image=[control_inpaint_image, control_canny_image],
            ip_adapter_image=ip_image,  # Reference image for IP-Adapter
            strength=0.1,               # How much to modify the input (0-1) # default value is set to 0.7
            ip_adapter_strength=0.1,    # How strongly to apply IP-Adapter (0-1) # default value is set to 0.8
            num_inference_steps=steps,
            guidance_scale=12,
            width=width,
            height=height,
            controlnet_conditioning_scale=[1.0, 1.0], # default value is set to [0.8, 0.8]
            generator=generator,
            callback_on_step_end=callback,
            callback_on_step_end_inputs=["latents"],
        ).images[0]
        flush()
        
        pasted_img = paste_fg_over_image(generated_image, image, mask_org)
        
        return pasted_img
    

    async def generate_async(self, prompt: str, product_image: Image.Image, mask_image: Image.Image, ip_image: Image.Image, width=1536, height=836) -> Dict[str, Any]:
        """Async prediction with thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._generate_sync, prompt, product_image, mask_image, ip_image, width, height)
    

    def _generate_sync(self, prompt: str, product_image: Image.Image, mask_image: Image.Image, ip_image: Image.Image, width: int, height: int) -> Dict[str, Any]:
        """Synchronous image generation."""
        if not self.model_loaded:
            raise RuntimeError("The pipeline is not loaded")
        
        start_time = time.time()
        
        try:
            
            # Run inference: generate an image
            generated_image = self._generate_image(prompt=prompt, image=product_image, mask=mask_image, ip_image=ip_image, steps=35, width=width, height=height) # steps is set 35 as default 

            # parsing
            
            processing_time = (time.time() - start_time) * 1000
            
            return {
                'generated_image': generated_image,
                'is_safe': 'no_implemented_yet',     #! Check the generated image's status
                'processing_time_ms': processing_time
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise