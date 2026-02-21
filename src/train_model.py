# CS6580 - Sprint 3
# Team Grapefruit
# Weber State University

# Imports and global definitions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from IPython.display import display
import seaborn as sns
from sklearn.model_selection import train_test_split, KFold
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from patsy import dmatrix
import os
from joblib import dump

interim_path = "https://connorwtech.com/resources/downloads/interim/"
processed_path = "https://connorwtech.com/resources/downloads/processed/"

pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


# Load Datasets
# One df_X.csv is created we can replace df_A with df_X and run the same code
# to train the model on the new dataset. 
df_A = pd.read_csv(processed_path + "df_A.csv")

# Baseline Model
# Target
y = df_A["birth_rate_2020_N"]

# Overall mean
y_mean = y.mean()

# Predict mean for every observation
baseline_preds = np.full(len(y), y_mean)

# Evaluate
baseline_rmse = np.sqrt(mean_squared_error(y, baseline_preds))
baseline_mae  = mean_absolute_error(y, baseline_preds)

print("Naive Baseline (Predict Overall Mean)")
print("--------------------------------------")
print("RMSE:", round(baseline_rmse, 4))
print("MAE :", round(baseline_mae, 4))

baseline_model = {
    "type": "mean_baseline",
    "target": "birth_rate_2020_N",
    "mean": y_mean,
    "rmse": baseline_rmse,
    "mae": baseline_mae
}

dump(baseline_model, "../model/baseline_model.joblib")

# TODO: Split data into train/test sets, train a linear regression model, evaluate it, and save the model.