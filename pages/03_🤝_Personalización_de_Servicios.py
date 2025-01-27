import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la página
st.title("🤝 Personalizacion de Servicios y Retencion de Clientes")

# Carga de datos
df_acc_por_tecnologia = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_acc_por_tecnologia.csv")
df_acc_por_rangos = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_acc_por_rangos.csv")
df_dial_baf = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_dial_baf.csv")
df_totales_dial_baf = pd.read_csv(r"C:\Users\juanv\Documents\PIDA\Datasets\df_totales_dial_baf.csv")

# Conversión de tipos
for df in [df_acc_por_tecnologia, df_acc_por_rangos, df_dial_baf, df_totales_dial_baf]:
    df["Año"] = pd.to_numeric(df["Año"], errors="coerce")
    df["Trimestre"] = pd.to_numeric(df["Trimestre"], errors="coerce")

# Sidebar para filtros
st.sidebar.title("Filtros")
provincias = st.sidebar.multiselect(
    "Selecciona Provincias",
    options=df_acc_por_rangos["Provincia"].unique(),
    default=df_acc_por_rangos["Provincia"].unique()
)
año = st.sidebar.selectbox(
    "Selecciona un Año",
    options=df_acc_por_rangos["Año"].unique(),
    index=0
)

# Filtro aplicado a los DataFrames
df_acc_por_rangos_filtered = df_acc_por_rangos[
    (df_acc_por_rangos["Provincia"].isin(provincias)) & 
    (df_acc_por_rangos["Año"] == año)
]
df_acc_por_tecnologia_filtered = df_acc_por_tecnologia[
    df_acc_por_tecnologia["Provincia"].isin(provincias)
]

# KPIs
col1, col2 = st.columns(2)

with col1:
    tasa_adopcion_fibra = (
        (df_acc_por_tecnologia_filtered["Fibra óptica"].sum() / 
         df_acc_por_tecnologia_filtered["Total"].sum()) * 100
    )
    st.metric("Tasa de Adopción de Fibra Óptica", f"{tasa_adopcion_fibra:.2f} %")

with col2:
    tecnologias_antiguas = (
        (df_dial_baf["Dial up"].sum() + df_acc_por_tecnologia_filtered["ADSL"].sum()) /
        (df_dial_baf["Total"].sum() + df_acc_por_tecnologia_filtered["Total"].sum()) * 100
    )
    st.metric("Usuarios con Tecnologías Antiguas", f"{tecnologias_antiguas:.2f} %")

# Gráfico 1: Proporción de Accesos por Rangos de Velocidad
if not df_acc_por_rangos_filtered.empty:
    df_rangos_totales = df_acc_por_rangos_filtered.iloc[:, 4:-1].sum()
    df_rangos_totales = pd.DataFrame({
        "Rango de Velocidad": df_rangos_totales.index,
        "Accesos": df_rangos_totales.values
    }).sort_values(by="Accesos", ascending=False)

    fig1 = px.bar(
        df_rangos_totales,
        x="Accesos",
        y="Rango de Velocidad",
        orientation="h",
        title="Proporción de Accesos por Rangos de Velocidad",
        labels={"Accesos": "Número de Accesos", "Rango de Velocidad": "Rango de Velocidad"},
        text="Accesos"
    )
    fig1.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig1.update_layout(yaxis=dict(title=None), xaxis=dict(title="Número de Accesos"))
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Evolución Temporal de Accesos por Velocidad
if not df_acc_por_rangos.empty:
    # Filtrar por provincia seleccionada
    df_evolucion = df_acc_por_rangos[df_acc_por_rangos["Provincia"].isin(provincias)]
    
    # Agrupar por año y sumar los accesos para cada rango de velocidad
    df_evolucion = df_evolucion.groupby(["Año"]).sum().reset_index()
    
    # Asegurarse de que las columnas de rangos de velocidad sean numéricas
    for col in df_evolucion.columns[1:]:
        df_evolucion[col] = pd.to_numeric(df_evolucion[col], errors="coerce").fillna(0)
    
    # Convertir a formato largo para Plotly Express
    df_evolucion_melted = df_evolucion.melt(
        id_vars=["Año"],
        value_vars=df_evolucion.columns[1:],
        var_name="Rango de Velocidad",
        value_name="Accesos"
    )
    
    # Crear el gráfico de líneas
    fig2 = px.line(
        df_evolucion_melted,
        x="Año",
        y="Accesos",
        color="Rango de Velocidad",
        title="Evolución Temporal de Accesos por Velocidad",
        labels={"Accesos": "Número de Accesos", "Año": "Año", "Rango de Velocidad": "Velocidad"}
    )
    fig2.update_traces(mode="lines+markers")
    fig2.update_layout(
        xaxis=dict(title="Año"),
        yaxis=dict(title="Número de Accesos"),
        legend_title="Rangos de Velocidad"
    )
    st.plotly_chart(fig2, use_container_width=True)


# Gráfico 3: Proporción de Tecnologías por Provincia
if not df_acc_por_tecnologia.empty:
    # Filtrar por provincia seleccionada
    df_tecnologias = df_acc_por_tecnologia[df_acc_por_tecnologia["Provincia"].isin(provincias)]

    # Calcular proporciones
    tecnologias_cols = ["ADSL", "Cablemodem", "Fibra óptica", "Wireless", "Otros"]  # Solo las columnas de tecnologías
    df_tecnologias["Total"] = df_tecnologias[tecnologias_cols].sum(axis=1)
    for col in tecnologias_cols:
        df_tecnologias[col] = (df_tecnologias[col] / df_tecnologias["Total"]) * 100

    # Promedio por provincia
    df_tecnologias_avg = df_tecnologias.groupby("Provincia")[tecnologias_cols].mean().reset_index()

    # Transformar a formato largo
    df_tecnologias_melted = df_tecnologias_avg.melt(
        id_vars=["Provincia"],
        value_vars=tecnologias_cols,  # Solo las columnas de tecnologías
        var_name="Tecnología",
        value_name="Proporción (%)"
    )

    # Crear el gráfico de barras apiladas
    fig3 = px.bar(
        df_tecnologias_melted,
        x="Provincia",
        y="Proporción (%)",
        color="Tecnología",
        title="Proporción de Accesos por Tecnología en Cada Provincia",
        labels={"Proporción (%)": "Proporción (%)", "Provincia": "Provincia", "Tecnología": "Tecnología"}
    )
    fig3.update_layout(
        xaxis=dict(title="Provincia"),
        yaxis=dict(title="Proporción (%)"),
        legend_title="Tecnología",
        barmode="stack"  # Barras apiladas
    )
    st.plotly_chart(fig3, use_container_width=True)
