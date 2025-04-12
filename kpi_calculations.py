
import pandas as pd

def calcular_efectividad_por_agente(df: pd.DataFrame) -> pd.DataFrame:
    tabla = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
    resultado = tabla.groupby("AGENTE DE COBRANZA")["CFRNID"].count().reset_index(name="CUENTAS EFECTIVAS")
    return resultado

def monto_prometido_vs_pagado(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MONTO COMPLETO"] = df[df["ESTADO DEL PAGO PROMETIDO"] == "COMPLETO"]["MONTO DE PAGO"]
    df["MONTO PARCIAL"] = df[df["ESTADO DEL PAGO PROMETIDO"] == "PARCIAL"]["MONTO DE PAGO"]
    df["MONTO SIN PAGO"] = df[df["ESTADO DEL PAGO PROMETIDO"] == "PENDIENTE"]["MONTO DE PAGO"]
    resumen = df.groupby("AGENTE DE COBRANZA").agg({
        "MONTO DE PAGO PROMETIDO": "sum",
        "MONTO COMPLETO": "sum",
        "MONTO PARCIAL": "sum",
        "MONTO SIN PAGO": "sum"
    }).fillna(0)
    resumen["% CUMPLIMIENTO"] = ((resumen["MONTO COMPLETO"] + resumen["MONTO PARCIAL"]) / resumen["MONTO DE PAGO PROMETIDO"]) * 100
    return resumen.reset_index()

def distribucion_estado_pago(df: pd.DataFrame) -> pd.DataFrame:
    return df["ESTADO DEL PAGO PROMETIDO"].value_counts(normalize=True).reset_index().rename(columns={
        "index": "Estado",
        "ESTADO DEL PAGO PROMETIDO": "% del Total"
    })

def monto_total_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
    df["MONTO SUMADO"] = df["MONTO DE PAGO"]
    return df.groupby("FECHA")["MONTO SUMADO"].sum().reset_index(name="MONTO TOTAL")

def cuentas_alto_riesgo(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[(df["ESTADO DEL PAGO PROMETIDO"] == "PENDIENTE") & (df["DIAS DE ATRASO EN EL MOMENTO DEL PAGO PROMETIDO"] >= 90)]
    return df.groupby("AGENTE DE COBRANZA")["CFRNID"].count().reset_index(name="CUENTAS DE ALTO RIESGO")

def indicadores_dso_rr_sr(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["FECHA_PROMESA"] = pd.to_datetime(df["HORA DE PAGO PROMETIDO"], errors="coerce")
    df["FECHA_REAL"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df_pagados = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])].copy()
    df_pagados = df_pagados[df_pagados["MONTO DE PAGO PROMETIDO"] > 0]
    df_pagados["DIAS_DSO"] = (df_pagados["FECHA_REAL"] - df_pagados["FECHA_PROMESA"]).dt.days
    resumen = df_pagados.groupby("AGENTE DE COBRANZA").agg({
        "MONTO DE PAGO PROMETIDO": "sum",
        "MONTO DE PAGO": "sum",
        "DIAS_DSO": "mean",
        "ESTADO DEL PAGO PROMETIDO": "count"
    }).rename(columns={
        "MONTO DE PAGO PROMETIDO": "PROMETIDO",
        "MONTO DE PAGO": "PAGADO",
        "DIAS_DSO": "DSO",
        "ESTADO DEL PAGO PROMETIDO": "PROMESAS LIQUIDADAS"
    })
    resumen["RECOVERY RATE (%)"] = (resumen["PAGADO"] / resumen["PROMETIDO"]) * 100
    resumen["SETTLEMENT RATE (%)"] = (resumen["PROMESAS LIQUIDADAS"] / resumen["PROMESAS LIQUIDADAS"].sum()) * 100
    return resumen.reset_index()

def indicadores_lpr_acp(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["FECHA_PROMESA"] = pd.to_datetime(df["HORA DE PAGO PROMETIDO"], errors="coerce")
    df["FECHA_REAL"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df_pagados = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])].copy()
    df_pagados["DIAS_REALES"] = (df_pagados["FECHA_REAL"] - df_pagados["FECHA_PROMESA"]).dt.days
    df_pagados["PAGO_TARDIO"] = df_pagados["DIAS_REALES"] > 0
    resumen = df_pagados.groupby("AGENTE DE COBRANZA").agg({
        "DIAS_REALES": "mean",
        "PAGO_TARDIO": "mean",
        "ESTADO DEL PAGO PROMETIDO": "count"
    }).rename(columns={
        "DIAS_REALES": "ACP",
        "PAGO_TARDIO": "LPR (%)",
        "ESTADO DEL PAGO PROMETIDO": "PAGOS"
    })
    resumen["LPR (%)"] = resumen["LPR (%)"] * 100
    return resumen.reset_index()

