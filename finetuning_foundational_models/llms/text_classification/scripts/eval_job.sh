#!/bin/bash

pushd ../
    echo "Activating the env..."
    source env/bin/activate
popd

pushd ../src
    echo "Started evaluating the model performance..."
    python3 evaluate.py
    echo "Model evaluation process is finished..."
popd