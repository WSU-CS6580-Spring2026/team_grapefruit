import pandas as pd
import numpy as np
import os

# This program should output locally then user must upload to server manually for security reasons

interim_path = "https://connorwtech.com/resources/downloads/interim/"

# 1.1 Load datasets

N   = pd.read_csv(interim_path + "Natality_2010_2020_interim.csv")

C10 = pd.read_csv(
    interim_path + "/cc-est2019-alldata_interim.csv",
    encoding="latin1"
)

C20 = pd.read_csv(
    interim_path + "/cc-est2023-alldata_interim.csv",
    encoding="latin1"
)

P   = pd.read_csv(interim_path + "/countypres_2000-2024_interim.csv")


# 1.2a1 Natality Preprocessing

# Clean county_code integer column
N["county_code"] = N["County Code"].astype("Int64")

# Rows with unidentified counties
mask_unidentified = (
    N["County"].astype(str).str.strip().str.lower().str.startswith("unidentified")
    | (N["county_code"] % 1000 == 999)
)

# Keep identified rows only
N_clean = N.loc[~mask_unidentified & N["Year"].isin([2010, 2020])].copy()
N_clean["Year"] = N_clean["Year"].astype(int)

# Create common county code
N_clean["county_code"] = N_clean["County Code"].astype("Int64")
N_clean["fips"] = N_clean["county_code"].astype(str).str.zfill(5)


# 1.2a2 Natality Pivoting (one row per county)

N_wide = (
    N_clean
    .pivot_table(
        index="fips",
        columns="Year",
        values=["Birth Rate", "Births", "Total Population"],
        aggfunc="mean"
    )
)

# Flatten column names
N_wide.columns = [
    f"{var.lower().replace(' ', '_')}_{year}"
    for (var, year) in N_wide.columns
]

N_wide = N_wide.reset_index()


# 1.2a3 Natatlity Final

# Counties were included in the analysis only if complete natality data were available for both 2010 and 2020, excluding "Unidentified Counties"

df_N = N_wide.dropna(
    subset=["birth_rate_2010", "birth_rate_2020"]
).copy()

# 1.2b1 Census Preprocessing

# Census AGEGRP → age-band suffix mapping
AGEGRP_TO_SUFFIX = {
    0:  "0000",  # Total population (all ages)
    1:  "0004",  # Ages 0–4
    2:  "0509",  # Ages 5–9
    3:  "1014",  # Ages 10–14
    4:  "1519",  # Ages 15–19
    5:  "2024",  # Ages 20–24
    6:  "2529",  # Ages 25–29
    7:  "3034",  # Ages 30–34
    8:  "3539",  # Ages 35–39
    9:  "4044",  # Ages 40–44
    10: "4549",  # Ages 45–49
    11: "5054",  # Ages 50–54
    12: "5559",  # Ages 55–59
    13: "6064",  # Ages 60–64
    14: "6569",  # Ages 65–69
    15: "7074",  # Ages 70–74
    16: "7579",  # Ages 75–79
    17: "8084",  # Ages 80–84
    18: "8599"   # Ages 85+ (labeled 85–99 for naming consistency)
}

c_agegrps_keep = [4, 5, 6, 7, 8]  # 15–19, 20–24, 25–29, 30–34, 35–39

c_cols_keep = [
    "fips",
    "AGEGRP",
    "TOT_POP",
    "TOT_FEMALE",
    "WA_FEMALE",
    "BA_FEMALE",
    "H_FEMALE"
]

def prep_census(df, name):
    # Build canonical join key
    df = df.copy()
    df["fips"] = df["STATE"].astype(str).str.zfill(2) + df["COUNTY"].astype(str).str.zfill(3)

    # Ensure AGEGRP is clean int for filtering/pivoting
    df["AGEGRP"] = df["AGEGRP"].astype(int)

    # Column existence check
    missing = [c for c in c_cols_keep if c not in df.columns]
    if missing:
        raise KeyError(f"{name}: Missing expected columns: {missing}")

    # Filter to chosen age groups and columns
    out = df.loc[df["AGEGRP"].isin(c_agegrps_keep), c_cols_keep].copy()

    # Optional: sort for predictable merges/pivots
    out = out.sort_values(["fips", "AGEGRP"]).reset_index(drop=True)

    return out

C10_ltd = prep_census(C10, "C10")
C20_ltd = prep_census(C20, "C20")



# 1.2b2 Census Pivoting

def census_to_wide(df_long, vars_to_widen, age_map, name):
    tmp = df_long.copy()
    tmp["age_suffix"] = tmp["AGEGRP"].map(age_map)

    # Safety check: ensure mapping covered all rows
    if tmp["age_suffix"].isna().any():
        missing = sorted(tmp.loc[tmp["age_suffix"].isna(), "AGEGRP"].unique().tolist())
        raise ValueError(f"{name}: AGEGRP values missing from mapping: {missing}")

    wide = tmp.pivot(index="fips", columns="age_suffix", values=vars_to_widen)

    # Flatten (var, age) -> var_age
    wide.columns = [f"{var}_{age}" for (var, age) in wide.columns]
    wide = wide.reset_index()

    return wide

