import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

# Function to load the CSV file
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Automatically load the CSV file
file_path = 'Bike_Locations_with_GDP_and_PopDensity.csv'
df = load_data(file_path)

# Display the first few rows of the dataset
st.write("### Data Preview")
st.write(df.head())

# Display the summary of the dataset
st.write("### Data Summary")
st.write(df.describe())

# Plot histograms
st.write("### Histogram of GDP (PPP) at Bike Locations")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['GDP_PPP'].dropna(), bins=30, kde=True, ax=ax)
plt.title('Histogram of GDP (PPP) at Bike Locations')
plt.xlabel('GDP (PPP)')
plt.ylabel('Frequency')
st.pyplot(fig)

# Insights
st.write("##### Insights")
st.write("""
1. Skewed distribution to the right. The majority of bike locations are concentrated in areas with lower GDP (PPP) values, as indicated by the high frequency in the lower bins.
2. Significant number of bikes in economically underdeveloped areas - huge potential for marketing!
3. Long tail towards the right - potential outliers with significant growth potential.
""")

st.write("### Histogram of Population Density at Bike Locations")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df['Population_Density'].dropna(), bins=30, kde=True, ax=ax)
plt.title('Histogram of Population Density at Bike Locations')
plt.xlabel('Population Density')
plt.ylabel('Frequency')
st.pyplot(fig)

# Insights
st.write("##### Insights")
st.write("""
Two main clusters:
1. Low population density
2. High population density
This is a huge insight for marketing analytics. Most of our focus has been on densely populated areas!
""")

# Initialize a map centered around the mean location
map_center = [df['Latitude'].mean(), df['Longitude'].mean()]

# Map for GDP (PPP)
st.write("### Map of Bike Locations Colored by GDP (PPP)")
gdp_map = folium.Map(location=map_center, zoom_start=7)
min_gdp = df['GDP_PPP'].min()
max_gdp = df['GDP_PPP'].max()
gdp_colormap = cm.linear.YlOrRd_09.scale(min_gdp, max_gdp)
gdp_colormap.caption = 'GDP (PPP)'

# Add markers to the map with colors based on GDP values
for idx, row in df.iterrows():
    if not pd.isna(row['GDP_PPP']):
        color = gdp_colormap(row['GDP_PPP'])
    else:
        color = 'gray'
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=5,
        popup=f"Vehicle Number: {row['Vehicle Number']}<br>GDP (PPP): {row['GDP_PPP']}<br>Population Density: {row['Population_Density']}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(gdp_map)

# Add the colormap to the map
gdp_colormap.add_to(gdp_map)
gdp_legend_html = f'''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 150px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; opacity: 0.85;">
    &nbsp;<b>Legend</b> <br>
    &nbsp;GDP (PPP) Colors:<br>
    &nbsp;<i class="fa fa-circle" style="color:{gdp_colormap(0)}"></i>&nbsp; Min ({min_gdp})<br>
    &nbsp;<i class="fa fa-circle" style="color:{gdp_colormap(0.5)}"></i>&nbsp; Mid<br>
    &nbsp;<i class="fa fa-circle" style="color:{gdp_colormap(1)}"></i>&nbsp; Max ({max_gdp})<br>
</div>
'''
gdp_map.get_root().html.add_child(folium.Element(gdp_legend_html))
st_folium(gdp_map, width=700, height=500)

# Map for Population Density
st.write("### Map of Bike Locations Colored by Population Density")
pop_density_map = folium.Map(location=map_center, zoom_start=7)
min_pop_density = df['Population_Density'].min()
max_pop_density = df['Population_Density'].max()
pop_density_colormap = cm.linear.YlOrRd_09.scale(min_pop_density, max_pop_density)
pop_density_colormap.caption = 'Population Density'

# Add markers to the map with colors based on population density values
for idx, row in df.iterrows():
    if not pd.isna(row['Population_Density']):
        color = pop_density_colormap(row['Population_Density'])
    else:
        color = 'gray'
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=5,
        popup=f"Vehicle Number: {row['Vehicle Number']}<br>GDP (PPP): {row['GDP_PPP']}<br>Population Density: {row['Population_Density']}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(pop_density_map)

# Add the colormap to the map
pop_density_colormap.add_to(pop_density_map)
pop_density_legend_html = f'''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 150px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; opacity: 0.85;">
    &nbsp;<b>Legend</b> <br>
    &nbsp;Population Density Colors:<br>
    &nbsp;<i class="fa fa-circle" style="color:{pop_density_colormap(0)}"></i>&nbsp; Min ({min_pop_density})<br>
    &nbsp;<i class="fa fa-circle" style="color:{pop_density_colormap(0.5)}"></i>&nbsp; Mid<br>
    &nbsp;<i class="fa fa-circle" style="color:{pop_density_colormap(1)}"></i>&nbsp; Max ({max_pop_density})<br>
</div>
'''
pop_density_map.get_root().html.add_child(folium.Element(pop_density_legend_html))
st_folium(pop_density_map, width=700, height=500)
