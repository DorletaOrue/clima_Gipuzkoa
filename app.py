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
ax.plot(filtered_data['Año'], filtered_data['Valor'], color='red')
ax.set_title(f'{variable} - {estacion}')
ax.set_xlabel('Fecha')
ax.set_ylabel('Balioa')

# Show plot in Streamlit
st.pyplot(fig)

# Layout with two columns: Plot on the left
left_col, right_col = st.columns([1, 3])  # You can adjust 1:3 to 1:2 or 2:3, etc.

with left_col:
    st.write("### Grafikoa")
    st.pyplot(fig)

with right_col:
    st.write("### Beste edukia")  # Optional: leave empty or add other content
