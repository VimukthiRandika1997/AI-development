# Hyper-parameter Tuning with XGBoost 3.0 and Optuna: CPU based vs GPU

- Tuning hyper-parameters can take a lot of time, this needs to be optimized
- Models like `xgboost` has lot of hyper-parameters which eventually make a lot of combinations and thus tuning process becomes so slow!

## Hyper-parameter Tunning

- Allows us to find the best set of parameters for the training task which could improve the accuracy for the given dataset
- Typically `xgboost` contains lots of parameters to be set during, hence the combination of those paramters matters.

## Guidelines for Hyper-paramter Tuning

1. Create a proper validation dataset first
2. Tuning parameters:
    - Get a baseline model by tuning once
    - Start the tuning phase by considering the combination of hyper-paramters and features ( feature engineering)


## How to run

1. Download the dataset from the [kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and put the `.csv` file in the `data` folder

    ```bash
    mkdir data
    # download the dataset and put it in here
    ```

2. Run the scripts: CPU vs GPU

    ```bash
    cd src/
    # CPU based tuning
    bash param_search_cpu.py

    # GPU based tuning
    bash param_search_gpu.py
    ```

## References:

- [Kaggle](https://www.kaggle.com/code/vimukthi1997/fast-tuning-with-xgboost-3-0-optuna-gpus/notebook)