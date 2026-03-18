import geopandas as gpd
import matplotlib.pyplot as plt

def plot_county_highlight(fips_code: str):
    state_fips = fips_code[:2]

    # Lightweight GeoJSON (no GDAL, no Fiona)
    counties_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    counties = gpd.read_file(counties_url)

    counties["id"] = counties["id"].astype(str)

    # Filter to state
    state_counties = counties[counties["id"].str.startswith(state_fips)]

    # Selected county
    selected = counties[counties["id"] == fips_code]
    if selected.empty:
        raise ValueError(f"FIPS {fips_code} not found")

    fig, ax = plt.subplots(figsize=(10, 10))

    state_counties.plot(ax=ax, color="#e0e0e0", edgecolor="black", linewidth=0.5)
    selected.plot(ax=ax, color="orange", edgecolor="red", linewidth=1.5)

    plt.title(f"County Highlight: {fips_code}")
    plt.axis("off")
    plt.show()

plot_county_highlight("49057")