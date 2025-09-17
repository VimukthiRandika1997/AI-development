"""
Functionalities for Dataset related operations
"""

import numpy as np
import pandas as pd
from datasets import Dataset
from config import settings


def generate_prompt(data_point):
    """
    Generate a prompt, instructions, text descriptions, and labels.
    """

    return f"""
            Classify the Email text into spam or not_spam.
text: {data_point["text"]}
label: {data_point["type"]}""".strip()


def generate_test_prompt(data_point):
    """
    Generate a test prompt, instructions, text descriptions without labels.
    """

    return f"""
            Classify the Email text into spam or not_spam.
text: {data_point["text"]}
label: """.strip()


def preprocess_datasets():

    """
    Preprocess the data before training:
        - Create system-intructions
        - Create text-description
        - Create labels
    """

    # Read the dataset as a Dataframe
    df =  pd.read_csv(settings.DATASET_PATH)
    df.columns = ["type", "text"]
    df.loc[:, "type"] = df.loc[:, "type"].str.replace("not spam","not_spam")

    # Shuffle the Dataframe and select only 10_000 rows
    # - frac=1 means all raws should be included in the shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Split the Dataframe to train and test sets
    train_size = 0.8
    eval_size = 1 - 0.8

    train_end = int(train_size * len(df))
    eval_end = train_end + int(eval_size * len(df))

    X_train = df[:train_end]
    X_eval = df[train_end:eval_end]
    X_test = df[eval_end:]


    # Convert the Dataframe to Huggingface Dataset format
    # - contains system instructions, a text description and a label (category)
    train_data = Dataset.from_pandas(X_train[["text"]])
    eval_data = Dataset.from_pandas(X_eval[["text"]])

    return train_data, eval_data, X_test