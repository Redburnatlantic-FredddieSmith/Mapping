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

# Load store density data from CSV file for London
store_density_data = pd.read_csv('/workspaces/Mapping/Raw Data for Greggs Scrape CSV London.csv')

# Merge store density data with GeoJSON data based on the 'LA' column
merged_data = pd.merge(geojson_df, store_density_data, how='left', on='LA')

# Define the center coordinates of London
center_lat = 51.509865
center_lon = -0.118092

# Create a choropleth map using Plotly Express
fig = px.choropleth_mapbox(
    merged_data,
    geojson=Local_authorities,
    locations='LA',
    color='Store_Density',
    featureidkey="properties.LAD21CD",
    color_continuous_scale="Aggrnyl",
    color_continuous_midpoint=75,
    range_color=[0, 100000],
    mapbox_style="carto-positron",
    center={"lat": center_lat, "lon": center_lon},
    zoom=8,  # Adjust the zoom level as needed
    labels={'Store_Density': 'Store Density'}
)

# Update layout and save the figure as a PNG file
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.write_image('centered_on_london.png')
