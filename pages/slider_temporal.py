import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df_habitacion = pd.read_csv("data/Habitacion_export_202303182309.csv")
df_salon = pd.read_csv("data/Salon_export_202303182309.csv")

# Concatenate the dataframes with a multi-index
df = pd.concat([df_habitacion, df_salon], keys=[
               "Habitación", "Salón"], names=["Ubicación"])
df = df.reorder_levels([1, 0]).sort_index()

# --------------------SIDEBAR----------------------------#
# Display the sidebar for selecting locations and time sampling
ubicaciones_disponibles = ["Habitación", "Salón"]
opciones_sampling = ['1min', '15min', '30min', '1h',
                     '3h', '6h', '12h', '1d', '1w', '1M']
ubicaciones_predeterminadas = st.sidebar.multiselect(
    "Selecciona la ubicación", ubicaciones_disponibles, default=["Habitación"])
sampling_predeterminado = st.sidebar.selectbox(
    'Selecciona el muestreo de tiempo', opciones_sampling, index=0)

ubicaciones_validas = [
    ubicacion for ubicacion in ubicaciones_predeterminadas if ubicacion in ubicaciones_disponibles]

if ubicaciones_validas:
    df_seleccionado = df.loc[df.index.get_level_values(
        "Ubicación").isin(ubicaciones_predeterminadas)]

    # Reset the index to convert the MultiIndex to a DataFrame
    df_seleccionado = df_seleccionado.reset_index()

    # Convert the Registro_temporal column to a datetime object
    df_seleccionado["Registro_temporal"] = pd.to_datetime(
        df_seleccionado["Registro_temporal"])

    # Set the Registro_temporal column as the index
    df_seleccionado = df_seleccionado.set_index("Registro_temporal")

    # Apply resampling to the data based on the selected time sampling by doing the mean of the values.
    df_seleccionado = df_seleccionado.resample(sampling_predeterminado).mean()

    # Add a column with location labels for coloring the lines
    df_seleccionado["Ubicación"] = [
        ubicacion for ubicacion in ubicaciones_predeterminadas if ubicacion in ubicaciones_disponibles] * len(df_seleccionado)

    st.title(
        'De momento solo admite una ubicación, no se pueden comparar ambas zonas de la casa.')
    # Line chart for temperature over time
    fig1 = px.line(df_seleccionado, x=df_seleccionado.index,
                   y="Temperatura_Celsius", color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={"Temperatura_Celsius": "Temperatura (Celsius)", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig1.update_layout(title="Temperatura",
                       yaxis_title="Temperatura (Celsius)")
    st.plotly_chart(fig1, use_container_width=True)

    # Line chart for humidity over time
    fig2 = px.line(df_seleccionado, x=df_seleccionado.index,
                   y="Humedad_relativa[%]", color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={"Humedad_relativa[%]": "Humedad relativa (%)", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig2.update_layout(title="Humedad",
                       yaxis_title="Humedad relativa (%)")
    st.plotly_chart(fig2, use_container_width=True)

    # Line chart for temperature and humidity over time, grouped by location
    fig3 = px.line(df_seleccionado, x=df_seleccionado.index, y=[
                   "Temperatura_Celsius", "Humedad_relativa[%]"], color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={"value": "Valor", "variable": "Variable", "Registro_temporal": "Tiempo", "Ubicación": "Ubicación"})
    fig3.update_layout(title="Temperatura y Humedad",
                       yaxis_title="Valor")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.scatter(df_seleccionado, x="Temperatura_Celsius", y="Humedad_relativa[%]", marginal_x="histogram", marginal_y="box", color="Ubicación", color_discrete_map={"Habitación": "#3DDEE0", "Salón": "#E07B3D"}, labels={
                      "Temperatura_Celsius": "Temperatura (Celsius)", "Humedad_relativa[%]": "Humedad relativa (%)", "Ubicación": "Ubicación"})
    fig4.update_layout(title="Relación entre temperatura y humedad",
                       xaxis_title="Temperatura (Celsius)", yaxis_title="Humedad relativa (%)")
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning(
        "Por favor, seleccione una ubicación válida para mostrar los gráficos")

st.dataframe(df_seleccionado)
