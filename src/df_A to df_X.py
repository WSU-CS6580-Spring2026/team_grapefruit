# Imports and global definitions

import pandas as pd

processed_path = "https://connorwtech.com/resources/downloads/processed/"


# Load dataset df_A into df_X for transformations

df_X = pd.read_csv(processed_path + 'df_A.csv')


# Combine female age groups by race

df_X["NHWA_FEMALE_2034_share_X"] = (
    df_X["NHWA_FEMALE_2024_C"] + df_X["NHWA_FEMALE_2529_C"] + df_X["NHWA_FEMALE_3034_C"]
    ) / (
    df_X["TOT_FEMALE_2024_C"] + df_X["TOT_FEMALE_2529_C"] + df_X["TOT_FEMALE_3034_C"])

df_X["NHBA_FEMALE_2034_share_X"] = (
    df_X["NHBA_FEMALE_2024_C"] + df_X["NHBA_FEMALE_2529_C"] + df_X["NHBA_FEMALE_3034_C"]
    ) / (
    df_X["TOT_FEMALE_2024_C"] + df_X["TOT_FEMALE_2529_C"] + df_X["TOT_FEMALE_3034_C"])

df_X["H_FEMALE_2034_share_X"] = (
    df_X["H_FEMALE_2024_C"] + df_X["H_FEMALE_2529_C"] + df_X["H_FEMALE_3034_C"]
    ) / (
    df_X["TOT_FEMALE_2024_C"] + df_X["TOT_FEMALE_2529_C"] + df_X["TOT_FEMALE_3034_C"])


# Create race categories (default "Mixed")

df_X["race_category_X"] = "Mixed"

df_X.loc[df_X["NHWA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "White"
df_X.loc[df_X["NHBA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Black"
df_X.loc[df_X["H_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Hispanic"


# Create "regime" variable by combining political preference and race categories (default "Minority-majority")

df_X["regime_X"] = "Minority_majority"

# White-majority
white_mask = df_X["NHWA_FEMALE_2034_share_X"] >= 0.6

# Mixed
mixed_mask = df_X["race_category_X"] == "Mixed"

# Political classification
df_X["pol_group_X"] = "Competitive"
df_X.loc[df_X["dem2010_P"] <= 0.4, "pol_group_X"] = "Republican"
df_X.loc[df_X["dem2010_P"] >= 0.6, "pol_group_X"] = "Democratic"

# Assign regimes
df_X.loc[white_mask & (df_X["pol_group_X"] == "Republican"), "regime_X"] = "White_Republican"
df_X.loc[white_mask & (df_X["pol_group_X"] == "Democratic"), "regime_X"] = "White_Democratic"
df_X.loc[white_mask & (df_X["pol_group_X"] == "Competitive"), "regime_X"] = "White_Competitive"

df_X.loc[mixed_mask & (df_X["pol_group_X"] == "Republican"), "regime_X"] = "Mixed_Republican"
df_X.loc[mixed_mask & (df_X["pol_group_X"] == "Democratic"), "regime_X"] = "Mixed_Democratic"
df_X.loc[mixed_mask & (df_X["pol_group_X"] == "Competitive"), "regime_X"] = "Mixed_Competitive"


# One-hot encoding

df_X = df_X.loc[:, ~df_X.columns.str.startswith("reg_")]

regime_dummies = pd.get_dummies(df_X["regime_X"], prefix="reg")

regime_dummies.columns = regime_dummies.columns + '_X'

# Attach to df_X
df_X = pd.concat([df_X, regime_dummies], axis=1)

save_path = "../data/processed/"

df_X.to_csv(save_path + "df_X.csv", index=False)