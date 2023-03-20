import streamlit as st
import pandas as pd
import plotly_express as px
from utils.funciones_varias import *

st.set_page_config(page_title="Humedades", layout="wide", page_icon="💦")
st.set_option("deprecation.showPyplotGlobalUse", False)

df = load_dataframes()
ubicaciones_predeterminadas = st.sidebar.multiselect("Selecciona la ubicación", ["Habitación", "Salón"], default=["Habitación", "Salón"])
df_seleccionado = df[df["Ubicación"].isin(ubicaciones_predeterminadas)]

if df_seleccionado.empty:
    st.warning("No hay ubicaciones seleccionadas")
    st.info("Por favor, selecciona una opción de la barra lateral.")
else:
    chart_config = {
        "color": "Ubicación",
        "color_discrete_map": {"Habitación": "#3DDEE0", "Salón": "#E07B3D"},
    }
    create_chart(df_seleccionado, "Registro_temporal", "Temperatura_Celsius", px.line, "Temperatura", "Temperatura (Celsius)", **chart_config)
    create_chart(df_seleccionado, "Registro_temporal", "Humedad_relativa[%]", px.line, "Humedad", "Humedad relativa (%)", **chart_config)
    create_chart(df_seleccionado, "Registro_temporal", ["Humedad_relativa[%]", "Temperatura_Celsius"], px.line, "Humedad y temperatura", "Humedad y temperatura", **chart_config)
    create_chart(df_seleccionado, "Humedad_relativa[%]", "Temperatura_Celsius", px.scatter, "Humedad y temperatura (dispersión)", "Temperatura (Celsius)", "Humedad relativa", marginal_y="histogram", marginal_x="histogram", trendline="ols", trendline_color_override="darkseagreen", **chart_config)
    create_chart(df_seleccionado, "Registro_temporal", ["Humedad_relativa[%]", "Temperatura_Celsius"], px.line, "Humedad y temperatura por ubicación", "Humedad y temperatura", "Tiempo", height=700, facet_col="Ubicación", **chart_config)
