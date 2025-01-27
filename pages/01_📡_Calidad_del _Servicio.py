import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la página
st.title("📡 Calidad del Servicio")

# **1. Cargar datos**
df_velocidad_sinrangos = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_velocidad_sinrangos.csv")
df_velocidad_sinrangos["Provincia"] = df_velocidad_sinrangos["Provincia"].str.strip()
df_velocidad_sinrangos["Año"] = pd.to_numeric(df_velocidad_sinrangos["Año"], errors="coerce")
df_velocidad_sinrangos["Velocidad"] = pd.to_numeric(df_velocidad_sinrangos["Velocidad"], errors="coerce")

# **2. Filtros en el sidebar**
st.sidebar.header("Filtros")
año = st.sidebar.slider(
    "Selecciona el año",
    min_value=int(df_velocidad_sinrangos["Año"].min(skipna=True)),
    max_value=int(df_velocidad_sinrangos["Año"].max(skipna=True)),
    step=1,
    key="slider_año"
)

provincia = st.sidebar.multiselect(
    "Selecciona las provincias",
    options=df_velocidad_sinrangos["Provincia"].unique(),
    default=df_velocidad_sinrangos["Provincia"].unique()
)

# **3. Filtrar los datos según los filtros seleccionados**
df_filtrado = df_velocidad_sinrangos[
    (df_velocidad_sinrangos["Año"] == año) &
    (df_velocidad_sinrangos["Provincia"].isin(provincia))
]

# **4. KPIs**
st.header("📊 Indicadores Clave de Desempeño (KPIs)")
col1, col2, col3 = st.columns(3)

# KPI: Velocidad promedio
vel_min = df_filtrado["Velocidad"].min()
col1.metric("Velocidad Minima (Mbps)", f"{vel_min:.2f}")

# KPI: Velocidad mediana
vel_mediana = df_filtrado["Velocidad"].median()
col2.metric("Velocidad Media (Mbps)", f"{vel_mediana:.2f}")

# KPI: Percentil 75
vel_percentil_75 = df_filtrado["Velocidad"].quantile(0.75)
col3.metric("Velocidad Alta (P75, Mbps)", f"{vel_percentil_75:.2f}")

# **5. Gráficos relevantes**
st.header("📈 Análisis Visual")

# **Boxplot: Distribución de velocidades**
st.subheader("Distribución de Velocidad por Provincia")
fig1 = px.box(
    df_filtrado,
    x="Provincia",
    y="Velocidad",
    color="Provincia",
    points="all",  # Muestra outliers
    title="Distribución de Velocidad por Provincia"
)
st.plotly_chart(fig1, use_container_width=True)

# **Línea: Evolución de la mediana de velocidad**
st.subheader("Evolución de la Velocidad Media (Mediana)")
df_median_all = df_velocidad_sinrangos.groupby(["Año", "Provincia"]).median(numeric_only=True).reset_index()
# Filtro solo por provincia
df_median_filtered = df_median_all[df_median_all["Provincia"].isin(provincia)]

# Crear el gráfico interactivo
fig2 = px.line(
        df_median_filtered,
        x="Año",
        y="Velocidad",
        color="Provincia",
        markers=True,  # Mostrar puntos para facilitar interpretación
        title="Evolución de la Mediana de Velocidad por Provincia"
)
st.plotly_chart(fig2, use_container_width=True)