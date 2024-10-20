
## CLOROPLETH ##
choropleth = folium.Choropleth(
    geo_data=geojson_path_plz2,
    name="Einwohner",
    data=gdf_plz2,
    columns=["plz", "einwohner"],
    key_on="feature.properties.plz",
    fill_color="YlGn",
    # fill_opacity=0.7,
    # line_opacity=0.1,
    legend_name="Einwohner",
    hover_data=["plz", "qkm", "einwohner"]
)

# geo_data      → Name of the json file. This file must be located in the working directory.
# data          → Name of the data frame containing the data.
# columns       → Columns employed to generate the choropleth map.
# key_on        → Key in the json file that contains the name of the country.
# fill_color    → Color scheme used in the visualization.
    # Sequential:
        # Blues: Blues (BuPu), Blues-Greens (YlGn), Greens (GnBu)
        # Reds: Reds (RdYlGn), Oranges (OrRd), Yellows (YlOrRd)
        # Purples: Purples (PuBuGn), Purples-Blues (YlGnBu)
    # Divergent:
        # Reds-Greens: RdYlGn_r (reversed), OrRd_r
        # Blues-Yellows: BuPu_r, YlGnBu_r
    # Qualitative:
        # Bright colors: Set1, Set2, Set3 (from ColorBrewer’s qualitative palette)
        # Pastel colors: Pastel1, Pastel2, Pastel3 (from ColorBrewer’s qualitative palette)
# fill_opacity  → Area fill opacity, range 0–1 (default 0.6).
# line_opacity  → GeoJSON geopath line opacity, range 0–1 (default 1).
# legend_name   → Title for the legend (default empty string).
# smooth_factor → How much to simplify the polyline on each zoom level.