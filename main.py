
import streamlit as st
import pandas as pd
import os
import sys

# Asegurar que el módulo utils se pueda importar
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))
from kpi_calculations import (
    productividad_por_agente,
    atraso_por_fila_y_estado,

    indicadores_nsr_rr,
    indicadores_lpr_acp,
    indicadores_dso_rr_sr,
    calcular_efectividad_por_agente,
    monto_prometido_vs_pagado,
    distribucion_estado_pago,
    monto_total_por_dia,
    cuentas_alto_riesgo
)

# Configuración general
st.set_page_config(page_title="Dashboard de Cobranza", layout="wide")
st.title("📊 Dashboard de Cobranza - KPIs Iniciales")

# Cargar datos
excel_path = os.path.join("data", "Historial_Pagos_Prestamos.xlsx")

@st.cache_data
def cargar_datos():
    return pd.read_excel(excel_path)

df = cargar_datos()
df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

# Mostrar columnas disponibles
st.subheader("🔍 Columnas encontradas en el archivo:")
st.write(df.columns.tolist())

# Vista general
st.subheader("📋 Vista general de los datos")
st.dataframe(df, use_container_width=True)

# KPI 1: Efectividad de Cobranza por Agente
st.subheader("✅ Efectividad de Cobranza por Agente")
efectividad = calcular_efectividad_por_agente(df)
if "Error" in efectividad.columns:
    st.error(f"❌ Error: {efectividad['Error'][0]}")
else:
    st.dataframe(efectividad, use_container_width=True)
    st.bar_chart(efectividad.set_index("AGENTE DE COBRANZA"))

# KPI 2: Monto Prometido vs Pagado por Estado del Pago
st.subheader("💰 Monto Prometido vs Pagado por Estado del Pago")
monto_cmp_total = monto_prometido_vs_pagado(df)
if "Error" in monto_cmp_total.columns:
    st.error(f"❌ Error: {monto_cmp_total['Error'][0]}")
else:
    st.dataframe(monto_cmp_total, use_container_width=True)

# KPI 3: Monto Total Recuperado por Día (Completo + Parcial)
st.subheader("📈 Monto Total Recuperado por Día")
fecha_min = df["FECHA"].min()
fecha_max = df["FECHA"].max()
fecha_ini, fecha_fin = st.date_input("📅 Rango para monto diario:", [fecha_min, fecha_max], key="filtro_monto_dia")
df_diario_filtrado = df[(df["FECHA"] >= pd.to_datetime(fecha_ini)) & (df["FECHA"] <= pd.to_datetime(fecha_fin))]
monto_diario = monto_total_por_dia(df_diario_filtrado)

if "Error" in monto_diario.columns:
    st.error(f"❌ Error: {monto_diario['Error'][0]}")
else:
    st.dataframe(monto_diario, use_container_width=True)
    st.line_chart(monto_diario.set_index("FECHA"))

# KPI 4: Cuentas de Alto Riesgo por Agente
st.subheader("🚨 Cuentas de Alto Riesgo por Agente")
alto_riesgo = cuentas_alto_riesgo(df)
if "Error" in alto_riesgo.columns:
    st.error(f"❌ Error: {alto_riesgo['Error'][0]}")
else:
    st.dataframe(alto_riesgo, use_container_width=True)
    st.bar_chart(alto_riesgo.set_index("AGENTE DE COBRANZA"))

# KPI 5: Distribución del Estado del Pago Prometido
st.subheader("📊 Distribución del Estado del Pago Prometido")
estado_pago = distribucion_estado_pago(df)
if "Error" in estado_pago.columns:
    st.error(f"❌ Error: {estado_pago['Error'][0]}")
else:
    estado_pago.columns = ["Estado", "% del Total"]
    st.dataframe(estado_pago, use_container_width=True)
    st.bar_chart(data=estado_pago.set_index("Estado"))

# KPI adicional: DSO, Recovery Rate y Settlement Rate
st.subheader("📉 DSO, Recovery Rate y Settlement Rate por Agente")
kpi_dso_rr_sr_df = indicadores_dso_rr_sr(df)

