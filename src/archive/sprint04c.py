# Imports and global definitions

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import geopandas as gpd
import joblib
from pathlib import Path
from PIL import Image

# Load image
ROOT = Path(__file__).resolve().parent.parent

img = Image.open(ROOT / 'docs/social political demographic groups_hc.PNG')

def plot_county_highlight(fips_code: str, county_name: str, df_rates: pd.DataFrame):
    """
    df_rates must contain:
        - 'fips' (string)
        - 'rate' (float, may contain NaN)
    """

    state_fips = fips_code[:2]

    counties_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    counties = gpd.read_file(counties_url)

    counties["id"] = counties["id"].astype(str)

    # --- Reproject only for Alaska ---
    if state_fips == "02":
        counties = counties.to_crs("EPSG:3338")   # Alaska Albers
    else:
        counties = counties.to_crs("EPSG:3857")   # Web Mercator

    # --- Filter to state ---
    state_counties = counties[counties["id"].str.startswith(state_fips)].copy()

    # --- Merge in birth-rate values ---
    df_rates = df_rates.copy()
    df_rates["fips"] = df_rates["fips"].astype(str)

    state_counties = state_counties.merge(
        df_rates[["fips", "rate"]],
        left_on="id",
        right_on="fips",
        how="left"
    )

    # --- Selected county geometry ---
    selected = state_counties[state_counties["id"] == fips_code]
    if selected.empty:
        raise ValueError(f"FIPS {fips_code} not found")

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(7, 7))

    # Heatmap: counties with rate → colormap, missing → grey
    state_counties.plot(
        ax=ax,
        column="rate",
        cmap="viridis",
        missing_kwds={
            "color": "lightgrey",
            "edgecolor": "black",
            "hatch": "///",
            "label": "No data"
        },
        linewidth=0.4,
        edgecolor="black"
    )

    # Highlight selected county
    selected.plot(
        ax=ax,
        facecolor="none",
        edgecolor="red",
        linewidth=2.0
    )

    ax.set_title(f"{county_name} : {fips_code}")
    ax.axis("off")

    st.pyplot(fig, width="content")
    plt.close(fig)

    
st.set_page_config(layout="wide")

# Load datasets

processed_path = "https://connorwtech.com/resources/downloads/processed/"
interim_path = "https://connorwtech.com/resources/downloads/interim/"

# Load datasets
df_2010 = pd.read_csv(processed_path + 'df_2010.csv')
df_2020 = pd.read_csv(processed_path + 'df_2020.csv')

P = pd.read_csv(interim_path + "countypres_2000-2024_interim.csv")

C10 = pd.read_csv(interim_path + "cc-est2019-alldata_interim.csv", encoding="latin1")
C20 = pd.read_csv(interim_path + "cc-est2023-alldata_interim.csv", encoding="latin1")

# NOTE: IT IS INTENDED THAT THIS WILL BE EARLIER STANDALONE CODE, OR INTEGRATED INTO PRIOR CODE, TO CREATE df_2020.csv
# ALSO NOTE: it is intended that the current df_X.csv will be renamed as df_2010.csv; that should happen in the original generation code


# normalize fips
df_2010["fips"] = df_2010["fips"].astype(str).str.zfill(5)
df_2020["fips"] = df_2020["fips"].astype(str).str.zfill(5)

