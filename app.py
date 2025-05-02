# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 13:51:48 2025

@author: N28ORIGD
"""
import pandas as pd
import numpy as np
import re
import folium
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import geopandas
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster  

st.set_page_config(page_title='Dashboard', layout='wide')
st.title('Klima Gipuzkoan')

# Set sidebar width
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 500px;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 500px;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title('Estazioa')

# Load data
Estaciones = pd.read_excel('Estaciones_temperatura.xlsx', sheet_name='Hoja4')

# Sidebar selectors
variables = Estaciones['Variable'].unique()
variable = st.sidebar.selectbox('Aldagaia', variables)

estaciones = Estaciones['Estación'].unique()
estacion = st.sidebar.selectbox('Estazioa', estaciones)
st_session_state['estacion']=estacion

# Filter data
filtered_data = Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == variable)]
filtered_data = filtered_data.dropna(subset=['Año', 'Valor'])

filtered_temp=Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == 'Tenperatura / Temperatura')]
filtered_prec=Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == 'Prezipitazioa / Precipitación')]
filtered_flow=Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == 'Emaria / Caudal')]

#Split main panel into two columns
col1,col2=st.columns([2,1])

with col1:

    geometry = geopandas.points_from_xy(Estaciones['long'], Estaciones['lat'])
    geo_df = geopandas.GeoDataFrame(
    Estaciones[["Año", "Estación", "lat", "long", "Variable",'Valor','Tendencia']], geometry=geometry)

    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]
    station_names = geo_df['Estación'].tolist()
    
    map1 = folium.Map(location=[43.178, -2.21], zoom_start=10)
    
    
    for location, name in zip(geo_df_list, station_names):
        folium.Circle(
            location=location,
            radius=6,
            fill=True,

            popup=name,
            tooltip=name
        ).add_to(map1)
    st_data = st_folium(map1, width=700, height=500)

with col2:
    filtered_temp = filtered_temp.dropna(subset=['Año', 'Valor']).copy()
    # Plotly chart
    fig1 = px.line(
        filtered_temp,
        x='Año',
        y='Valor')
    fig1.update_traces(mode='lines+markers',line=dict(color='red')) 
    #calcular la línea de tendencia
    x_temp=filtered_temp['Año'].astype(int)
    y_temp=filtered_temp['Valor']
    z_temp=np.polyfit(x_temp,y_temp,1)
    p_temp=np.poly1d(z_temp)

    #Añadir línea de tendencia
    fig1.add_trace(go.Scatter(
        x=x_temp,
        y=p_temp(x_temp),
        mode='lines',
        name='Tendencia',
        line=go.scatter.Line(color='black',dash='dash',width=3)
    ))
    
    fig1.update_layout(title_x=0.5, xaxis_title='',yaxis_title='T (ºC)', title=estacion,template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

    filtered_prec = filtered_prec.dropna(subset=['Año', 'Valor']).copy()
    fig2=px.bar(
        filtered_prec,
        x='Año',
        y='Valor')
    #calcular la línea de tendencia
    x_prec=filtered_prec['Año'].astype(int)
    y_prec=filtered_prec['Valor']
    z_prec=np.polyfit(x_prec,y_prec,1)
    p_prec=np.poly1d(z_prec)

    fig2.add_trace(go.Scatter(
        x=x_prec,
        y=p_prec(x_prec),
        mode='lines',
        name='Tendencia',
        line=go.scatter.Line(color='red',dash='dot',width=3)
    ))
    fig2.update_layout(title_x=0.5, xaxis_title='',yaxis_title='P (mm)', title='',template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

    filtered_flow = filtered_flow.dropna(subset=['Año', 'Valor']).copy()
    # Plotly chart
    fig3 = px.line(
        filtered_flow,
        x='Año',
        y='Valor')
    fig3.update_traces(mode='lines+markers',line=dict(color='green')) 
    #calcular la línea de tendencia
    x_flow=filtered_flow['Año'].astype(int)
    y_flow=filtered_flow['Valor']
    z_flow=np.polyfit(x_flow,y_flow,1)
    p_flow=np.poly1d(z_flow)

    #Añadir línea de tendencia
    fig3.add_trace(go.Scatter(
        x=x_flow,
        y=p_flow(x_flow),
        mode='lines',
        name='Tendencia',
        line=go.scatter.Line(color='black',dash='dash',width=3)
    ))
    
    fig3.update_layout(title_x=0.5, xaxis_title='',yaxis_title='caudal (m^3/s)', title='',template='plotly_white')
    st.plotly_chart(fig3, use_container_width=True)
