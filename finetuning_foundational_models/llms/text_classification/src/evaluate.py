from peft import PeftModel
from transformers import (AutoModelForCausalLM, 
                          AutoTokenizer, 
                          BitsAndBytesConfig, 
                          pipeline)
from tqdm import tqdm

from config import settings
from dataset import preprocess_datasets
from metrics import evaluate
from loguru import logger


# - Helper functions
def load_model():
    """
    Load the base model
    """

    base_model_name =  settings.BASE_MODEL

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=False,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="float16",
    )

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        device_map="auto",
        torch_dtype="float16",
        quantization_config=bnb_config, 
    )

    model.config.use_cache = False
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    tokenizer.pad_token_id = tokenizer.eos_token_id

    return model, tokenizer


def predict(test, model, tokenizer):
    """
    Predict the category of the text
    """

    y_pred = []
    categories = ["spam", "not_spam"]
    
    for i in tqdm(range(len(test))):
        prompt = test.iloc[i]["text"]
        pipe = pipeline(task="text-generation", 
                        model=model, 
                        tokenizer=tokenizer, 
                        max_new_tokens=4, 
                        temperature=0.1)
        
        result = pipe(prompt)
        answer = result[0]['generated_text'].split("label:")[-1].strip()
        
        # Determine the predicted category
        for category in categories:
            if category.lower() in answer.lower():
                y_pred.append(category)
                break
        else:
            y_pred.append("none")
    
    return y_pred


def evaluate_on_pretrained_model(y_true):
    """
    Evaluate the model performance using pretrained model weights
    """

    model, tokenizer = load_model()

    # Make the predictions
    y_pred = predict(X_test, model, tokenizer)

    # evaluate the results
    evaluate(y_true, y_pred)


def evaluate_on_finetuned_model(y_true):
    """
    Evaluate the model performance using finetuned model weights
    """

    # load the base model
    model, tokenizer = load_model()
    fine_tuned_model = f"{settings.BASE_MODEL}_output"

    # merge the adapter with base the model
    model = PeftModel.from_pretrained(model, fine_tuned_model)
    model = model.merge_and_unload()

    # Make the predictions
    y_pred = predict(X_test, model, tokenizer)

    # evaluate the results
    evaluate(y_true, y_pred)


# - Main execution
_, _, X_test = preprocess_datasets()
y_true = X_test.loc[:,'label']

logger.info("Evaluating model performance using pre-trained model...")
evaluate_on_pretrained_model(y_true=y_true)


logger.info("Evaluating model performance using finetuned model...")
evaluate_on_finetuned_model(y_true=y_true)