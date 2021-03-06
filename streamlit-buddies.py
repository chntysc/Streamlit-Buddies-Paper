import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import matplotlib.image as mpimg

st.set_page_config(layout="wide")
st.title('Dashboard for Ocean Wind and Wave Data on Indonesia Fisheries Management Area 711')
st.subheader('WPP-711')
st.write('WPP-RI 711 is a fisheries management area in Indonesia consisted of Natuna Sea, Karimata Strait, and some part of South China Sea as well as bordering 6 provinces; Riau, Riau Islands, Jambi, Bangka Belitung Islands, West Kalimantan, and South Sumatra. ')
img = mpimg.imread(Path(__file__).parents[0] / 'dataframe/WPP-711.jpg')
st.image(img)
st.write('sc : https://www.researchgate.net/figure/Areas-map-according-to-priority-values-of-four-working-units-in-WPP-711_fig3_322161929')
st.write('This dashboard lets you observe these parameters in WPP-RI 711:')
st.write('1. Wind speed and direction (seasonal, monthly, annual)')
st.write('2. Significant wave height (seasonal, monthly, annual)')
st.write('3. Significant wave height prediction (daily)')
st.write('Data source: ECMWF ERA-5')

# Reading Data CSV
#domain area
#loc_data = Path(__file__).parents[0] / 'dataframe/area_swh.csv'
area_swh = pd.read_csv(Path(__file__).parents[0] / 'dataframe/area_swh.csv',index_col=0)
area_wind = pd.read_csv(Path(__file__).parents[0] / 'dataframe/area_wind.csv',index_col=0)
#metadata
meta_swh = pd.read_csv(Path(__file__).parents[0] / 'dataframe/metadata_swh.csv',index_col=0)
meta_wind = pd.read_csv(Path(__file__).parents[0] / 'dataframe/metadata_wind.csv',index_col=0)
#statistika deskriptif
stat_swh = pd.read_csv(Path(__file__).parents[0] / 'dataframe/descriptive_statistic_data-swh.csv',index_col=0)
stat_wind = pd.read_csv(Path(__file__).parents[0] / 'dataframe/descriptive_statistic_data-wind.csv',index_col=0)
# dataframe untuk plot time-series
df_swh = pd.read_csv(Path(__file__).parents[0] / 'dataframe/df_swh.csv',index_col=0)
df_wind = pd.read_csv(Path(__file__).parents[0] / 'dataframe/df_wind.csv',index_col=0)

def data_view(area,meta,stat):
    col1,col2 = st.beta_columns(2)
    with col1:
        st.subheader('Domain Area')
        st.dataframe(area)
    with col2:
        st.subheader('Metadata')
        st.dataframe(meta)
    
    st.subheader('Statistic Descriptive')
    st.dataframe(stat)

def data_overview():
    st.header('Summary Statistic')
    data_type = st.selectbox("data type", ['SWH', 'Wind'])
    if data_type == 'SWH':
        data_view(area_swh,meta_swh,stat_swh)
    elif data_type == 'Wind':
        data_view(area_wind,meta_wind,stat_wind)

def plot_timeseries(df, title ,var, yaxis): 
#data = data nc , title = variabel judul , misal SWH atau wind, var = variable yang ingin di cari cth 'wind', yaxis = judul yaxisnya apa cth : 'wind (m/s)'
    x = st.sidebar.slider('year', value = [2000,2020], min_value = 2000,max_value = 2020, step = 1)
    st.sidebar.write('Years Interval', x )
    min_year = f'{x[0]}'
    max_year= f'{x[1]}'
    df = df[min_year+'-01-01 06:00:00':max_year+'-12-31 18:00:00']
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df['time.1'],y=df[var],
                         line = dict(color='red', width=2)))
    titled = title

    fig = fig.update_layout(title=f"Time Series {titled}  {x[0]} - {x[1]}",
                  title_x=0.5,
                  font=dict(
        size=15,
        color="black"),
                   xaxis_title='Time',
                   yaxis_title=yaxis,
                  width=1200,
                  height=500,
                  legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01))

    st.write(fig)

def readimagefile(var,period):
    img = mpimg.imread(Path(__file__).parents[0] / f'{var}/{var}{period}.png')
    st.image(img)

def period_choose(period, period_list,var):
    series = st.sidebar.selectbox(period , period_list)
    for i in period_list :
        if series == i :
            readimagefile(var,i)
        else :
            pass
        
def period_time(var):
    variable = var
    st.sidebar.write('Time Period')
    annually = st.sidebar.checkbox('Annually')
    monthly = st.sidebar.checkbox('Monthly')
    seasonally = st.sidebar.checkbox('Seasonally')
    years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
    '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    months = ['January','February', 'March','April','May','June','July','August','September','October','November','December']
    seasons = ['DJF', 'JJA' ,'MAM' ,'SON']
    if annually :
        period_choose('Annually', years,var)
    if monthly :
        period_choose('Monthly', months , var)
    if seasonally:
        period_choose('Seasonally',seasons,var)
    

#sidebar menu
st.sidebar.title('Navigation')
processing_type = st.sidebar.radio("Information", ('Summary Statistic', 'Data Visualisation','Data Prediction'))

if processing_type =='Summary Statistic':
    data_overview()

if processing_type =='Data Visualisation':
    st.header('Data Visualisation')
    data_type = st.sidebar.selectbox("data type", ['SWH', 'Wind'])
    if data_type == 'SWH':
        time_series = st.sidebar.checkbox('Time - Series')
        colormap = st.sidebar.checkbox('Colormap')
        if time_series:
            plot_timeseries(df_swh,'SWH','swh','swh(m)')
        if colormap :
            period_time('swh')
        
    elif data_type =='Wind':
        time_series = st.sidebar.checkbox('Time - Series')
        colormap_quiver = st.sidebar.checkbox('Colormap & Quiver')
        if time_series:
            plot_timeseries(df_wind,'Wind','mag','wind speed(m)')
        if colormap_quiver :
            period_time('wind')
        
        
    








