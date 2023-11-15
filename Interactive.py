from urllib.request import urlopen
import json
import plotly.express as px
import pandas as pd
import numpy as np

# Fetch the GeoJSON data of UK local authorities
with urlopen('https://raw.githubusercontent.com/thomasvalentine/Choropleth/main/Local_Authority_Districts_(December_2021)_GB_BFC.json') as response:
    Local_authorities = json.load(response)

# Access the local authority code directly from GeoJSON data
geojson_codes = [feature['properties']['LAD21CD'] for feature in Local_authorities['features']]

# Create a DataFrame with local authority codes
geojson_df = pd.DataFrame({'LA': geojson_codes})

# Load store density data from CSV file
store_density_data = pd.read_csv('/workspaces/Mapping/CSV Files/Raw Data for Greggs Scrape CSV.csv')

# Merge store density data with GeoJSON data based on the 'LA' column
merged_data = pd.merge(geojson_df, store_density_data, how='left', on='LA')

# Convert non-numerical values to 200,000
merged_data['Store_Density'] = pd.to_numeric(merged_data['Store_Density'], errors='coerce').fillna(200000)

# Apply a logarithmic transformation to the store density values
merged_data['Store_Density_Log'] = np.log10(merged_data['Store_Density'])

# Create a choropleth map using Plotly Express with 'Blues' color scheme and inverted colors
fig = px.choropleth_mapbox(
    merged_data,
    geojson=Local_authorities,
    locations='LA',
    color='Store_Density_Log',
    featureidkey="properties.LAD21CD",
    color_continuous_scale="Blues_r",  # Use 'Blues_r' for inverted colors
    mapbox_style="carto-positron",
    center={"lat": 55.09621, "lon": -4.0286298},
    zoom=4.2,
    labels={'Store_Density_Log': 'Log Store Density'},
    hover_data=['Name', 'Store_Density']  # Specify columns to be displayed on hover
)

# Update layout and save the figure as a PNG file
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.write_image('interactive_map_south_blues_inverted_log.png')

fig.show()



