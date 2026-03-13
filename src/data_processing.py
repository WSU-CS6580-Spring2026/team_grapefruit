# Imports and global definitions

import pandas as pd

processed_path = "https://connorwtech.com/resources/downloads/processed/"


# Load dataset df_A into df_X for transformations

df_2010 = pd.read_csv(processed_path + 'df_A.csv')
df_2020 = pd.read_csv(processed_path + 'df_B.csv')

# For the 2010 Data set DF_X
# Combine female age groups by race

df_2010["NHWA_FEMALE_2034_share_X"] = (
    df_2010["NHWA_FEMALE_2024_C"] + df_2010["NHWA_FEMALE_2529_C"] + df_2010["NHWA_FEMALE_3034_C"]
    ) / (
    df_2010["TOT_FEMALE_2024_C"] + df_2010["TOT_FEMALE_2529_C"] + df_2010["TOT_FEMALE_3034_C"])

df_2010["NHBA_FEMALE_2034_share_X"] = (
    df_2010["NHBA_FEMALE_2024_C"] + df_2010["NHBA_FEMALE_2529_C"] + df_2010["NHBA_FEMALE_3034_C"]
    ) / (
    df_2010["TOT_FEMALE_2024_C"] + df_2010["TOT_FEMALE_2529_C"] + df_2010["TOT_FEMALE_3034_C"])

df_2010["H_FEMALE_2034_share_X"] = (
    df_2010["H_FEMALE_2024_C"] + df_2010["H_FEMALE_2529_C"] + df_2010["H_FEMALE_3034_C"]
    ) / (
    df_2010["TOT_FEMALE_2024_C"] + df_2010["TOT_FEMALE_2529_C"] + df_2010["TOT_FEMALE_3034_C"])


# Create race categories (default "Mixed")

df_2010["race_category_X"] = "Mixed"

df_2010.loc[df_2010["NHWA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "White"
df_2010.loc[df_2010["NHBA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Black"
df_2010.loc[df_2010["H_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Hispanic"


# Create "regime" variable by combining political preference and race categories (default "Minority-majority")

df_2010["regime_X"] = "Minority_majority"

# White-majority
white_mask = df_2010["NHWA_FEMALE_2034_share_X"] >= 0.6

# Mixed
mixed_mask = df_2010["race_category_X"] == "Mixed"

# Political classification
df_2010["pol_group_X"] = "Competitive"
df_2010.loc[df_2010["dem2010_P"] <= 0.4, "pol_group_X"] = "Republican"
df_2010.loc[df_2010["dem2010_P"] >= 0.6, "pol_group_X"] = "Democratic"

# Assign regimes
df_2010.loc[white_mask & (df_2010["pol_group_X"] == "Republican"), "regime_X"] = "White_Republican"
df_2010.loc[white_mask & (df_2010["pol_group_X"] == "Democratic"), "regime_X"] = "White_Democratic"
df_2010.loc[white_mask & (df_2010["pol_group_X"] == "Competitive"), "regime_X"] = "White_Competitive"

df_2010.loc[mixed_mask & (df_2010["pol_group_X"] == "Republican"), "regime_X"] = "Mixed_Republican"
df_2010.loc[mixed_mask & (df_2010["pol_group_X"] == "Democratic"), "regime_X"] = "Mixed_Democratic"
df_2010.loc[mixed_mask & (df_2010["pol_group_X"] == "Competitive"), "regime_X"] = "Mixed_Competitive"


# One-hot encoding

df_2010 = df_2010.loc[:, ~df_2010.columns.str.startswith("reg_")]

regime_dummies = pd.get_dummies(df_2010["regime_X"], prefix="reg")

regime_dummies.columns = regime_dummies.columns + '_X'

# Attach to df_2010
df_2010 = pd.concat([df_2010, regime_dummies], axis=1)

save_path = "../data/processed/"

df_2010.to_csv(save_path + "df_2010.csv", index=False)

# For the 2020 Data set DF_X
# Combine female age groups by race

df_2020["NHWA_FEMALE_2034_share_X"] = (
    df_2020["NHWA_FEMALE_2024_C"] + df_2020["NHWA_FEMALE_2529_C"] + df_2020["NHWA_FEMALE_3034_C"]
    ) / (
    df_2020["TOT_FEMALE_2024_C"] + df_2020["TOT_FEMALE_2529_C"] + df_2020["TOT_FEMALE_3034_C"])

df_2020["NHBA_FEMALE_2034_share_X"] = (
    df_2020["NHBA_FEMALE_2024_C"] + df_2020["NHBA_FEMALE_2529_C"] + df_2020["NHBA_FEMALE_3034_C"]
    ) / (
    df_2020["TOT_FEMALE_2024_C"] + df_2020["TOT_FEMALE_2529_C"] + df_2020["TOT_FEMALE_3034_C"])

df_2020["H_FEMALE_2034_share_X"] = (
    df_2020["H_FEMALE_2024_C"] + df_2020["H_FEMALE_2529_C"] + df_2020["H_FEMALE_3034_C"]
    ) / (
    df_2020["TOT_FEMALE_2024_C"] + df_2020["TOT_FEMALE_2529_C"] + df_2020["TOT_FEMALE_3034_C"])


# Create race categories (default "Mixed")

df_2020["race_category_X"] = "Mixed"

df_2020.loc[df_2020["NHWA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "White"
df_2020.loc[df_2020["NHBA_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Black"
df_2020.loc[df_2020["H_FEMALE_2034_share_X"] >= 0.6, "race_category_X"] = "Hispanic"


# Create "regime" variable by combining political preference and race categories (default "Minority-majority")

df_2020["regime_X"] = "Minority_majority"

# White-majority
white_mask = df_2020["NHWA_FEMALE_2034_share_X"] >= 0.6

# Mixed
mixed_mask = df_2020["race_category_X"] == "Mixed"

# Political classification
df_2020["pol_group_X"] = "Competitive"
df_2020.loc[df_2020["dem2020_P"] <= 0.4, "pol_group_X"] = "Republican"
df_2020.loc[df_2020["dem2020_P"] >= 0.6, "pol_group_X"] = "Democratic"

# Assign regimes
df_2020.loc[white_mask & (df_2020["pol_group_X"] == "Republican"), "regime_X"] = "White_Republican"
df_2020.loc[white_mask & (df_2020["pol_group_X"] == "Democratic"), "regime_X"] = "White_Democratic"
df_2020.loc[white_mask & (df_2020["pol_group_X"] == "Competitive"), "regime_X"] = "White_Competitive"

df_2020.loc[mixed_mask & (df_2020["pol_group_X"] == "Republican"), "regime_X"] = "Mixed_Republican"
df_2020.loc[mixed_mask & (df_2020["pol_group_X"] == "Democratic"), "regime_X"] = "Mixed_Democratic"
df_2020.loc[mixed_mask & (df_2020["pol_group_X"] == "Competitive"), "regime_X"] = "Mixed_Competitive"


# One-hot encoding

df_2020 = df_2020.loc[:, ~df_2020.columns.str.startswith("reg_")]

regime_dummies = pd.get_dummies(df_2020["regime_X"], prefix="reg")

regime_dummies.columns = regime_dummies.columns + '_X'

# Attach to df_2020
df_2020 = pd.concat([df_2020, regime_dummies], axis=1)

save_path = "../data/processed/"

df_2020.to_csv(save_path + "df_2020.csv", index=False)