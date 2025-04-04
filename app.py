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
ax.plot([1, 2, 3], [4, 5, 6])
ax.plot(filtered_data['Año'], filtered_data['Valor'], color='red')
ax.set_title(f'{variable} - {estacion}')
ax.set_xlabel('Fecha')
ax.set_ylabel('Balioa')


# Layout: two columns to simulate left/right (sidebar + plot look)
st.markdown("---")  # horizontal rule for spacing

left_col, _ = st.columns([1, 3])  # Only use the left column

with left_col:
    st.pyplot(fig)
