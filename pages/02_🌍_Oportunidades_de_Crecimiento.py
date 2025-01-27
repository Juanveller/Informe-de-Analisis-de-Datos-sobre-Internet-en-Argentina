import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="🌍 Oportunidades de Crecimiento y Expansión", layout="wide")

# Título de la página
st.title("🌍 Oportunidades de Crecimiento y Expansión")

# Cargar los datos
df_accesos_tecnologia_localidad = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_accesos_tecnologia_localidad.csv")
df_penetracion_hogares = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_penetracion_hogares.csv")
df_penetracion_poblacion = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_penetracion_poblacion.csv")
df_penetracion_totales = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_penetracion_totales.csv")
df_totales_acc_por_tecnologia = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_totales_acc_por_tecnologia.csv")

# Limpieza básica
df_penetracion_hogares["Año"] = pd.to_numeric(df_penetracion_hogares["Año"], errors="coerce")
df_penetracion_poblacion["Año"] = pd.to_numeric(df_penetracion_poblacion["Año"], errors="coerce")
df_penetracion_totales["Año"] = pd.to_numeric(df_penetracion_totales["Año"], errors="coerce")

# Sidebar con filtros
st.sidebar.title("Filtros")
provincias = st.sidebar.multiselect(
    "Selecciona las provincias",
    options=df_penetracion_hogares["Provincia"].unique(),
    default=df_penetracion_hogares["Provincia"].unique(),
)

años = st.sidebar.slider(
    "Selecciona el rango de años",
    int(df_penetracion_hogares["Año"].min()),
    int(df_penetracion_hogares["Año"].max()),
    (int(df_penetracion_hogares["Año"].min()), int(df_penetracion_hogares["Año"].max()))
)

# Filtrar los datos según los filtros seleccionados
df_hogares_filtrado = df_penetracion_hogares[
    (df_penetracion_hogares["Provincia"].isin(provincias)) & 
    (df_penetracion_hogares["Año"].between(*años))
]

df_poblacion_filtrado = df_penetracion_poblacion[
    (df_penetracion_poblacion["Provincia"].isin(provincias)) & 
    (df_penetracion_poblacion["Año"].between(*años))
]

# KPIs (Afectados por filtros)
penetracion_prom_hogares = df_hogares_filtrado["Accesos por cada 100 hogares"].mean()
penetracion_prom_poblacion = df_poblacion_filtrado["Accesos por cada 100 hab"].mean()
penetracion_total_estimada = df_hogares_filtrado["Accesos por cada 100 hogares"].sum()

# Mostrar KPIs
st.metric("Penetración Promedio en Hogares", f"{penetracion_prom_hogares:.2f} accesos")
st.metric("Penetración Promedio en Población", f"{penetracion_prom_poblacion:.2f} accesos")
st.metric("Cobertura Total Estimada", f"{penetracion_total_estimada:.0f} accesos")

# Gráfico 1: Distribución por provincia (hogares) con filtro de años
st.subheader("Distribución de Accesos por Provincia (Hogares)")
fig1 = px.box(
    df_hogares_filtrado,  # Ahora filtrado también por años
    x="Provincia",
    y="Accesos por cada 100 hogares",
    color="Provincia",
    points="all",
    title="Distribución de Accesos por cada 100 Hogares"
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Evolución de la penetración de hogares por año
st.subheader("Evolución de la Penetración por Hogares")
df_hogares_median = df_hogares_filtrado.groupby(["Año", "Provincia"])["Accesos por cada 100 hogares"].median().reset_index()
fig2 = px.line(
    df_hogares_median,
    x="Año",
    y="Accesos por cada 100 hogares",
    color="Provincia",
    title="Evolución de la Penetración por Hogares (Mediana)",
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Evolución de la penetración por población
st.subheader("Evolución de la Penetración por Población")
df_poblacion_median = df_poblacion_filtrado.groupby(["Año", "Provincia"])["Accesos por cada 100 hab"].median().reset_index()
fig3 = px.line(
    df_poblacion_median,
    x="Año",
    y="Accesos por cada 100 hab",
    color="Provincia",
    title="Evolución de la Penetración por Población (Mediana)",
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)


