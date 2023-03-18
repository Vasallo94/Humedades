# --------------------LIBRARIES----------------------------#
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly_express as px
import plotly.graph_objects as go


# --------------------PAGE CONFIGURATION----------------------------#
# layout="centered" or "wide"
st.set_page_config(page_title="Humedades", layout="wide", page_icon="💦")
st.set_option("deprecation.showPyplotGlobalUse", False)

# --------------------LOAD DATAFRAMES----------------------------#
# Load CSV files for temperature and humidity data from two sensors in the house
try:
    df_habitacion = pd.read_csv("data/Habitacion_export_202303131817.csv")
    df_salon = pd.read_csv("data/Salon_export_202303131824.csv")
except FileNotFoundError:
    st.warning("No se encontraron los archivos CSV. Por favor, asegúrate de que estén en la carpeta 'data' y con los nombres correctos.")
    st.stop()

# Concatenate the dataframes with a multi-index
df = pd.concat([df_habitacion, df_salon], keys=["Habitación", "Salón"], names=["Ubicación"])
df = df.reorder_levels([1, 0]).sort_index()

# --------------------SIDEBAR----------------------------#
# Display the sidebar for selecting locations
ubicaciones_disponibles = ["Habitación", "Salón"]
ubicaciones_predeterminadas = st.sidebar.multiselect("Selecciona la ubicación", ubicaciones_disponibles)
ubicaciones_validas = [ubicacion for ubicacion in ubicaciones_predeterminadas if ubicacion in ubicaciones_disponibles]

# --------------------DATA VISUALIZATION----------------------------#
# Show charts for selected locations
if ubicaciones_validas:
    df_seleccionado = df.loc[df.index.get_level_values("Ubicación").isin(ubicaciones_predeterminadas)]

    # Line chart for temperature over time
    fig1 = px.line(x=df_seleccionado["Registro_temporal"], y=df_seleccionado["Temperatura_Celsius"])
    st.plotly_chart(fig1, use_container_width=True)

    # Line chart for humidity over time
    fig2 = px.line(df_seleccionado, x=df_seleccionado["Registro_temporal"], y=df_seleccionado["Humedad_relativa[%]"])
    st.plotly_chart(fig2, use_container_width=True)

    # Line chart for temperature and humidity over time, grouped by location
    fig3 = px.line(df_seleccionado, x="Registro_temporal", y=["Temperatura_Celsius", "Humedad_relativa[%]"], color=df_seleccionado.index.get_level_values(0))
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("Por favor, selecciona al menos una ubicación.")
