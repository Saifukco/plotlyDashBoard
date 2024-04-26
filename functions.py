import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import radians, cos, sin, asin, sqrt

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'


# Fucntion to create pie chart
def pie_chart(df):
    fig_pie = px.pie(df, values='Net Value', names='User',
             title='Emp Conribution')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    return fig_pie

# Function to create MAP
def map_chart(df):
    # Calculate mean latitude and longitude
    mean_lat = df['Latitude'].mean()
    mean_lon = df['Longitude'].mean()

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
    for index, row in df.iterrows():
        dist = haversine(mean_lon, mean_lat, row['Longitude'], row['Latitude'])
        distances.append(dist)

    max_distance = max(distances)
    mapbox_zoom = round(8 - max_distance / 1000)  # Adjust the divisor as needed for proper zoom level

    # Create map plot with automatic zoom
    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_name='Outlets Name')

    # Update layout for map style and zoom level
    fig.update_layout(mapbox_style='open-street-map',
                    mapbox_zoom=mapbox_zoom,
                    mapbox_center={'lat': mean_lat, 'lon': mean_lon},
                    margin={'r':0,'t':0,'l':0,'b':0})
    return fig

# Function to create trend chart
def trend_chart(df):
    fig_trend = px.line(df, x='Order Date', y="Net Value")
    fig_trend.update_traces(mode = 'lines')
    return fig_trend

# function to creat sale by product table
def sale_by_poduct_table(df):
    cal_df=df.groupby(['Product']).aggregate({"Qty ( Unit )":"sum","Net Value":"sum"}).reset_index()
    cal_df.sort_values(by="Net Value",ascending=False,inplace=True)
    return cal_df

# function to creat by PrimaryCategory SecondaryCategory sunburst_chart
def PrimaryCategory_SecondaryCategory_sunburst_chart(df):
    fig = px.sunburst(df, path=['User','PrimaryCategory', 'SecondaryCategory'], values='Net Value')
    return fig

# Function to show total sales
def total_sale_indicater(df):
    fig = go.Figure(go.Indicator(
    mode = "number",
    value = df['Net Value'].sum(),
    number = {'prefix': "₹" ,"font":{"size":50,'color':'black'}}))
    fig.update_layout(
    paper_bgcolor="lightgray",
    height=100,width=200)
    return fig

# Function to show total Quantity
def total_quantity_indicater(df):
    fig = go.Figure(go.Indicator(
    mode = "number",
    value = df['Qty ( Unit )'].sum(),
    number = {"font":{"size":50,'color':'black'}}))
    fig.update_layout(
    paper_bgcolor="lightgray",
    height=100,width=200)
    return fig

# Function to show total Sale and Quantity
def total_sale_qunatity_indicater(df):    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df['Net Value'].sum(),
        number = {'prefix': "₹" ,"font":{"size":50,'color':'black'}},
        domain = {'row':0,'column':0},
        title={'text':"<span style='font-size:20px;color:black;'>Sale</span>","align":"center"}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df['Qty ( Unit )'].sum(),
        number = {"font":{"size":50,'color':'black'}},
        domain = {'row':0,'column':1},
        title={'text':"<span style='font-size:20px;color:black;'>Quantity</span>","align":"center"}))

    fig.update_layout(
        paper_bgcolor="lightgray",
        height=200,width=420)
    fig.update_layout(
        grid = {'rows': 1, 'columns': 2, 'pattern': "independent"})
    return fig

# Function to show outlet metrics
def outlets_metrics(df):    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df['Outlets Erp Id'].nunique(),
        number = {"font":{"size":50,'color':'black'}},
        domain = {'row':0,'column':0},
        title={'text':"<span style='font-size:20px;color:black;'>Outlet Count</span>","align":"center"}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df[df['Qty ( Unit )']>0]['Outlets Erp Id'].nunique(),
        number = {"font":{"size":50,'color':'black'}},
        domain = {'row':0,'column':2},
        title={'text':"<span style='font-size:20px;color:black;'>Productive Outlet Count</span>","align":"center"}))
    
    fig.add_trace(go.Indicator(
        mode = "number",
        value = df['Net Value'].sum()/df[df['Qty ( Unit )']>0]['Outlets Erp Id'].nunique(),
        number = {'prefix': "₹", "font":{"size":50,'color':'black'}},
        domain = {'row':0,'column':4},
        title={'text':"<span style='font-size:20px;color:black'>AVG Sales By<br><span style='font-size:20px;color:black'>Productive Outlet</span>","align":"center"}))

    fig.update_layout(
        paper_bgcolor="lightgray",
        height=200,width=900)
    fig.update_layout(
        grid = {'rows': 2, 'columns': 3, 'pattern': "independent"})
    return fig