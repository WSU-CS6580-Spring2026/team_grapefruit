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
#processed_path = "../data/processed/"

pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


# Load Datasets
# One df_X.csv is created we can replace df_A with df_X and run the same code
# to train the model on the new dataset. 
df_X = pd.read_csv(processed_path + "df_X.csv")

# Baseline Model
# Target
y = df_X["birth_rate_2020_N"]

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

# Model I: Percent Change Model

df_I = df_X.copy()

# Percent change
df_I["br_pct_change"] = (df_I["birth_rate_2020_N"] - df_I["birth_rate_2010_N"]) / df_I["birth_rate_2010_N"]
df_I = df_I.replace([np.inf, -np.inf], np.nan).dropna(subset=["br_pct_change", "birth_rate_2010_N"])

reg_cols_I = [c for c in df_I.columns if c.startswith("reg_")]
ref_I = "reg_White_Competitive_X"
reg_cols_model_I = [c for c in reg_cols_I if c != ref_I]

X_I = df_I[reg_cols_model_I].astype(int)          # regime-only
y_I = df_I["br_pct_change"]

X_train_I, X_test_I, y_train_I, y_test_I = train_test_split(X_I, y_I, test_size=0.20, random_state=71)

m_I = LinearRegression().fit(X_train_I, y_train_I)
pred_I = m_I.predict(X_test_I)

rmse_I = np.sqrt(mean_squared_error(y_test_I, pred_I))
mae_I  = mean_absolute_error(y_test_I, pred_I)
print("Percent-change model (regime-only)")
print("RMSE:", round(rmse_I,4), "MAE:", round(mae_I,4))

percent_change_model = {
    "model_type": "linear_regression",
    "target": "br_pct_change",
    "reference_regime": ref_I,
    "features": reg_cols_model_I,
    "model": m_I,
    "rmse": rmse_I,
    "mae": mae_I,
    "n_train": len(X_train_I),
    "n_test": len(X_test_I),
    "random_state": 71
}

dump(percent_change_model, "../model/percent_change_model_regime_only.joblib")



# Model II: Excess 2020 Model

df_II = df_X.copy()
df_II = df_II.dropna(subset=["birth_rate_2010_N", "birth_rate_2020_N"]).copy()

# 1 - baseline trajectory model
base_II = LinearRegression()
X0_II = df_II[["birth_rate_2010_N"]]
y0_II = df_II["birth_rate_2020_N"]
base_II.fit(X0_II, y0_II)

df_II["br2020_pred_from2010"] = base_II.predict(X0_II)
df_II["excess_2020"] = df_II["birth_rate_2020_N"] - df_II["br2020_pred_from2010"]

# 2 - model excess using regimes
reg_cols_II = [c for c in df_II.columns if c.startswith("reg_")]
ref_II = "reg_White_Competitive_X"
reg_cols_model_II = [c for c in reg_cols_II if c != ref_II]

X_II = df_II[reg_cols_model_II].astype(int)
y_II = df_II["excess_2020"]

X_train_II, X_test_II, y_train_II, y_test_II = train_test_split(X_II, y_II, test_size=0.20, random_state=71)

m_II = LinearRegression().fit(X_train_II, y_train_II)
pred_II = m_II.predict(X_test_II)

rmse_II = np.sqrt(mean_squared_error(y_test_II, pred_II))
mae_II  = mean_absolute_error(y_test_II, pred_II)
print("Excess-2020 model (regimes explain deviation from expected trajectory)")
print("RMSE:", round(rmse_II,4), "MAE:", round(mae_II,4))

excess_2020_model = {
    "model_type": "linear_regression",
    "target": "excess_2020",
    "reference_regime": ref_II,
    "features": reg_cols_model_II,
    "model": m_II,
    "rmse": rmse_II,
    "mae": mae_II,
    "n_train": len(X_train_II),
    "n_test": len(X_test_II),
    "random_state": 71
}

dump(excess_2020_model, "../model/excess_2020_model.joblib")



# Model III: Full Interaction Model

df_III = df_X.dropna(subset=["birth_rate_2010_N","birth_rate_2020_N"]).copy()

# Confirm dummies are numeric (0/1) (not True/False)
reg_cols_III = [c for c in df_III.columns if c.startswith("reg_")]
for c in reg_cols_III:
    df_III[c] = df_III[c].astype(int)

ref_III = "reg_White_Competitive_X"
reg_cols_model_III = [c for c in reg_cols_III if c != ref_III]

# Upgrade code to handle hyphens
terms_main_III = " + ".join([f'Q("{c}")' for c in reg_cols_model_III])
terms_int_III  = " + ".join([f'birth_rate_2010_N:Q("{c}")' for c in reg_cols_model_III])

formula = f'birth_rate_2020_N ~ birth_rate_2010_N + {terms_main_III} + {terms_int_III}'

fit_III = smf.ols(formula, data=df_III).fit()
print(fit_III.summary())


full_interaction_model = {
    "model_type": "statsmodels_ols_full_interaction",
    "target": "birth_rate_2020_N",
    "formula": formula,
    "reference_regime": ref_III,
    "features": reg_cols_model_III,
    "model": fit_III,
    "n_train": len(df_III),
    "trained_on_full_data": True,
    "random_state": 71
}

dump(full_interaction_model, "../model/full_interaction_model.joblib")
