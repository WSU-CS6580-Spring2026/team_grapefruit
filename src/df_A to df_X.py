# Imports and global definitions

import pandas as pd

processed_path = "https://connorwtech.com/resources/downloads/processed/"


# Load datasets

df_A = pd.read_csv(processed_path + 'df_A.csv')


# Combine female age groups by race

df_A["NHWA_FEMALE_2034_share_X"] = (
    df_A["NHWA_FEMALE_2024_C"] + df_A["NHWA_FEMALE_2529_C"] + df_A["NHWA_FEMALE_3034_C"]
    ) / (
    df_A["TOT_FEMALE_2024_C"] + df_A["TOT_FEMALE_2529_C"] + df_A["TOT_FEMALE_3034_C"])

df_A["NHBA_FEMALE_2034_share_X"] = (
    df_A["NHBA_FEMALE_2024_C"] + df_A["NHBA_FEMALE_2529_C"] + df_A["NHBA_FEMALE_3034_C"]
    ) / (
    df_A["TOT_FEMALE_2024_C"] + df_A["TOT_FEMALE_2529_C"] + df_A["TOT_FEMALE_3034_C"])

df_A["H_FEMALE_2034_share_X"] = (
    df_A["H_FEMALE_2024_C"] + df_A["H_FEMALE_2529_C"] + df_A["H_FEMALE_3034_C"]
    ) / (
    df_A["TOT_FEMALE_2024_C"] + df_A["TOT_FEMALE_2529_C"] + df_A["TOT_FEMALE_3034_C"])


# Create race categories (default "Mixed")

df_A["race_category_X"] = "Mixed"

df_A.loc[df_A["NHWA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "White"
df_A.loc[df_A["NHBA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Black"
df_A.loc[df_A["H_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Hispanic"


# Create "regime" variable by combining political preference and race categories (default "Minority-majority")

df_A["regime_X"] = "Minority_majority"

# White-majority
white_mask = df_A["NHWA_FEMALE_2034_share_X"] >= 0.6

# Mixed
mixed_mask = df_A["race_category_X"] == "Mixed"

# Political classification
df_A["pol_group_X"] = "Competitive"
df_A.loc[df_A["dem2010_P"] <= 0.4, "pol_group_X"] = "Republican"
df_A.loc[df_A["dem2010_P"] >= 0.6, "pol_group_X"] = "Democratic"

# Assign regimes
df_A.loc[white_mask & (df_A["pol_group_X"] == "Republican"), "regime_X"] = "White_Republican"
df_A.loc[white_mask & (df_A["pol_group_X"] == "Democratic"), "regime_X"] = "White_Democratic"
df_A.loc[white_mask & (df_A["pol_group_X"] == "Competitive"), "regime_X"] = "White_Competitive"

df_A.loc[mixed_mask & (df_A["pol_group_X"] == "Republican"), "regime_X"] = "Mixed_Republican"
df_A.loc[mixed_mask & (df_A["pol_group_X"] == "Democratic"), "regime_X"] = "Mixed_Democratic"
df_A.loc[mixed_mask & (df_A["pol_group_X"] == "Competitive"), "regime_X"] = "Mixed_Competitive"


# One-hot encoding

df_A = df_A.loc[:, ~df_A.columns.str.startswith("reg_")]

regime_dummies = pd.get_dummies(df_A["regime_X"], prefix="reg")

regime_dummies.columns = regime_dummies.columns + '_X'

# Attach to df_A
df_A = pd.concat([df_A, regime_dummies], axis=1)