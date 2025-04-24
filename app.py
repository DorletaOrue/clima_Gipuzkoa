# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 13:51:48 2025

@author: N28ORIGD
"""
import pandas as pd
import re
import folium
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px  
from io import BytesIO

st.set_page_config(page_title='Dashboard', layout='wide')
st.title('Clima Gipuzkoan')

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

# Filter data
filtered_data = Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == variable)]
filtered_data = filtered_data.dropna(subset=['Año', 'Valor'])

filtered_temp=Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == 'Tenperatura / Temperatura')]
filtered_prec=Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == 'Prezipitazioa / Precipitación')]

#Split main panel into two columns
col1,col2=st.columns([2,1])

with col1:
    map1=folium.Map(location=[43.1,-1],zoom_start=12)
    map1

with col2:
    # Plotly chart
    fig1 = px.line(
        filtered_temp,
        x='Año',
        y='Valor')
    fig1.update_traces(mode='lines+markers',line=dict(color='red')) 
    fig1.update_layout(title_x=0.5, xaxis_title='',yaxis_title='T (ºC)', title=estacion,template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

    fig2=px.bar(
        filtered_prec,
        x='Año',
        y='Valor')
    fig2.update_layout(title_x=0.5, xaxis_title='',yaxis_title='P (mm)', title='',template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

