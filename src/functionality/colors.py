import matplotlib.colors as mcolors

# Define a function to create RGBA tuples
def rgba_from_value(gdf, color, column, alpha_factor):
    return gdf.apply(lambda row: mcolors.to_rgba(color, alpha=row[column] * alpha_factor), axis=1)
