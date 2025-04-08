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
from io import BytesIO

st.set_page_config(page_title='Dashboard', layout='wide')
st.title('Clima Gipuzkoan')

# Set sidebar width
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 800px;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 800px;
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

# Plotly chart
if not filtered_data.empty:
    fig = px.line(
        filtered_data,
        x='Año',
        y='Valor',
        title=f'{Variable} - {estacion}',
        labels={'Año': ' ', 'Valor': 'T(ºC)'},
        markers=True
    )
    fig.update_layout(title_x=0.5, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Ez dago daturik aukeratutako irizpideekin.")
