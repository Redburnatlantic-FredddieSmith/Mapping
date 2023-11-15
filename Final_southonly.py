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

# Load store density data from CSV file for the south of England
store_density_data = pd.read_csv('/workspaces/Mapping/CSV Files/Raw Data for Greggs Scrape CSV South.csv')

# Merge store density data with GeoJSON data based on the 'LA' column
merged_data = pd.merge(geojson_df, store_density_data, how='left', on='LA')

# Define color scale with grey for NaN values
color_scale = px.colors.sequential.Blues
color_scale.insert(0, '#808080')  # Add grey as the first color

# Create a choropleth map using Plotly Express
fig = px.choropleth_mapbox(
    merged_data,
    geojson=Local_authorities,
    locations='LA',
    color='Store_Density',
    featureidkey="properties.LAD21CD",
    color_continuous_scale=color_scale,  # Use the modified color scale
    color_continuous_midpoint=75,  # Set midpoint for transition
    range_color=[0, 100000],  # Set the expanded range of values
    mapbox_style="carto-positron",
    center={"lat": 51.509865, "lon": -0.40},  # Centered on London
    zoom=6.5,  # Adjust zoom level for a closer look at the south of England
    labels={'Store_Density': 'Store Density'}
)

# Update layout and save the figure as a PNG file
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.write_image('south_with_grey.png')


