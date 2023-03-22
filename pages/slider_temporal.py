import streamlit as st
import pandas as pd
import plotly.express as px
from utils.funciones_varias import *


# Load data
df = load_data()


# Sidebar
ubicaciones_disponibles = ["Habitación", "Salón"]
opciones_sampling = ['1min', '15min', '30min', '1h', '3h', '6h', '12h', '1d', '1w', '1M']
ubicaciones_predeterminadas, sampling_predeterminado = create_sidebar(ubicaciones_disponibles, opciones_sampling)

# Filter data
df_seleccionado = filter_data(df, ubicaciones_predeterminadas, sampling_predeterminado)

# Create charts
figs = create_plotly_charts(df_seleccionado)

st.dataframe(df_seleccionado)
# Display charts
st.header("Gráficos de temperatura y humedad")
st.plotly_chart(figs[0], use_container_width=True)
st.plotly_chart(figs[1], use_container_width=True)



