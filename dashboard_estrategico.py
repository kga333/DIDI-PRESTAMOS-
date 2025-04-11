
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Estratégico", layout="wide")

st.title("📊 Dashboard Estratégico de Cobranza")

# Cargar datos
uploaded_file = st.file_uploader("Sube el archivo Excel de pagos", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.success("Archivo cargado correctamente.")

    # KPIs básicos
    total_prometido = df["MONTO PROMETIDO"].sum() if "MONTO PROMETIDO" in df.columns else 0
    total_pagado = df["MONTO PAGADO"].sum() if "MONTO PAGADO" in df.columns else 0
    tasa_cumplimiento = (total_pagado / total_prometido) * 100 if total_prometido > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Monto Prometido", f"${total_prometido:,.2f}")
    col2.metric("✅ Monto Pagado", f"${total_pagado:,.2f}")
    col3.metric("📈 Tasa de Cumplimiento", f"{tasa_cumplimiento:.2f}%")

    # Tabla
    st.subheader("📋 Tabla de Datos")
    st.dataframe(df)

    # Gráfico
    if "AGENTE" in df.columns and "MONTO PAGADO" in df.columns:
        graf = df.groupby("AGENTE")["MONTO PAGADO"].sum().reset_index()
        fig = px.bar(graf, x="AGENTE", y="MONTO PAGADO", title="Monto Pagado por Agente")
        st.plotly_chart(fig, use_container_width=True)
