import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Calidad del Servicio", layout="wide")

st.title("Calidad del Servicio")

# Carga de datos
df_acc_vel_loc = pd.read_csv("Datasets/df_acc_vel_loc_sinrangos.csv")
df_velocidad_sinrangos = pd.read_csv("Datasets/df_velocidad_sin_rangos.csv")
df_velocidad_porcentaje = pd.read_csv("Datasets/df_velocidad_porciento_prov.csv")

# Filtros
provincia = st.selectbox("Selecciona una provincia", options=df_acc_vel_loc["Provincia"].unique())
año = st.slider("Selecciona el año", min_value=int(df_velocidad_sinrangos["Año"].min()), max_value=int(df_velocidad_sinrangos["Año"].max()), step=1)

# Filtrado de datos
df_filtrado_acc = df_acc_vel_loc[df_acc_vel_loc["Provincia"] == provincia]
df_filtrado_vel = df_velocidad_sinrangos[(df_velocidad_sinrangos["Provincia"] == provincia) & (df_velocidad_sinrangos["Año"] == año)]

# Visualizaciones
st.subheader(f"Distribución de Accesos en {provincia}")
fig_acc = px.bar(df_filtrado_acc, x="Localidad", y="Accesos", color="Velocidad (Mbps)", title="Accesos por localidad")
st.plotly_chart(fig_acc, use_container_width=True)

st.subheader(f"Velocidades promedio en {provincia} - {año}")
fig_vel = px.line(df_filtrado_vel, x="Trimestre", y="Velocidad", title="Evolución de la velocidad")
st.plotly_chart(fig_vel, use_container_width=True)
