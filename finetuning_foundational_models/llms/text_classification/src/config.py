import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    # Weight & Biases settings
    WB_TOKEN = os.getenv("WANDB_TOKEN")

    # Huggingface settings
    HF_TOKEN = os.getenv("HF_TOKEN")

    # Dataset settings
    BASE_DATASET_DIR_PATH="../data"
    DATASET_NAME = "email_spam.csv"
    DATASET_PATH = os.path.join(BASE_DATASET_DIR_PATH, DATASET_NAME)

    # Model settings
    BASE_MODEL = "microsoft/Phi-3.5-mini-instruct"


settings = Settings()