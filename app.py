import pandas as pd
import plotly.express as px
from math import radians, cos, sin, asin, sqrt
import streamlit as st
df=pd.read_csv(r"C:\work\plotly\Gusto Output Mar 27 2.csv")


user=set(df['User'].unique())
# Add a "Select All" option at the beginning of the list
users = ['Select All'] + list(user)
# Use multiselect instead of selectbox
selected_users = st.sidebar.multiselect(
    "SalesMan",
    users,
     # Select None or the first user by default
    help="Select one or more SalesMan or choose 'Select All' to include all.",
)

# state=set(df['State'].unique())
# # Add a "Select All" option at the beginning of the list
# state = ['Select All'] + list(state)
# # Use multiselect instead of selectbox
# selected_users = st.sidebar.multiselect(
#     "State",
#     users,
#      # Select None or the first user by default
#     help="Select one or more State or choose 'Select All' to include all.",
# )
# #st.write('You selected:', selected_users)

# Filter the DataFrame based on the selected SalesMan
if "Select All" in selected_users:
    filtered_df = df
else:
    filtered_df = df[df['User'].isin(selected_users)]

# Set up layout
#st.sidebar.write('You selected:', selected_users)

# Display filtered DataFrame in top right
st.write(filtered_df)

mean_lat = filtered_df['Latitude'].mean()
mean_lon = filtered_df['Longitude'].mean()

# Calculate distance between points and set zoom level accordingly
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles.
    return c * r

distances = []
for index, row in filtered_df.iterrows():
    dist = haversine(mean_lon, mean_lat, row['Longitude'], row['Latitude'])
    distances.append(dist)

max_distance = max(distances)
mapbox_zoom = round(8 - max_distance / 1000)  # Adjust the divisor as needed for proper zoom level

# Create map plot with automatic zoom
fig = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', hover_name='Outlets Name')

# Update layout for map style and zoom level
fig.update_layout(mapbox_style='open-street-map',
                  mapbox_zoom=mapbox_zoom,
                  mapbox_center={'lat': mean_lat, 'lon': mean_lon},
                  margin={'r':0,'t':0,'l':0,'b':0})

# Show the plot
st.plotly_chart(fig, use_container_width=True)

# Create pie chart
fig_pie = px.pie(filtered_df, values='Net Value', names='User',
             title='Emp Conribution')
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie, use_container_width=True)