# Update names from P
P_tmp = P[["county_fips", "state", "county_name"]].copy()
P_tmp["fips"] = P_tmp["county_fips"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(5)
P_tmp = P_tmp.drop(columns=["county_fips"]).drop_duplicates("fips")

P_tmp["state"] = P_tmp["state"].astype(str).str.title()
P_tmp["county"] = P_tmp["county_name"].astype(str).str.title()
P_tmp = P_tmp.drop(columns=["county_name"])

# eliminate superfluous information from bases
base_2010 = df_2010[["fips", "birth_rate_2010_N", "birth_rate_2020_N", "regime_X"]].copy()
base_2010 = base_2010.rename(columns={"regime_X": "regime_2010"})

base_2020 = df_2020[["fips", "regime_X"]].copy()
base_2020 = base_2020.rename(columns={"regime_X": "regime_2020"})

br_2020 = df_2020[["fips", "birth_rate_2020_N"]].copy()

# 2010 population lookup
pop10 = C10[
    (C10["SUMLEV"] == 50) &
    (C10["AGEGRP"] == 0)
][["STATE", "COUNTY", "TOT_POP"]].copy()

pop10["fips"] = (
    pop10["STATE"].astype(int).astype(str).str.zfill(2) +
    pop10["COUNTY"].astype(int).astype(str).str.zfill(3)
)

pop10 = pop10.rename(columns={"TOT_POP": "pop_2010"})
pop10 = pop10[["fips", "pop_2010"]]


# 2020 population
pop20 = C20[
    (C20["SUMLEV"] == 50) &
    (C20["AGEGRP"] == 0)
][["STATE", "COUNTY", "TOT_POP"]].copy()

pop20["fips"] = (
    pop20["STATE"].astype(int).astype(str).str.zfill(2) +
    pop20["COUNTY"].astype(int).astype(str).str.zfill(3)
)

pop20 = pop20.rename(columns={"TOT_POP": "pop_2020"})
pop20 = pop20[["fips", "pop_2020"]]

# build df_app as overall singular df
df_app = (
    base_2010
    .merge(base_2020, on="fips", how="left")
    .merge(br_2020, on="fips", how="left", suffixes=("", "_from_B"))
    .merge(P_tmp, on="fips", how="left")
)

df_app = df_app.merge(pop10, on="fips", how="left")
df_app = df_app.merge(pop20, on="fips", how="left")


# build dropdown label
df_app["dropdown_label"] = df_app["state"] + " - " + df_app["county"]

# final column order
df_app = df_app[
    ["fips", "dropdown_label", "state", "county",
     "pop_2010", "pop_2020",
     "regime_2010", "regime_2020",
     "birth_rate_2010_N", "birth_rate_2020_N"
    ]
].copy()


reg_cols = [
    "reg_Minority_majority_X",
    "reg_Mixed_Competitive_X",
    "reg_Mixed_Democratic_X",
    "reg_Mixed_Republican_X",
    "reg_White_Competitive_X",
    "reg_White_Democratic_X",
    "reg_White_Republican_X",
]

# Path to the project root (folder containing "model/")
ROOT = Path(__file__).resolve().parent.parent

# Path to the model directory
MODEL_DIR = ROOT / "model"

# Load the model
model_path = MODEL_DIR / "full_interaction_model.joblib"

loaded = joblib.load(model_path)
fit = loaded["model"]   # <-- this is the actual statsmodels model


# -------------------------
# 2) Predict 2030 using 2020 as the baseline
#    (using 2010->2020)
# -------------------------

pred = df_2020.dropna(subset=["birth_rate_2020_N"]).copy()

# dummies --> numeric 0/1
for c in reg_cols:
    pred[c] = pred[c].astype(int)

# use model on 2020 data
pred["birth_rate_2010_N"] = pred["birth_rate_2020_N"]

pred["birth_rate_2030_pred"] = fit.predict(pred)

# Get prediction object
pred_results = fit.get_prediction(pred)

pred_summary = pred_results.summary_frame(alpha=0.05)

# add prediction to 2020 df
df_2020["birth_rate_2030_pred"] = pred_summary["mean"]
df_2020["birth_rate_2030_ci_lower"] = pred_summary["obs_ci_lower"]
df_2020["birth_rate_2030_ci_upper"] = pred_summary["obs_ci_upper"]

# update df_app
proj_cols = [
    "fips",
    "birth_rate_2030_pred",
    "birth_rate_2030_ci_lower",
    "birth_rate_2030_ci_upper"
]

df_app = df_app.merge(
    df_2020[proj_cols],
    on="fips",
    how="left"
)

def nearest_lists(
    df_app: pd.DataFrame,
    selected_fips: str,
    rate_col: str = "birth_rate_2030_pred",
    regime_col: str = "regime_2020",
    k: int = 5
):
    df = df_app.copy()
    df["fips"] = df["fips"].astype(str).str.zfill(5)
    selected_fips = str(selected_fips).zfill(5)

    if selected_fips not in set(df["fips"]):
        raise ValueError(f"selected_fips {selected_fips} not found")

    df[rate_col] = pd.to_numeric(df[rate_col], errors="coerce")

    target = df.loc[df["fips"] == selected_fips].iloc[0]
    target_rate = target[rate_col]

    cand = df.dropna(subset=[rate_col]).copy()
    cand["abs_diff"] = (cand[rate_col] - target_rate).abs()

    # ---- OVERALL LIST ----
    # Sort by distance
    sorted_cand = cand.sort_values("abs_diff")

    # Take k+1 closest (this includes the selected county automatically)
    overall = (
        sorted_cand.head(k + 1)
                   .sort_values(rate_col)
                   .copy()
    )

    # ---- SAME-REGIME LIST ----
    same = None
    if regime_col in df.columns and pd.notna(target[regime_col]):
        same_reg = cand[cand[regime_col] == target[regime_col]].copy()
        same = (
            same_reg.sort_values("abs_diff")
                    .head(k + 1)
                    .sort_values(rate_col)
                    .copy()
        )

    # ---- FORMAT OUTPUT ----
    def format_out(d):
        if d is None:
            return None
        out = d[["fips", "state", "county", rate_col, "abs_diff"]].copy()
        out["label"] = out["state"].astype(str) + " - " + out["county"].astype(str)
        out["is_selected"] = (out["fips"] == selected_fips).astype(int)
        out = out.rename(columns={rate_col: "rate"})
        return out[["label", "rate", "is_selected"]].reset_index(drop=True)

    return target, format_out(overall), format_out(same)

# county data we want displayed
def county_report(df_app: pd.DataFrame, selection: str, k: int = 5, rate_col: str = "birth_rate_2030_pred"):
    """
    selection can be either:
      - fips (e.g., '49057')
      - dropdown_label (e.g., 'Utah - Weber')
    Returns a dict with the selected county details + two neighbor tables.
    """
    df = df_app.copy()
    df["fips"] = df["fips"].astype(str).str.zfill(5)

    # Resolve selection -> fips
    s = str(selection).strip()

    if s.isdigit() and len(s) <= 5:
        selected_fips = s.zfill(5)
    else:
        # assume dropdown label
        matches = df[df["dropdown_label"].astype(str).str.lower() == s.lower()]
        if matches.empty:
            # fail-safe
            matches = df[df["dropdown_label"].astype(str).str.lower().str.contains(s.lower(), na=False)]
        if len(matches) != 1:
            raise ValueError(f"Selection '{selection}' matched {len(matches)} counties; need exactly 1.")
        selected_fips = matches.iloc[0]["fips"]

    target, nearest_any, nearest_same = nearest_lists(
        df_app=df,
        selected_fips=selected_fips,
        rate_col=rate_col,
        regime_col="regime_2020",
        k=k
    )

    # panel of values
    panel = {
        "State": target.get("state", None),
        "County": target.get("county", None),
        "FIPS": target.get("fips", None),
        "2010 population": int(target["pop_2010"]) if pd.notna(target.get("pop_2010", np.nan)) else None,
        "2010 Socio-Political Category": target.get("regime_2010", None),
        "2020 population": int(target["pop_2020"]) if pd.notna(target.get("pop_2020", np.nan)) else None,
        "2020 Socio-Political Category": target.get("regime_2020", None),
        "2010 birth rate": float(target["birth_rate_2010_N"]) if pd.notna(target.get("birth_rate_2010_N", np.nan)) else None,
        "2020 birth rate": float(target["birth_rate_2020_N"]) if pd.notna(target.get("birth_rate_2020_N", np.nan)) else None,
        "2030 birth rate (projected)": float(target["birth_rate_2030_pred"]) if pd.notna(target.get("birth_rate_2030_pred", np.nan)) else None,
        "2030 projection (95% lower)": float(target["birth_rate_2030_ci_lower"]) if pd.notna(target.get("birth_rate_2030_ci_lower", np.nan)) else None,
        "2030 projection (95% upper)": float(target["birth_rate_2030_ci_upper"]) if pd.notna(target.get("birth_rate_2030_ci_upper", np.nan)) else None,
    }

    result = {
        "panel": panel,
        "nearest_any": nearest_any,
        "nearest_same_regime": nearest_same
    }
    return result

def format_panel_value(key, value):
    # Add commas to population numbers
    if "population" in key.lower() and isinstance(value, (int, float)):
        return f"{int(value):,}"

    # Round birth rates / projections
    if isinstance(value, float):
        return f"{value:.2f}"

    return value


def highlight_selected_row(row):
    if row["is_selected"] == 1:
        return ["background-color: #2a4d69; color: white; font-weight: bold;"] * len(row)
    return [""] * len(row)


# county plot addendum
def plot_county_trend_with_cone(df_app: pd.DataFrame, selection: str):
    df = df_app.copy()
    df["fips"] = df["fips"].astype(str).str.zfill(5)

    # Resolve selection -> fips
    s = str(selection).strip()
    if s.isdigit() and len(s) <= 5:
        fips = s.zfill(5)
    else:
        m = df[df["dropdown_label"].astype(str).str.lower() == s.lower()]
        if m.empty:
            m = df[df["dropdown_label"].astype(str).str.lower().str.contains(s.lower(), na=False)]
        if len(m) != 1:
            raise ValueError(f"Selection '{selection}' matched {len(m)} counties; need exactly 1.")
        fips = m.iloc[0]["fips"]

    row = df.loc[df["fips"] == fips].iloc[0]

    # Values
    y2010 = row["birth_rate_2010_N"]
    y2020 = row["birth_rate_2020_N"]
    y2030 = row["birth_rate_2030_pred"]
    lo2030 = row["birth_rate_2030_ci_lower"]
    hi2030 = row["birth_rate_2030_ci_upper"]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Actual
    ax.plot([2010, 2020], [y2010, y2020], marker="o", linewidth=2, label="Observed")

    # Forecast (dashed)
    ax.plot([2020, 2030], [y2020, y2030], marker="o", linestyle="--", linewidth=2, label="Projected")

    # Projection cone
    ax.fill_between(
        [2020, 2030],
        [y2020, lo2030],
        [y2020, hi2030],
        alpha=0.15,
        label="95% CI"
    )

    ax.set_title(f"{row['county']}, {row['state']} Birth Rate Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Birth Rate (per 1,000)")
    ax.set_xticks([2010, 2020, 2030])
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
#    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# display county report to Streamlit
def print_county_summary(report: dict):
    panel = report["panel"]

    county = panel.get("County", "")
    state = panel.get("State", "")

    lower = panel.get("2030 projection (95% lower)")
    upper = panel.get("2030 projection (95% upper)")

    highlight_blue = "#476a9f"

    st.markdown(
        f"""
        <h1 style="color: {highlight_blue}; margin-bottom: 0;">
            {county} County, {state}
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.caption("County demographic profile and projected 2030 birth rate per 1,000 population")

    st.subheader("County Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem;">Location</p>',
            unsafe_allow_html=True
        )
        st.write(f"**State:** {panel.get('State', '')}")
        st.write(f"**County:** {panel.get('County', '')}")
        st.write(f"**FIPS:** {panel.get('FIPS', '')}")

        st.markdown(
            f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem; margin-top: 1rem;">Birth Rates</p>',
            unsafe_allow_html=True
        )
        st.write(f"**2010 Birth Rate:** {panel.get('2010 birth rate', 0):.2f}")
        st.write(f"**2020 Birth Rate:** {panel.get('2020 birth rate', 0):.2f}")
        st.write(f"**2030 Projected Birth Rate:** {panel.get('2030 birth rate (projected)', 0):.2f}")

        if lower is not None and upper is not None:
            st.write(f"**2030 Projection (95% CI):** {lower:.2f} - {upper:.2f}")

    with col2:
        st.markdown(
            f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem;">Population</p>',
            unsafe_allow_html=True
        )
        st.write(f"**2010 Population:** {int(panel.get('2010 population', 0)):,}")
        st.write(f"**2020 Population:** {int(panel.get('2020 population', 0)):,}")

        st.markdown(
            f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem; margin-top: 1rem;">Socio-Political Category</p>',
            unsafe_allow_html=True
        )
        st.write(f"**2010:** {panel.get('2010 Socio-Political Category', '')}")
        st.write(f"**2020:** {panel.get('2020 Socio-Political Category', '')}")

def print_county_tables(report_any: dict, report_same: dict, show_any=True, show_same=True, k_any=5, k_same=5):
    if show_any:
        st.subheader(f"{k_any} Closest Counties by Projected 2030 Birth Rate")

        df_any_full = report_any["nearest_any"].copy()
        df_any_selected = df_any_full[df_any_full["is_selected"] == 1]
        df_any_others = df_any_full[df_any_full["is_selected"] != 1]

        # df_any = pd.concat(
        #     [df_any_selected, df_any_others.head(k_any)],
        #     ignore_index=True
        # )
        
        df_any = df_any_full.head(k_any + 1)
        
        df_any["rate"] = df_any["rate"].round(2)
        
        styled_any = (
            df_any.style
            .format({"rate": "{:.2f}"})
            .apply(highlight_selected_row, axis=1)
            .set_properties(subset=["rate"], **{"text-align": "right"})
        )

        st.dataframe(
            styled_any,
            hide_index=True,
            width='content',
            column_config={
                "label": st.column_config.TextColumn("County", width="medium"),
                "rate": st.column_config.NumberColumn("2030 Birth Rate (per 1,000)", format="%.2f"),
                "is_selected": None,
            },
        )

    if show_same:
        st.subheader(f"{k_same} Closest Counties in the Same Socio-Political Category")

        ns = report_same["nearest_same_regime"]
        print("NS: ")
        print(ns)
        print("\n\n")
        if ns is not None:
            df_same_full = ns.copy()
            df_same_selected = df_same_full[df_same_full["is_selected"] == 1]
            df_same_others = df_same_full[df_same_full["is_selected"] != 1]

            df_same = df_same_full.head(k_same + 1)
            
            # df_same = pd.concat(
            #     [df_same_selected, df_same_others.head(k_same)],
            #     ignore_index=True
            # )
            df_same["rate"] = df_same["rate"].round(2)

            styled_same = (
                df_same.style
                .format({"rate": "{:.2f}"})
                .apply(highlight_selected_row, axis=1)
                .set_properties(subset=["rate"], **{"text-align": "right"})
            )

            st.dataframe(
                styled_same,
                hide_index=True,
                width='content',
                column_config={
                    "label": st.column_config.TextColumn("County", width="medium"),
                    "rate": st.column_config.NumberColumn("2030 Birth Rate (per 1,000)", format="%.2f"),
                    "is_selected": None,
                },
            )
        else:
            st.write("(No same-category matches available)")

# # display county report to Streamlit
# def print_county_report2(report: dict, show_any=True, show_same=True, k_any=5, k_same=5):
#     panel = report["panel"]

#     county = panel.get("County", "")
#     state = panel.get("State", "")

#     lower = panel.get("2030 projection (95% lower)")
#     upper = panel.get("2030 projection (95% upper)")

#     highlight_blue = "#476a9f"

#     # Title
#     st.markdown(
#         f"""
#         <h1 style="color: {highlight_blue}; margin-bottom: 0;">
#             {county} County, {state}
#         </h1>
#         """,
#         unsafe_allow_html=True
#     )

#     st.caption("County demographic profile and projected 2030 birth rate per 1,000 population")

#     st.subheader("County Summary")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown(
#             f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem;">Location</p>',
#             unsafe_allow_html=True
#         )
#         st.write(f"**State:** {panel.get('State', '')}")
#         st.write(f"**County:** {panel.get('County', '')}")
#         st.write(f"**FIPS:** {panel.get('FIPS', '')}")

#         st.markdown(
#             f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem; margin-top: 1rem;">Birth Rates</p>',
#             unsafe_allow_html=True
#         )
#         st.write(f"**2010 Birth Rate:** {panel.get('2010 birth rate', 0):.2f}")
#         st.write(f"**2020 Birth Rate:** {panel.get('2020 birth rate', 0):.2f}")
#         st.write(f"**2030 Projected Birth Rate:** {panel.get('2030 birth rate (projected)', 0):.2f}")

#         if lower is not None and upper is not None:
#             st.write(f"**2030 Projection (95% CI):** {lower:.2f} - {upper:.2f}")

#     with col2:
#         st.markdown(
#             f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem;">Population</p>',
#             unsafe_allow_html=True
#         )
#         st.write(f"**2010 Population:** {int(panel.get('2010 population', 0)):,}")
#         st.write(f"**2020 Population:** {int(panel.get('2020 population', 0)):,}")

#         st.markdown(
#             f'<p style="color: {highlight_blue}; font-weight: bold; font-size: 1.1rem; margin-top: 1rem;">Socio-Political Category</p>',
#             unsafe_allow_html=True
#         )
#         st.write(f"**2010:** {panel.get('2010 Socio-Political Category', '')}")
#         st.write(f"**2020:** {panel.get('2020 Socio-Political Category', '')}")


#     st.subheader("Birth Rate Trend")
#     plot_county_trend_with_cone(df_app, st_cnt)

#     # ---- nearest_any table ----
#     if show_any:
#         st.subheader(f"{k_any} Closest Counties by Projected 2030 Birth Rate")

#         df_any_full = report["nearest_any"].copy()

#         df_any_selected = df_any_full[df_any_full["is_selected"] == 1]
#         df_any_others = df_any_full[df_any_full["is_selected"] != 1]

#         df_any = pd.concat(
#             [df_any_selected, df_any_others.head(k_any + 1)],
#             ignore_index=True
#         )
#         df_any["rate"] = df_any["rate"].round(2)

#         styled_any = (
#             df_any.style
#             .format({"rate": "{:.2f}"})
#             .apply(highlight_selected_row, axis=1)
#             .set_properties(subset=["rate"], **{"text-align": "right"})
#         )

#         st.dataframe(
#             styled_any,
#             hide_index=True,
#             width='content',
#             column_config={
#                 "label": st.column_config.TextColumn("County", width="medium"),
#                 "rate": st.column_config.NumberColumn("2030 Birth Rate (per 1,000)", format="%.2f"),
#                 "is_selected": None,
#             },
#         )

#     # ---- nearest_same_regime table ----
#     if show_same:
#         st.subheader(f"{k_same} Closest Counties in the Same Socio-Political Category")

#         ns = report["nearest_same_regime"]
#         if ns is not None:
#             df_same_full = ns.copy()

#             df_same_selected = df_same_full[df_same_full["is_selected"] == 1]
#             df_same_others = df_same_full[df_same_full["is_selected"] != 1]

#             df_same = pd.concat(
#                 [df_same_selected, df_same_others.head(k_same + 1)],
#                 ignore_index=True
#             )
#             df_same["rate"] = df_same["rate"].round(2)

#             styled_same = (
#                 df_same.style
#                 .format({"rate": "{:.2f}"})
#                 .apply(highlight_selected_row, axis=1)
#                 .set_properties(subset=["rate"], **{"text-align": "right"})
#             )

#             st.dataframe(
#                 styled_same,
#                 hide_index=True,
#                 width='content',
#                 column_config={
#                     "label": st.column_config.TextColumn("County", width="medium"),
#                     "rate": st.column_config.NumberColumn("2030 Birth Rate (per 1,000)", format="%.2f"),
#                     "is_selected": None,
#                 },
#             )
#         else:
#             st.write("(No same-category matches available)")


# launch section

# ---- Dashboard (left side) ----
st.sidebar.header("County Explorer")

county_list = sorted(df_app["dropdown_label"].tolist())

st_cnt = st.sidebar.selectbox(
    "Select a County",
    county_list,
    index=county_list.index("Utah - Weber")
)

# print(county_list)

st.sidebar.divider()

show_any = st.sidebar.checkbox("Show closest counties (any)", value=True)
k_any = st.sidebar.slider("How many (any)", min_value=1, max_value=10, value=5)

st.sidebar.divider()

show_same = st.sidebar.checkbox("Show closest counties (same category)", value=True)
k_same = st.sidebar.slider("How many (same category)", min_value=1, max_value=10, value=5)

k_max = max(k_any, k_same)

rep_any  = county_report(df_app, st_cnt, k=k_any,  rate_col="birth_rate_2030_pred")
rep_same = county_report(df_app, st_cnt, k=k_same, rate_col="birth_rate_2030_pred")

rep = county_report(df_app, st_cnt, k=k_max, rate_col="birth_rate_2030_pred")
print("FIPS Code: " + rep["panel"]["FIPS"])

# ---- Main layout ----
left, right, margin = st.columns([1.6, 0.8, 0.6])

with left:
    print_county_summary(rep)
    # ---- Tables below ----
    print_county_tables(
        rep_any,
        rep_same,
        show_any=show_any,
        show_same=show_same,
        k_any=k_any,
        k_same=k_same
    )

with right:
    st.subheader("Birth Rate Trend")
    plot_county_trend_with_cone(df_app, st_cnt)
    df_rates = df_app[["fips", "birth_rate_2030_pred"]].rename(
        columns={"birth_rate_2030_pred": "rate"}
    )
    
    plot_county_highlight(
        rep["panel"]["FIPS"],
        st_cnt,
        df_rates
    )

    st.image(img)
