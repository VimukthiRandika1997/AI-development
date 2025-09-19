# AI Background Generation

<div align="center">
    <picture>
        <img alt="Building AI Applications" height="600px" src="https://github.com/VimukthiRandika1997/AI-background-generation/raw/main/assets/sample_image.png">
    </picture> 
</div>

- Generate backgrounds (outpainting task) given  foreground product objects of interest.
- This is useful feature in e-commerce platform for generating product packshots:
    - Preserve the original product's details
    - Instant background images tailored to different themes 

## 🛠️ Technical Details

- Following models were fine-tuned for this task using a custom datasets:

    - **SDXL base model**: *for adapting the model for background generation (LoRA training)*
    - **IP Adapter model**: *for mapping image-to-image translation task*
    - **Cusom Controlnets**: *for handling spatial conditions*

- There were two datasets created from scratch for this image generation training pipeline:

    1. **Background dataset**: contains the following things
        - a background image 
        - a corresponding text prompt which describes the background image

        ![background dataset](/finetuning_foundational_models/computer_vision/ai_background_generator/assets/ai_background_generator_background_dataset.png)

    2. **Product dataset**: contains the following things
    
        - a product image
        - a product mask 
        - a corresponding text prompt which describes the environment where the product lies

        ![product dataset](/finetuning_foundational_models/computer_vision/ai_background_generator/assets/ai_background_generator_product_dataset.png)


        - For the creation of this training dataset, I have fine-tuned Vision Language Models (VLMs) called `Florence-2` and `Llama 3.2-vision` to generate text-prompts that follows a specific prompt-structure.

            - Given a product-image, the models should create an accurate description about the sorrounding environment of the product without describing the product.
            - The prompt should follow the below criterions:
                - **Surface where object is located**
                - **Surrounding objects**
                - **Background**
                - **Lighting**
                - **Overall mood**
            - In this way, we can refer to any product item without specifying the category of it during the inference time
            - `Florence-2` has more flexibility to target specif product item within an image as it was pre-trained on the object-detection task whereas `Llama 3.2-vision` doesn't have that kind of an in-built capability to target certain objects within an image by default.
            <div align="center">
                <picture>
                    <img alt="Building AI Applications" height="600px" src="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fdrive.google.com/uc?id=1QZQIIypvTie4L7cngEewFS8qDo9LYI6o">
                </picture> 
                <p><i>Generated prompt: Professional photo of an object on a stone podium which is on a marble table, a wall in the background, a palm leaf in the corner, a harsh shadow from the left side, a concrete wall in the background, minimalist mood</i></p>
            </div>

            <div align="center">
                <picture>
                    <img alt="Building AI Applications" height="600px" src="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fdrive.google.com/uc?id=1kKZDUmaSyaQnsvjf5hzKR694DaiVNOtm">
                </picture> 
                <p><i>Generated prompt: Professional photo of an object on a marble podium which is on a jungle clearing, surrounded by palm trees and lush greenery, a misty mountain range in the background, a cloudy sky</i></p>
            </div>

- API Design: 
    - A modular FastAPI for generating background images: [more details](/ai-background-generation/README.md)

