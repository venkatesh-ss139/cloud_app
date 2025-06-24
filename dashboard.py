import geopandas as gpd
import pandas as pd
import hvplot.pandas
import panel as pn
from pandas.api.types import CategoricalDtype

pn.extension()

# -----------------------------
# Parameters
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
bins = [0, 10, 20, 40, 60, float('inf')]
labels = ['0-10', '11-20', '21-40', '41-60', '>60']
cat_dtype = CategoricalDtype(categories=labels, ordered=True)

cmap = {
    '0-10': '#048039',
    '11-20': '#96eb83',
    '21-40': '#f0ee71',
    '41-60': '#eba665',
    '>60':  '#db2b1f'
}

# -----------------------------
# Load your data
gdf = gpd.read_file("cloud_per_data.geojson")

# Let's assume it's already loaded

# Ensure classification columns exist for each month
def add_class_columns(df):
    for month in months:
        col_class = f"{month}_class"
        df[col_class] = pd.cut(df[month], bins=bins, labels=labels, include_lowest=True)
        df[col_class] = df[col_class].astype(cat_dtype)
    return df

gdf = add_class_columns(gdf)

# -----------------------------
# Create a function to generate grid of plots for a given year
def create_monthly_grid(year):
    year_df = gdf[gdf['year'] == year]
    plots = []
    for month in months:
        col = f"{month}_class"
        plot = year_df.hvplot(
            geo=True,
            tiles='CartoLight',
            c=col,
            cmap=cmap,
            colorbar=False,
            legend='right',
            line_color='black',
            title=f"{month} - {year}",
            frame_width=380,
            frame_height=300
        )
        plots.append(plot)
    return pn.GridBox(*plots, ncols=3)

# -----------------------------
# Create year selector widget
year_selector = pn.widgets.Select(name='Select Year', options=sorted(gdf['year'].unique()), value=gdf['year'].max())

# Bind the dashboard to update when year is selected
dashboard = pn.bind(create_monthly_grid, year=year_selector)

# -----------------------------
# Final layout
final_layout = pn.Column(
    "# ☁️ Monthly Cloud Cover - Australia",
    "Select a year to view tile-wise cloud percentage from Jan to Jun.",
    year_selector,
    dashboard
)

# Show the dashboard
final_layout.show()