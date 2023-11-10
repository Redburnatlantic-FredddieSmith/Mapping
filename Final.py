from urllib.request import urlopen
import json
import plotly.express as px
import pandas as pd

# Fetch the GeoJSON data of UK local authorities
with urlopen('https://raw.githubusercontent.com/thomasvalentine/Choropleth/main/Local_Authority_Districts_(December_2021)_GB_BFC.json') as response:
    Local_authorities = json.load(response)

# Access the local authority code directly from GeoJSON data
geojson_codes = [feature['properties']['LAD21CD'] for feature in Local_authorities['features']]

# Create a DataFrame with local authority codes
geojson_df = pd.DataFrame({'LA': geojson_codes})

# Load store density data from CSV file
store_density_data = pd.read_csv('Raw Data for Greggs Scrape CSV.csv')

# Merge store density data with GeoJSON data based on the 'LA' column
merged_data = pd.merge(geojson_df, store_density_data, how='left', on='LA')

# Create a choropleth map using Plotly Express with dark red to dark blue color scale up to 150k
fig = px.choropleth_mapbox(
    merged_data,
    geojson=Local_authorities,
    locations='LA',
    color='Store_Density',
    featureidkey="properties.LAD21CD",
    color_continuous_scale="RdBu",  # Use the RdBu color scale
    color_continuous_midpoint=75,  # Set midpoint for transition
    range_color=[0, 150000],  # Set the expanded range of values
    mapbox_style="carto-positron",
    center={"lat": 55.09621, "lon": -4.0286298},
    zoom=4.2,
    labels={'Store_Density': 'Store Density'}
)

# Update layout and save the figure as a PNG file
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.write_image('choropleth_map_with_density_dark_red_to_dark_blue_expanded_range.png')
