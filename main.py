import pandas as pd
import cartopy as ct
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pathlib 

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('Raw Data for Greggs Scrape CSV.csv')

def color_gradient(density):
  """Generates a color based on a given store density."""

  # Normalize the store density to a value between 0 and 1
  normalized_density = density / df['Store_Density'].max()

  # Calculate the red, green, and blue components of the color
  red = 1.0 - normalized_density
  green = 0.0
  blue = normalized_density

# Apply the color gradient function to the store density data
df['color'] = df['Store_Density'].apply(color_gradient)

# Create a GeoAxes object with the specified projection
ax = ccrs.PlateCarree()
ax = plt.axes(projection=ax)

# Plot the local authority boundaries and shade based on store density
for feature in df.iterrows():
  geometry = feature[1]['GlobalID']
  color = feature[1]['color']

  # Plot the local authority boundary with the corresponding color
  ax.add_geometries([geometry], crs=ccrs.OSGB(), facecolor=color, edgecolor='black')

# Add a legend for the color gradient
ax.legend(title='Store Density')

# Save the map to a file
plt.savefig('local_authority_map.png', weakref=False)