if "Error" in kpi_dso_rr_sr_df.columns:
    st.error(f"❌ Error: {kpi_dso_rr_sr_df['Error'][0]}")
else:
    st.dataframe(kpi_dso_rr_sr_df, use_container_width=True)
    st.bar_chart(kpi_dso_rr_sr_df.set_index("AGENTE DE COBRANZA")[["DSO", "RECOVERY RATE (%)", "SETTLEMENT RATE (%)"]])

# KPI adicional: LPR y ACP
st.subheader("⏱️ Late Payment Rate (LPR) y Average Collection Period (ACP)")
kpi_lpr_acp_df = indicadores_lpr_acp(df)

if "Error" in kpi_lpr_acp_df.columns:
    st.error(f"❌ Error: {kpi_lpr_acp_df['Error'][0]}")
else:
    st.dataframe(kpi_lpr_acp_df, use_container_width=True)
    st.bar_chart(kpi_lpr_acp_df.set_index("AGENTE DE COBRANZA")[["LPR (%)", "ACP"]])

# KPI adicional: Negotiation Success Rate y Rejection Rate
st.subheader("🤝 Negotiation Success Rate (NSR) y Rejection Rate (RR)")
kpi_nsr_rr_df = indicadores_nsr_rr(df)

if "Error" in kpi_nsr_rr_df.columns:
    st.error(f"❌ Error: {kpi_nsr_rr_df['Error'][0]}")
else:
    st.dataframe(kpi_nsr_rr_df, use_container_width=True)
    st.bar_chart(kpi_nsr_rr_df.set_index("AGENTE DE COBRANZA")[["NSR (%)", "RR (%)"]])

# KPI adicional: Análisis por fila de cobranza y estado de pago
st.subheader("⏱️ Análisis de atraso y cumplimiento por fila de cobranza")
lpr_acp_filas = atraso_por_fila_y_estado(df)

if "Error" in lpr_acp_filas.columns:
    st.error(f"❌ Error: {lpr_acp_filas['Error'][0]}")
else:
    st.dataframe(lpr_acp_filas, use_container_width=True)

# KPI adicional: Promedio de días de atraso y total de casos por fila y estado
st.subheader("📊 Promedio de días de atraso y cantidad de casos por fila y estado del pago")
df_atraso_fila_estado = atraso_por_fila_y_estado(df)

if "Error" in df_atraso_fila_estado.columns:
    st.error(f"❌ Error: {df_atraso_fila_estado['Error'][0]}")
else:
    st.dataframe(df_atraso_fila_estado, use_container_width=True)

# KPI: Promedio de días de atraso y cantidad de casos por fila de cobranza y estado del pago
st.subheader("📌 Promedio de Días de Atraso por Fila de Cobranza y Estado del Pago")
df_kpi_final = atraso_por_fila_y_estado(df)

if "Error" in df_kpi_final.columns:
    st.error(f"❌ Error: {df_kpi_final['Error'][0]}")
else:
    st.dataframe(df_kpi_final, use_container_width=True)

# 🏆 Productividad por agente (filtrada por fecha y fila)
st.subheader("🏆 Productividad por Agente de Cobranza (Con filtros)")

with st.expander("📆 Filtros para productividad"):
    col1, col2 = st.columns(2)
    fecha_inicio_prod = col1.date_input("Desde", df["FECHA"].min().date())
    fecha_fin_prod = col2.date_input("Hasta", df["FECHA"].max().date())
    fila_seleccion_prod = st.selectbox("Selecciona la fila de cobranza", options=["Todos"] + sorted(df["FILA DE COBRANZA"].dropna().unique().tolist()))

if fila_seleccion_prod != "Todos":
    df_productividad = productividad_por_agente(df, fecha_inicio_prod, fecha_fin_prod, fila_seleccion_prod)
else:
    df_productividad = productividad_por_agente(df, fecha_inicio_prod, fecha_fin_prod)

st.dataframe(df_productividad, use_container_width=True)