# Columns to widen = everything in c_cols_keep except the keys
vars_to_widen = [c for c in c_cols_keep if c not in ("fips", "AGEGRP")]

wanted_ages = [AGEGRP_TO_SUFFIX[a] for a in c_agegrps_keep]

df_C10 = census_to_wide(C10_ltd, vars_to_widen, AGEGRP_TO_SUFFIX, "C10")
df_C20 = census_to_wide(C20_ltd, vars_to_widen, AGEGRP_TO_SUFFIX, "C20")

# Enforce consistent column order (optional but recommended)
wanted_cols = ["fips"] + [f"{v}_{a}" for v in vars_to_widen for a in wanted_ages]
df_C10 = df_C10[wanted_cols]
df_C20 = df_C20[wanted_cols]



# 1.2c1 Presidential preprocessing

years_baseline = [2008, 2012]
year_actual = 2020
years_keep = years_baseline + [year_actual]

# Work on a copy
Pp = P.copy()

# Keep only years of interest (your file already only has these, but safe)
Pp = Pp.loc[Pp["year"].isin(years_keep)].copy()

# Drop non-county rows (missing county_fips) BEFORE building fips
Pp = Pp.dropna(subset=["county_fips"]).copy()

# Canonical 5-digit FIPS
Pp["county_fips"] = Pp["county_fips"].astype(int)
Pp["fips"] = Pp["county_fips"].astype(str).str.zfill(5)

# Keep only needed columns
Pp = Pp[["fips", "year", "candidatevotes", "totalvotes"]].copy()

# Collapse to one row per county-year (defensive)
P_county_year = (
    Pp.groupby(["fips", "year"], as_index=False)
      .agg({"candidatevotes": "sum", "totalvotes": "max"})
)

# Democratic vote share
P_county_year["dem_share"] = P_county_year["candidatevotes"] / P_county_year["totalvotes"]

# Baseline partisan alignment (average of 2008 & 2012)
dem2010 = (
    P_county_year.loc[P_county_year["year"].isin(years_baseline)]
                 .groupby("fips", as_index=False)["dem_share"]
                 .mean()
                 .rename(columns={"dem_share": "dem2010"})
)

# Contemporary partisan alignment (2020)
dem2020 = (
    P_county_year.loc[P_county_year["year"] == year_actual, ["fips", "dem_share"]]
                 .rename(columns={"dem_share": "dem2020"})
)


# 1.2c2 Presidential final

#County political alignment was measured using Democratic vote share.
#Baseline partisan alignment (dem2010) was calculated as the average Democratic vote share across the 2008 and 2012 presidential elections.
#Contemporary political alignment (dem2020) reflects Democratic vote share in the 2020 presidential election.
#Vote shares were calculated as the proportion of total county-level presidential votes cast for the Democratic candidate.

# Final political dataset
# Retain only counties with both baseline (2008–2012) and 2020 data
df_P = dem2010.merge(dem2020, on="fips", how="inner")


# 1.3 Final datasets

common_fips = (
    set(df_C10["fips"])
    & set(df_C20["fips"])
    & set(df_N["fips"])
    & set(df_P["fips"])
)
common_fips = sorted(common_fips)

# Filter each dataset
C10_c = df_C10[df_C10["fips"].isin(common_fips)].copy()
C20_c = df_C20[df_C20["fips"].isin(common_fips)].copy()
N_c   = df_N[df_N["fips"].isin(common_fips)].copy()
P_c   = df_P[df_P["fips"].isin(common_fips)].copy()

# Adding suffixes to columns to show origin
P_c.rename(columns=lambda x: f"{x}_P" if x != "fips" else x, inplace=True)
N_c.rename(columns=lambda x: f"{x}_N" if x != "fips" else x, inplace=True)
C20_c.rename(columns=lambda x: f"{x}_C" if x != "fips" else x, inplace=True)
C10_c.rename(columns=lambda x: f"{x}_C" if x != "fips" else x, inplace=True)

# Consistent ordering
for d in (C10_c, C20_c, N_c, P_c):
    d.sort_values("fips", inplace=True)
    d.reset_index(drop=True, inplace=True)

df_A = (
    C10_c
    .merge(P_c[["fips", "dem2010_P"]], on="fips", how="inner")
    .merge(
        N_c[["fips", "birth_rate_2010_N", "births_2010_N", "birth_rate_2020_N", "births_2020_N"]],
        on="fips",
        how="inner"
    )
)

df_B = (
    C20_c
    .merge(P_c[["fips", "dem2020_P"]], on="fips", how="inner")
    .merge(
        N_c[["fips", "birth_rate_2020_N", "births_2020_N"]],
        on="fips",
        how="inner"
    )
)

save_path = "../data/processed/"

C10_c.to_csv(save_path + "C10_c.csv", index=False)
C20_c.to_csv(save_path + "C20_c.csv", index=False)
N_c.to_csv(save_path + "N_c.csv", index=False)
P_c.to_csv(save_path + "P_c.csv", index=False)

df_A.to_csv(save_path + "df_A.csv", index=False)
df_B.to_csv(save_path + "df_B.csv", index=False)