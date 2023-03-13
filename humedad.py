# --------------------LIBRERÍAS----------------------------#
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly_express as px
import plotly.graph_objects as go


# --------------------CONFIGURACIÓN DE LA PÁGINA----------------------------#
# layout="centered" or "wide"
st.set_page_config(page_title="Humedades", layout="wide", page_icon="💦")
st.set_option("deprecation.showPyplotGlobalUse", False)

st.title("Humedades")

# --------------------IMPORTACIÓN DE LOS DATAFRAME----------------------------#
df_habitacion = pd.read_csv("data/Habitación_export_202303131817.csv")
df_salon = pd.read_csv("data/Salón_export_202303131824.csv")

# Renombrar la columna "Registro temporal para frecuencia de muestreo cada 1 min min" a "registro temporal"
# df_salon = df_salon.rename(
#     columns={
#         "Registro temporal para frecuencia de muestreo cada 1 min": "registro temporal"
#     }
# )
# df_habitacion = df_habitacion.rename(
#     columns={
#         "Registro temporal para frecuencia de muestreo cada 1 min": "registro temporal"
#     }
# )
# ! no entiendo por qué no funciona la mierda del rename...

# Concatenar los dataframes en uno solo con Multiíndice
df = pd.concat(
    [df_habitacion, df_salon], keys=["habitación", "salón"], names=["ubicación"]
)
df = df.reorder_levels([1, 0]).sort_index()
# opciones para la selección de ubicaciones
ubicaciones_disponibles = ["habitación", "salón"]
# valores predeterminados para la selección de ubicaciones
ubicaciones_predeterminadas = st.sidebar.multiselect(
    "Selecciona ubicaciones", ubicaciones_disponibles
)
st.dataframe(df)
# verificar que los valores predeterminados estén en la lista de opciones
ubicaciones_validas = [
    ubicacion
    for ubicacion in ubicaciones_predeterminadas
    if ubicacion in ubicaciones_disponibles
]

# mostrar la selección de ubicaciones válidas y plotear con la decisión
if ubicaciones_validas:
    df_seleccionado = df.loc[
        df.index.get_level_values("ubicación").isin(ubicaciones_predeterminadas)
    ]
    fig1 = px.line(
        x=df_seleccionado["Registro_temporal"],
        y=df_seleccionado["Temperatura_Celsius"],
    )
    st.plotly_chart(fig1)

    fig2 = px.line(
        df_seleccionado,
        x=df_seleccionado["Registro_temporal"],
        y=df_seleccionado["Humedad_relativa[%]"],
    )
    st.plotly_chart(fig2)
    # fig3 = px.line(
    #     df_seleccionado,
    #     x="Registro_temporal",
    #     y=["Temperatura_Celsius", "Humedad_relativa[%]"],
    #     color=df_seleccionado.index.get_level_values(0),
    # )
    # # Mostrar gráfico en Streamlit
    # st.plotly_chart(fig3)
else:
    st.warning("Por favor, selecciona al menos una ubicación.")

# --------------------SIDEBAR----------------------------#
# st.sidebar.image("img/logo.png", width=150)
st.sidebar.title("MENÚ")
st.sidebar.subheader("")
st.sidebar.write("")
