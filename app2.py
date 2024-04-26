import pandas as pd
import plotly.express as px
from math import radians, cos, sin, asin, sqrt
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters

st.set_page_config(page_title="Gusto", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Gusto")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df=pd.read_csv(r"C:\work\plotly\Gusto Output Mar 27 2.csv")

df['Order Date']=pd.to_datetime(df['Order Date']).dt.date

dynamic_filters = DynamicFilters(df, filters=['User', 'State', 'PrimaryCategory', 'City'])

with st.sidebar:
    st.write("Apply filters in any order 👇")

dynamic_filters.display_filters(location='sidebar')

filtered_df = dynamic_filters.filter_df()
# Create a date range slider

with st.sidebar:
    start_date = st.date_input("Start Date", filtered_df['Order Date'].min())
    end_date = st.date_input("End Date", filtered_df['Order Date'].max())
    st.write("Or")

    start_date, end_date = st.sidebar.slider(
        "Select Date Range",
        min_value=filtered_df['Order Date'].min(),
        max_value=filtered_df['Order Date'].max(),
        value=(filtered_df['Order Date'].min(), filtered_df['Order Date'].max())
    )

# Filter the DataFrame based on the selected date range
filtered_df = filtered_df[(df['Order Date'] >= start_date) & (filtered_df['Order Date'] <= end_date)]

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Table")
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
with col2:
    st.header("Map")
    st.plotly_chart(fig,use_container_width=True)

# Create pie chart
fig_pie = px.pie(filtered_df, values='Net Value', names='User',
             title='Emp Conribution')
fig_pie.update_traces(textposition='inside', textinfo='percent+label')

with col3:
    st.header("Pie Chart")
    st.plotly_chart(fig_pie)

# Creat Trend line

fig_trend = px.line(filtered_df, x='Order Date', y="Net Value")
fig_trend.update_traces(mode = 'lines')


st.header("Trend Line")
st.plotly_chart(fig_trend)

st.metric(label="Sale",value=str(filtered_df['Net Value'].sum()))