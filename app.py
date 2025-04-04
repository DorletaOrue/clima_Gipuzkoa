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

# Set sidebar width
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 400px;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 400px;
        }
    </style>
""", unsafe_allow_html=True)



st.set_page_config(page_title='Dashboard',layout='wide')
st.title('Clima Gipuzkoan')

st.sidebar.title('Estazioa')


#load data
Estaciones=pd.read_excel('Estaciones_temperatura.xlsx',sheet_name='Hoja4')

#Create the chart
variables=Estaciones['Variable'].unique()
variable=st.sidebar.selectbox('Aldagaia',variables)

estaciones = Estaciones['Estación'].unique()
estacion=st.sidebar.selectbox('Estazioa',estaciones)

# Filter data
filtered_data = Estaciones[(Estaciones['Estación'] == estacion) & (Estaciones['Variable'] == variable)]

# Create the chart
fig, ax = plt.subplots()
ax.plot(filtered_data['Año'], filtered_data['Valor'], color='red')
ax.set_title(f'{variable} - {estacion}')
ax.set_xlabel('Fecha')
ax.set_ylabel('Balioa')

# Save the plot to a buffer
buf = BytesIO()
fig.savefig(buf, format="png")
buf.seek(0)

# Show plot in the sidebar as an image
st.sidebar.image(buf, caption="Grafikoa",  use_container_width=True)
