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
    df_habitacion = pd.read_csv("data/Habitacion_export_202303182309.csv")
    df_salon = pd.read_csv("data/Salon_export_202303182309.csv")
except FileNotFoundError:
    st.warning("No se encontraron los archivos CSV. Por favor, asegúrate de que estén en la carpeta 'data' y con los nombres correctos.")
    st.stop()

# Concatenate the dataframes with a multi-index
df = pd.concat([df_habitacion, df_salon], keys=[
               "Habitación", "Salón"], names=["Ubicación"])
df = df.reorder_levels([1, 0]).sort_index()

# --------------------SIDEBAR----------------------------#
# Display the sidebar for selecting locations
ubicaciones_disponibles = ["Habitación", "Salón"]
ubicaciones_predeterminadas = st.sidebar.multiselect(
    "Selecciona la ubicación", ubicaciones_disponibles, default=ubicaciones_disponibles)
ubicaciones_validas = [
    ubicacion for ubicacion in ubicaciones_predeterminadas if ubicacion in ubicaciones_disponibles]


if ubicaciones_validas:
    df_seleccionado = df.loc[df.index.get_level_values(
        "Ubicación").isin(ubicaciones_predeterminadas)]

    # Add a column with location labels for coloring the lines
    df_seleccionado["Ubicación"] = df_seleccionado.index.get_level_values(
        "Ubicación").map(lambda x: "Habitación" if x == "Habitación" else "Salón")

    # Line chart for temperature over time
    fig1 = px.line(df_seleccionado, x="Registro_temporal",
                   y="Temperatura_Celsius", color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={"Temperatura_Celsius": "Temperatura (Celsius)", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig1.update_layout(title="Temperatura",
                       yaxis_title="Temperatura (Celsius)")
    st.plotly_chart(fig1, use_container_width=True)

    # Line chart for humidity over time
    fig2 = px.line(df_seleccionado, x="Registro_temporal",
                   y="Humedad_relativa[%]", color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={"Humedad_relativa[%]": "Humedad relativa (%)", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig2.update_layout(title="Humedad",
                       yaxis_title="Humedad relativa (%)")
    st.plotly_chart(fig2, use_container_width=True)

    # Line chart for temperature and humidity over time, grouped by location
    fig3 = px.line(df_seleccionado, x="Registro_temporal", y=["Temperatura_Celsius", "Humedad_relativa[%]"], color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={
        "value": "Valor", "variable": "Variable", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig3.update_layout(
        title="Temperatura y humedad por ubicación", yaxis_title="Valor")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning(
        "Por favor, seleccione una ubicación válida para mostrar los gráficos")