# Gráfico de barras horizontal
if not df_productividad.empty:
    try:
        import altair as alt
        graf_prod = alt.Chart(df_productividad).mark_bar(size=30).encode(
            y=alt.Y("CUENTAS CON PAGO:Q", title="Cuentas Pagadas", scale=alt.Scale(zero=True, nice=True)),
            x=alt.X("AGENTE DE COBRANZA:N", sort="-y", title="Agente de Cobranza"),
            tooltip=["AGENTE DE COBRANZA", "CUENTAS CON PAGO"]
        ).properties(width=900, height=500)

        texto = alt.Chart(df_productividad).mark_text(
            align="center",
            baseline="bottom",
            dy=-5
        ).encode(
            x=alt.X("AGENTE DE COBRANZA:N", sort="-y"),
            y="CUENTAS CON PAGO:Q",
            text=alt.Text("CUENTAS CON PAGO:Q")
        )

        st.altair_chart(graf_prod + texto, use_container_width=True)
    except Exception as e:
        st.warning(f"No se pudo renderizar la gráfica de productividad: {e}")
    except Exception as e:
        st.warning(f"No se pudo renderizar la gráfica de productividad: {e}")
    except Exception as e:
        st.warning(f"No se pudo renderizar la gráfica de productividad: {e}")


st.subheader("🏢 Productividad por Fila de Cobranza")

try:
    df_filas = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
    df_filas_grouped = df_filas.groupby("FILA DE COBRANZA").size().reset_index(name="CUENTAS PAGADAS")

    graf_fila = alt.Chart(df_filas_grouped).mark_bar(size=30).encode(
        y=alt.Y("CUENTAS PAGADAS:Q", title="Cuentas Pagadas"),
        x=alt.X("FILA DE COBRANZA:N", sort="-y", title="Fila de Cobranza"),
        tooltip=["FILA DE COBRANZA", "CUENTAS PAGADAS"]
    ).properties(width=700, height=400)

    etiquetas_fila = alt.Chart(df_filas_grouped).mark_text(
        align="center", baseline="bottom", dy=-5
    ).encode(
        x=alt.X("FILA DE COBRANZA:N", sort="-y"),
        y="CUENTAS PAGADAS:Q",
        text="CUENTAS PAGADAS:Q"
    )

    st.altair_chart(graf_fila + etiquetas_fila, use_container_width=True)
except Exception as e:
    st.warning(f"No se pudo mostrar la gráfica por fila de cobranza: {e}")

st.subheader("📊 Comparativo de Cumplimiento y Productividad por Agente")

# Filtro por fecha
fechas_disponibles = pd.to_datetime(df["FECHA"].unique())
fecha_min, fecha_max = fechas_disponibles.min(), fechas_disponibles.max()
fecha_inicio, fecha_fin = st.date_input("Selecciona el rango de fechas:", [fecha_min, fecha_max])

df_fecha = df[
    (pd.to_datetime(df["FECHA"]) >= pd.to_datetime(fecha_inicio)) &
    (pd.to_datetime(df["FECHA"]) <= pd.to_datetime(fecha_fin))
]


# Filtro adicional por agente de cobranza
agentes_disponibles = sorted(df_fecha["AGENTE DE COBRANZA"].dropna().unique())
agente_seleccionado = st.selectbox("Selecciona un agente de cobranza:", ["Todos"] + agentes_disponibles)

if agente_seleccionado != "Todos":
    df_fecha = df_fecha[df_fecha["AGENTE DE COBRANZA"] == agente_seleccionado]


# KPIs de cumplimiento por estado
tabla_estado = df_fecha.pivot_table(
    index="AGENTE DE COBRANZA",
    columns="ESTADO DEL PAGO PROMETIDO",
    values="MONTO DE PAGO",
    aggfunc="sum",
    fill_value=0
).reset_index()

monto_prometido = df_fecha.groupby("AGENTE DE COBRANZA")["MONTO DE PAGO PROMETIDO"].sum().reset_index(name="MONTO PROMETIDO")
tabla_estado = pd.merge(monto_prometido, tabla_estado, on="AGENTE DE COBRANZA", how="left")
tabla_estado["% CUMPLIMIENTO"] = ((tabla_estado.get("COMPLETO", 0) + tabla_estado.get("PARCIAL", 0)) / tabla_estado["MONTO PROMETIDO"] * 100).round(2)

