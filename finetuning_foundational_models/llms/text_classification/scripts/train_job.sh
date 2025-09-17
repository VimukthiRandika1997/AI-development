#!/bin/bash

pushd ../
    echo "Activating the env..."
    source env/bin/activate
popd

pushd ../src
    echo "Start fine-tuning the model..."
    python3 train.py
    echo "Fine-tuning process is finished..."

    echo "Uploading the model to HF hub..."
    python3 upload_model.py
    echo "Uploading process is finished..."
popd