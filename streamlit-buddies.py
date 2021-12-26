import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import matplotlib.image as mpimg



st.title('Dashboard for Ocean Wind and Wave Data on Indonesia Fisheries Management Area 711')

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

def data_view(data,title):
    st.subheader(title)
    df = data
    st.write(df)

def data_overview():
    st.header('Summary Statistic')
    data_type = st.selectbox("data type", ['SWH', 'Wind'])
    if data_type == 'SWH':
        data_view(area_swh,'Domain Area')
        data_view(meta_swh,'Metadata')
        data_view(stat_swh,'Statistic Descriptive')
    elif data_type == 'Wind':
        data_view(area_wind,'Domain Area')
        data_view(meta_wind,'Metadata')
        data_view(stat_wind,'Statistic Descriptive')

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
processing_type = st.sidebar.radio("Information", ('Summary Statistic', 'Data Visualisation'))

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
        
        
    








