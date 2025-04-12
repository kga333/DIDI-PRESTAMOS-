# 📊 Dashboard de Cobranza - Versión Completa para Render

Este proyecto contiene el dashboard `main.py` que se ejecuta con Streamlit y se despliega en Render. Ya incluye:

- KPIs completos
- Filtros por fecha, agente y fila de cobranza
- Cálculos de DSO, RR, ACP, LPR, NSR, entre otros
- Gráficas interactivas con Altair

## Estructura

```
📁 DIDI_PRESTAMOS_DASHBOARD_RENDER/
│
├── main.py
├── requirements.txt
├── README.md
├── 📁 utils/
│   └── kpi_calculations.py
├── 📁 data/
│   └── Historial_Pagos_Prestamos.xlsx  ← Debes subirlo tú manualmente
```

## Cómo desplegar en Render

1. Sube esta carpeta a un repositorio en GitHub
2. En Render:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `streamlit run main.py --server.port=10000`