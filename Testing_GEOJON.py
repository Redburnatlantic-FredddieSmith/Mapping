from urllib.request import urlopen
import json
import plotly.express as px

with urlopen('https://raw.githubusercontent.com/thomasvalentine/Choropleth/main/Local_Authority_Districts_(December_2021)_GB_BFC.json') as response:
    Local_authorities = json.load(response)

    la_data = []
# Iterative over JSON
for i in range(len(Local_authorities["features"])):
    # Extract local authority name
    la = Local_authorities["features"][i]['properties']['LAD21NM']
    # Assign the local authority name to a new 'id' property for later linking to dataframe
    Local_authorities["features"][i]['id'] = la
    # While I'm at it, append local authority name to a list to make some dummy data to test, along with i for a value to test on map
    la_data.append([la,i])

import pandas as pd

# turn dummy data into a dataframe
df = pd.DataFrame(la_data)
# update column names
df.columns = ['LA','Val']

fig = px.choropleth_mapbox(df,geojson=Local_authorities,locations='LA', color='Val',featureidkey="properties.LAD21NM",color_continuous_scale="Viridis", mapbox_style="carto-positron",center={"lat": 55.09621, "lon": -4.0286298},zoom=4.2,
labels={'val':'value'})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# Save the figure as a PNG file
fig.write_image('choropleth_map.png')