st.markdown("### 💰 Monto Prometido vs Pagado por Estado del Pago")
st.dataframe(tabla_estado)

# Productividad por agente
tabla_productividad = df_fecha[df_fecha["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
tabla_productividad = tabla_productividad.groupby("AGENTE DE COBRANZA").size().reset_index(name="CUENTAS PAGADAS")
tabla_productividad = tabla_productividad.sort_values(by="CUENTAS PAGADAS", ascending=False)

st.markdown("### 🏆 Productividad por Agente de Cobranza")
st.dataframe(tabla_productividad)

# Gráfica: Monto prometido vs pagado por estado (por agente)
try:
    df_plot_estado = tabla_estado.copy()
    df_plot_estado = df_plot_estado.fillna(0)
    df_plot_estado = df_plot_estado.melt(
        id_vars=["AGENTE DE COBRANZA"],
        value_vars=["COMPLETO", "PARCIAL", "PENDIENTE"],
        var_name="ESTADO DEL PAGO",
        value_name="MONTO"
    )

    chart_estado = alt.Chart(df_plot_estado).mark_bar().encode(
        x=alt.X("AGENTE DE COBRANZA:N", sort="-y", title="Agente de Cobranza"),
        y=alt.Y("MONTO:Q", title="Monto"),
        color="ESTADO DEL PAGO:N",
        tooltip=["AGENTE DE COBRANZA", "ESTADO DEL PAGO", "MONTO"]
    ).properties(width=800, height=400).configure_axisX(labelAngle=-45)

    st.altair_chart(chart_estado, use_container_width=True)
except Exception as e:
    st.warning(f"No se pudo generar la gráfica de montos por estado: {e}")

# Gráfica: Productividad (cuentas con pago)
try:
    chart_productividad = alt.Chart(tabla_productividad).mark_bar(size=20).encode(
        x=alt.X("AGENTE DE COBRANZA:N", sort="-y"),
        y=alt.Y("CUENTAS PAGADAS:Q", title="Cuentas con Pago"),
        tooltip=["AGENTE DE COBRANZA", "CUENTAS PAGADAS"]
    ).properties(width=800, height=400).configure_axisX(labelAngle=-45)

    st.altair_chart(chart_productividad, use_container_width=True)
except Exception as e:
    st.warning(f"No se pudo generar la gráfica de productividad: {e}")

# ✅ Sección: Efectividad de Cobranza por Agente (con filtros de fecha, fila y agente)
st.subheader("✅ Efectividad de Cobranza por Agente (Filtrada)")

# Filtros aplicados
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    filtro_fila = st.selectbox("📁 Fila de Cobranza", ["Todos"] + sorted(df["FILA DE COBRANZA"].dropna().unique().tolist()), key="fila_efectividad")
with col_f2:
    filtro_agente = st.selectbox("👤 Agente de Cobranza", ["Todos"] + sorted(df["AGENTE DE COBRANZA"].dropna().unique().tolist()), key="agente_efectividad")
with col_f3:
    fechas = st.date_input("📆 Rango de Fechas", [df["FECHA"].min(), df["FECHA"].max()], key="fecha_efectividad")

# Aplicar filtros
df_ef = df.copy()
df_ef["FECHA"] = pd.to_datetime(df_ef["FECHA"], errors="coerce")
if filtro_fila != "Todos":
    df_ef = df_ef[df_ef["FILA DE COBRANZA"] == filtro_fila]
if filtro_agente != "Todos":
    df_ef = df_ef[df_ef["AGENTE DE COBRANZA"] == filtro_agente]
df_ef = df_ef[(df_ef["FECHA"] >= pd.to_datetime(fechas[0])) & (df_ef["FECHA"] <= pd.to_datetime(fechas[1]))]

# Calcular efectividad
efectividad_df = calcular_efectividad_por_agente(df_ef)
if not efectividad_df.empty:
    st.dataframe(efectividad_df, use_container_width=True)
    st.bar_chart(efectividad_df.set_index("AGENTE DE COBRANZA"))
else:
    st.info("No hay datos disponibles para los filtros seleccionados.")