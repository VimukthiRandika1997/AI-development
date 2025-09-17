import wandb
import bitsandbytes as bnb
import torch.nn as nn
from peft import LoraConfig, PeftConfig
from trl import SFTTrainer
from transformers import (AutoModelForCausalLM, 
                          AutoTokenizer, 
                          BitsAndBytesConfig, 
                          TrainingArguments, 
                          logging)
from config import settings
from dataset import preprocess_datasets


# - Helper functions
def find_all_linear_names(model):
    """
    Extract linear modules from the model.
    These are used to create the LoRA layers to be finetuned during the training.
    """

    cls = bnb.nn.Linear4bit
    lora_module_names = set()

    for name, module in model.named_modules():
        if isinstance(module, cls):
            names = name.split('.')
            lora_module_names.add(names[0] if len(names) == 1 else names[-1])
    if 'lm_head' in lora_module_names:  # needed for 16 bit
        lora_module_names.remove('lm_head')

    return list(lora_module_names) # ['gate_up_proj', 'down_proj', 'qkv_proj', 'o_proj']


# Login to your account
wb_token = settings.WB_TOKEN
wandb.login(key=wb_token)

# Create a runner
runner = wandb.init(
    project=f"Fine-tune {settings.BASE_MODEL} on Email Spam Text Classification",
    job_type="training_phase",
    anonymous="allow" # allow other to watch the logs in the UI
)


def start_training():

    # Load the pretrained model, tokenizer for the training
    # - 4-bit quantized version is used here
    base_model =  settings.BASE_MODEL
    tokenizer = AutoTokenizer.from_pretrained(base_model)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=False,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="float16",
    )

    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        device_map="auto",
        torch_dtype="float16",
        quantization_config=bnb_config, 
    )


    model.config.use_cache = False
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token_id = tokenizer.eos_token_id


    modules = find_all_linear_names(model)

    # Setting the hyper-parameters
    output_dir = f"{settings.BASE_MODEL}_output"

    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0,
        r=64,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=modules,
    )

    training_arguments = TrainingArguments(
        output_dir=output_dir,                    # directory to save and repository id
        num_train_epochs=1,                       # number of training epochs
        per_device_train_batch_size=1,            # batch size per device during training
        gradient_accumulation_steps=4,            # number of steps before performing a backward/update pass
        gradient_checkpointing=True,              # use gradient checkpointing to save memory
        optim="paged_adamw_8bit",
        logging_steps=1,                         
        learning_rate=2e-5,                       # learning rate, based on QLoRA paper, a slow-training rate
        weight_decay=0.001,
        fp16=False,
        bf16=False,
        max_grad_norm=0.3,                        # max gradient norm based on QLoRA paper
        max_steps=-1,
        warmup_ratio=0.03,                        # warmup ratio based on QLoRA paper
        group_by_length=False,
        lr_scheduler_type="cosine",               # use cosine learning rate scheduler
        report_to="wandb",                        # report metrics to w&b
        eval_strategy="steps",                    # save checkpoint every epoch
        eval_steps = 0.2
    )


    # Get the training datasets
    train_data, eval_data, _ = preprocess_datasets()

    trainer = SFTTrainer(
        model=model,
        args=training_arguments,
        train_dataset=train_data,
        eval_dataset=eval_data,
        peft_config=peft_config,
        dataset_text_field="text",
        tokenizer=tokenizer,
        max_seq_length=512,
        packing=False,
        dataset_kwargs={
        "add_special_tokens": False,
        "append_concat_token": False,
        }
    )

    # Finetune the model
    trainer.train()

    # Generate evaluation report after the training is finished
    wandb.finish()
    model.config.use_cache = True

    # Save trained model and tokenizer
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)


if __name__ == "__main__":
    start_training()