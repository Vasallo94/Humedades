import pandas as pd
import plotly.express as px
import streamlit as st


def load_dataframes():
    try:
        df_habitacion = pd.read_csv("data/Habitacion_export_202303182309.csv")
        df_salon = pd.read_csv("data/Salon_export_202303182309.csv")
    except FileNotFoundError:
        st.warning("No se encontraron los archivos CSV. Por favor, asegúrate de que estén en la carpeta 'data' y con los nombres correctos.")
        st.stop()
    df_habitacion['ubicacion'] = 'Habitación'
    df_salon['ubicacion'] = 'Salón'
    return pd.merge(df_habitacion, df_salon, how='outer')

def create_chart(df, x, y, chart_type, title, yaxis_title, xaxis_title=None, height=500, **kwargs):
    fig = chart_type(df, x=x, y=y, **kwargs)
    fig.update_layout(title=title, yaxis_title=yaxis_title, xaxis_title=xaxis_title)
    st.plotly_chart(fig, use_container_width=True, height=height)

def load_data():
    df_habitacion = pd.read_csv("data/Habitacion_export_202303182309.csv")
    df_salon = pd.read_csv("data/Salon_export_202303182309.csv")
    df_habitacion['ubicacion'] = 'Habitación'
    df_salon['ubicacion'] = 'Salón'
    df = pd.merge(df_habitacion, df_salon, how='outer')
    df = df.index.name = "Ubicación"
    return df

def create_sidebar(ubicaciones_disponibles, opciones_sampling):
    ubicaciones_predeterminadas = st.sidebar.multiselect("Selecciona la ubicación", ubicaciones_disponibles, default=["Habitación"])
    sampling_predeterminado = st.sidebar.selectbox('Selecciona el muestreo de tiempo', opciones_sampling, index=0)
    return ubicaciones_predeterminadas, sampling_predeterminado

# def filter_data(df, ubicaciones_predeterminadas, sampling_predeterminado):
#     df_seleccionado = df.loc[df.index.get_level_values("ubicacion").isin(ubicaciones_predeterminadas)]
#     #df_seleccionado = df_seleccionado.reset_index(level=1)
#     #df_seleccionado["Ubicación"] = df_seleccionado["Ubicación"].apply(lambda x: x[1])
#     df_seleccionado["Registro_temporal"] = pd.to_datetime(df_seleccionado["Registro_temporal"])
#     df_seleccionado = df_seleccionado.set_index("Registro_temporal")
#     df_seleccionado = df_seleccionado.resample(sampling_predeterminado).mean()
#     return df_seleccionado

def filter_data(df, ubicaciones_predeterminadas, sampling_predeterminado):
    df_seleccionado = df.loc[df.index.get_level_values("Ubicación").isin(ubicaciones_predeterminadas)]
    df_seleccionado["Registro_temporal"] = pd.to_datetime(df_seleccionado["Registro_temporal"])
    df_seleccionado = df_seleccionado.set_index("Registro_temporal")
    df_seleccionado = df_seleccionado.resample(sampling_predeterminado).mean()
    return df_seleccionado

def create_plotly_charts(df_seleccionado):
    # Line chart for temperature over time
    figs = []
    fig1 = px.line(df_seleccionado, x=df_seleccionado.index, y="Temperatura_Celsius", color="Ubicación",
                   color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"},
                   labels={"Temperatura_Celsius": "Temperatura (Celsius)", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig1.update_layout(title="Temperatura", yaxis_title="Temperatura (Celsius)")
    figs.append(fig1)

    # Line chart for humidity over time
    fig2 = px.line(df_seleccionado, x=df_seleccionado.index, y="Humedad_relativa[%]", color="ubicacion",
                   color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"},
                   labels={"Humedad_relativa[%]": "Humedad relativa (%)", "Registro_temporal": "Tiempo", "ubicacion": "Ubicación"})
    fig2.update_layout(title="Humedad", yaxis_title="Humedad relativa (%)")
    figs.append(fig2)
    return figs
