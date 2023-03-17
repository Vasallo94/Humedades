# ------------------------- LIBRERÍAS ------------------------- #
import streamlit as st
import pandas as pd
import plotly_express as px

# ---------------------- CONFIGURACIÓN DE LA PÁGINA ---------------------- #
st.set_page_config(page_title="Humedades", layout="wide", page_icon="💦")
st.set_option("deprecation.showPyplotGlobalUse", False)

st.title("Humedades")
st.markdown("<center><h2><l style='color:white; font-size: 30px;'>Primeros acercamientos al problema de humedades que tengo en mi casa. En desarrollo...</h2></center>",
            unsafe_allow_html=True)

# ---------------------- IMPORTACIÓN DE LOS DATAFRAME ---------------------- #
df_habitacion = pd.read_csv("data/Habitacion_export_202303131817.csv")
df_salon = pd.read_csv("data/Salon_export_202303131824.csv")

# Concatenar los dataframes en uno solo con Multiíndice
df = pd.concat([df_habitacion, df_salon], keys=["habitación", "salón"], names=["ubicación"])
df = df.reorder_levels([1, 0]).sort_index()

# ---------------------- SIDEBAR ---------------------- #
st.sidebar.title("MENÚ")
ubicaciones_disponibles = ["habitación", "salón"]
ubicaciones_predeterminadas = st.sidebar.multiselect("Selecciona la ubicación", ubicaciones_disponibles)

# Verificar que los valores predeterminados estén en la lista de opciones
ubicaciones_validas = [ubicacion for ubicacion in ubicaciones_predeterminadas if ubicacion in ubicaciones_disponibles]

# ---------------------- PLOT Y VISUALIZACIÓN ---------------------- #
if ubicaciones_validas:
    df_seleccionado = df.loc[df.index.get_level_values("ubicación").isin(ubicaciones_predeterminadas)]

    # Crear columnas para organizar la visualización
    col1, col2 = st.columns(2)

    # Gráfico de temperatura en la columna 1
    with col1:
        st.subheader("Temperatura (Celsius)")
        fig1 = px.line(x=df_seleccionado["Registro_temporal"], y=df_seleccionado["Temperatura_Celsius"])
        st.plotly_chart(fig1)

    # Gráfico de humedad relativa en la columna 2
    with col2:
        st.subheader("Humedad relativa (%)")
        fig2 = px.line(df_seleccionado, x=df_seleccionado["Registro_temporal"], y=df_seleccionado["Humedad_relativa[%]"])
        st.plotly_chart(fig2)

    # Gráfico de temperatura vs humedad relativa en la columna 1
    with col1:
        st.subheader("Temperatura vs Humedad relativa")
        fig3 = px.scatter(df_seleccionado, x="Temperatura_Celsius", y="Humedad_relativa[%]", color=df_seleccionado.index.get_level_values(0))
        st.plotly_chart(fig3)

    # Gráfico de densidad de temperatura en la columna 2
    with col2:
        st.subheader("Densidad de temperatura")
        fig4 = px.density_contour(df_habitacion, x="Temperatura_Celsius", y="Humedad_relativa[%]")
        st.plotly_chart(fig4)

else:
    st.warning("Por favor, selecciona al menos una ubicación")