def indicadores_nsr_rr(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df_validas = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL", "PENDIENTE"])].copy()
    df_validas["PROMESA EXITOSA"] = df_validas["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])
    df_validas["PROMESA FALLIDA"] = df_validas["ESTADO DEL PAGO PROMETIDO"] == "PENDIENTE"
    resumen = df_validas.groupby("AGENTE DE COBRANZA").agg({
        "ESTADO DEL PAGO PROMETIDO": "count",
        "PROMESA EXITOSA": "sum",
        "PROMESA FALLIDA": "sum"
    }).rename(columns={
        "ESTADO DEL PAGO PROMETIDO": "TOTAL PROMESAS",
        "PROMESA EXITOSA": "CUMPLIDAS",
        "PROMESA FALLIDA": "RECHAZADAS"
    })
    resumen["NSR (%)"] = (resumen["CUMPLIDAS"] / resumen["TOTAL PROMESAS"]) * 100
    resumen["RR (%)"] = (resumen["RECHAZADAS"] / resumen["TOTAL PROMESAS"]) * 100
    return resumen.reset_index()

def atraso_por_fila_y_estado(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL", "PENDIENTE"])]
    df["DIAS DE ATRASO"] = pd.to_numeric(df["DIAS DE ATRASO EN EL MOMENTO DEL PAGO PROMETIDO"], errors="coerce").fillna(0)
    agrupado = df.groupby(["FILA DE COBRANZA", "ESTADO DEL PAGO PROMETIDO"]).agg({
        "DIAS DE ATRASO": "mean",
        "CFRNID": "count"
    }).reset_index()
    agrupado.rename(columns={
        "DIAS DE ATRASO": "PROMEDIO DIAS DE ATRASO",
        "CFRNID": "TOTAL CASOS"
    }, inplace=True)
    return agrupado


def productividad_por_agente(df: pd.DataFrame, fecha_inicio=None, fecha_fin=None, fila=None) -> pd.DataFrame:
    df = df.copy()
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    if fecha_inicio and fecha_fin:
        df = df[(df["FECHA"] >= fecha_inicio) & (df["FECHA"] <= fecha_fin)]

    if fila:
        df = df[df["FILA DE COBRANZA"] == fila]

    df = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
    resumen = df.groupby("AGENTE DE COBRANZA")["CFRNID"].count().reset_index(name="CUENTAS PAGADAS")
    resumen = resumen.sort_values("CUENTAS PAGADAS", ascending=False)
    return resumen


def productividad_por_agente(df: pd.DataFrame, fecha_inicio=None, fecha_fin=None, fila=None) -> pd.DataFrame:
    df = df.copy()
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    if fecha_inicio:
        df = df[df["FECHA"] >= pd.to_datetime(fecha_inicio)]
    if fecha_fin:
        df = df[df["FECHA"] <= pd.to_datetime(fecha_fin)]
    if fila:
        df = df[df["FILA DE COBRANZA"] == fila]

    df = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
    
    resumen = df.groupby("AGENTE DE COBRANZA")["CFRNID"].count().reset_index(name="CUENTAS CON PAGO")
    resumen = resumen.sort_values(by="CUENTAS CON PAGO", ascending=False).reset_index(drop=True)
    return resumen

def calcular_efectividad_por_agente(df):
    df_filtrado = df[df["ESTADO DEL PAGO PROMETIDO"].isin(["COMPLETO", "PARCIAL"])]
    efectividad = df_filtrado.groupby("AGENTE DE COBRANZA").size().reset_index(name="CUENTAS CON PAGO")
    efectividad = efectividad.sort_values(by="CUENTAS CON PAGO", ascending=False)
    return efectividad