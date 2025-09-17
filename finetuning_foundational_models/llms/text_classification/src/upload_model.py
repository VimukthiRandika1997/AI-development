import torch

from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel
from datetime import datetime
from loguru import logger

from config import settings

# Reload tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(settings.BASE_MODEL)

base_model_reload = AutoModelForCausalLM.from_pretrained(
        settings.BASE_MODEL,
        return_dict=True,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
)

fine_tuned_model = f"{settings.BASE_MODEL}_output"

# Merge adapter with base model
model = PeftModel.from_pretrained(base_model_reload, fine_tuned_model)
model = model.merge_and_unload()

# Save the full model and tokenizer locally
now = datetime.now()
unique_id = now.strftime('%Y%m%d%H%M%S%f')
model_dir = f"{settings.BASE_MODEL}_{unique_id}"
model.save_pretrained(model_dir)
tokenizer.save_pretrained(model_dir)


# Push to the HF hub
try:
    try:
        # Login to HF account
        login(token = settings.HF_TOKEN)
    except Exception as e:
        logger.error(f"Error is occured during login to your HF Account: {str(e)}")

    model.push_to_hub(model_dir, use_temp_dir=False)
    tokenizer.push_to_hub(model_dir, use_temp_dir=False)
    logger.info("Model is successfully uploaded to HF")

except Exception as e:
    logger.error(f"Error is occured during model uploading: {str(e)}")