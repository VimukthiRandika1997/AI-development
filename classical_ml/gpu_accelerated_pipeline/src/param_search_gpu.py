"""
Hyper-paramter search using GPU loaded model
"""

# - Imports
import os
import xgboost as xgb
import pandas as pd
import numpy as np
import sklearn
import optuna

from sklearn.model_selection import cross_val_score
from dataset import load_dataset
from loguru import logger

logger.info("XGBoost Version", xgb.__version__)
logger.info("Pandas Version", pd.__version__)
logger.info("Numpy Version", np.__version__)
logger.info("SKlearn Version", sklearn.__version__)
logger.info("Optuna Version", optuna.__version__)


# Load the model
# - refer the kaggle notebook for the hyper-parameter usages: https://www.kaggle.com/code/vimukthi1997/fast-tuning-with-xgboost-3-0-optuna-gpus/notebook
reg = xgb.XGBClassifier(
    base_score=None,
    booster=None,
    callbacks=None,
    colsample_bylevel=None,
    colsample_bynode=None,
    colsample_bytree=None,
    device=None,
    early_stopping_rounds=None,
    enable_categorical=False,
    eval_metric=None,
    feature_types=None,
    gamma=None,
    grow_policy=None,
    importance_type=None,
    interaction_constraints=None,
    learning_rate=None,
    max_bin=None,
    max_cat_threshold=None,
    max_cat_to_onehot=None,
    max_delta_step=None,
    max_depth=None,
    max_leaves=None,
    min_child_weight=None,
    monotone_constraints=None,
    multi_strategy=None,
    n_estimators=None,
    n_jobs=None,
    num_parallel_tree=None,
    random_state=None,
)

# Load the dataset: features and labels
X, y = load_dataset()

# Defining the objective function
def objective_fn(trial):
    param = {
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        "gamma": trial.suggest_float("gamma", 0, 5),
    }

    model = xgb.XGBClassifier(
        **param,
    )

    score = cross_val_score(model, X, y, cv=3, scoring="roc_auc").mean()

    return score

# Create and run the optimization process with 100 trials
study = optuna.create_study(study_name="xgboost_study_cuda", direction="maximize")
study.optimize(objective_fn, n_trials=100, show_progress_bar=True, n_jobs=1)

# Get the best parameter values
best_params = study.best_params

logger.info("Best parameters: {best_params}")