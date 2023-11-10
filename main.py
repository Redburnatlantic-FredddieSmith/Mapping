import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pathlib

df = pd.read_csv('Raw Data for Greggs Scrape CSV.csv')

def color_gradient(density, max_density):
    """Generates a color based on a given store density."""
    normalized_density = density / max_density
    red = 1.0 - normalized_density
    green = 0.0
    blue = normalized_density
    return red, green, blue

# Calculate maximum store density for normalization
max_density = df['Store_Density'].max()

df['red'], df['green'], df['blue'] = zip(*df.apply(lambda row: color_gradient(row['Store_Density'], max_density), axis=1))

ax = plt.axes(projection=ccrs.PlateCarree())

for index, row in df.iterrows():
    color = (row['red'], row['green'], row['blue'])

    # Use the 'GlobalID' directly as an identifier
    identifier = row['GlobalID']
    # Plotting a point with the identifier as text
    ax.text(row['LONG'], row['LAT'], identifier, transform=ccrs.PlateCarree(), color=color)

# Create a colorbar to represent the store density
sc = plt.scatter([], [], c=[], cmap='viridis', vmin=0, vmax=max_density)  # Adjust vmin and vmax
plt.colorbar(sc, label='Store Density')

plt.savefig('local_authority_map.png')


