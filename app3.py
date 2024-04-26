import pandas as pd
import plotly.express as px
from math import radians, cos, sin, asin, sqrt
from functions import *
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters

st.set_page_config(page_title="Gusto", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: VSTAR")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df=pd.read_csv(r"C:\work\plotly\Gusto Output Mar 27 2.csv")

df['Order Date']=pd.to_datetime(df['Order Date']).dt.date

dynamic_filters = DynamicFilters(df, filters=['User', 'State', 'Beats', 'City', 'PrimaryCategory'])

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


plh = st.container()
script = """<div id = 'chat_outer'></div>"""
st.markdown(script, unsafe_allow_html=True)

col_for_met1,col_for_met2=st.columns(2)

# Show the total sale and quantity
with col_for_met1:
    st.header("Sale And Quantity")
    st.plotly_chart(total_sale_qunatity_indicater(filtered_df))

# Show the Outlet Metrics
with col_for_met2:
    st.header("Outlet Metrics")
    st.plotly_chart(outlets_metrics(filtered_df))


col11, col12, col13 = st.columns(3)

# Show the table
with col11:
    st.header("Table")
    st.write(filtered_df)

# Show the map
with col12:
    st.header("Map")
    st.plotly_chart(map_chart(filtered_df),use_container_width=True)

# show the pie chart
with col13:
    st.header("Pie Chart")
    st.plotly_chart(pie_chart(filtered_df))



col21,col22,col23=st.columns(3)

# Show the trend chart
with col21:
    st.header("Trend Chart")
    st.plotly_chart(trend_chart(filtered_df.groupby('Order Date').aggregate({'Net Value':'sum'}).reset_index()),use_container_width=True)

# Show the sale by product table
with col22:
    st.header("Sale By Product")
    st.write(sale_by_poduct_table(filtered_df).set_index('Product'))

# show sale by PrimaryCategory SecondaryCategory sunburst_chart
with col23:
    st.header("Sale By PrimaryCategory and SecondaryCategory")
    st.plotly_chart(PrimaryCategory_SecondaryCategory_sunburst_chart(filtered_df),use_container_width=True)