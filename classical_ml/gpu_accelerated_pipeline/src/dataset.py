"""
Dataset Information

- Credict card fraud detection dataset
- 280K transactions with features
- Binary classification (Fraud / No fraud)
- Highly imsbalanced (only 492 fraud instances)
- Features are V1-V28: dimensionally  reduced features ( we don't what they are)

"""

# - Imports
import os
import pandas as pd


def load_dataset():
    # Load the dataset
    dataset_path = "../data/creditcard.csv"
    assert os.path.exists(dataset_path), "CSV file doesn't exist"
    df = pd.read_csv(dataset_path)

    # Extract the features
    X = df[[c for c in df.columns if c.startswith("V")] + ["Amount"]]
    y = df["Class"]

    return X, y