
# 📊 Dashboard Estratégico de Cobranza

Este proyecto es un dashboard interactivo creado con **Streamlit** para visualizar datos de cobranza desde un archivo Excel. Puedes desplegarlo localmente o en Render para monitorear:

- Monto prometido vs monto pagado
- Tasa de cumplimiento
- KPIs de desempeño por agente
- Gráficas interactivas

## 🧾 Archivos incluidos

- `dashboard_estrategico.py`: código principal de la app en Streamlit
- `requirements.txt`: librerías necesarias para el entorno
- `Historial_Pagos_Prestamos.xlsx`: ejemplo de archivo Excel para prueba

## 🚀 Cómo desplegar en Render

1. Haz clic en **New Web Service**
2. Conecta tu cuenta de GitHub y selecciona este repositorio
3. Usa la siguiente configuración:

- **Build Command**:  
  `pip install -r requirements.txt`

- **Start Command**:  
  `streamlit run dashboard_estrategico.py --server.port=10000`

- **Runtime**: Python 3.10+

¡Render se encargará del resto!

## 🛠️ Cómo correr localmente

```bash
pip install -r requirements.txt
streamlit run dashboard_estrategico.py
```

---

© Proyecto educativo – creado con ❤️ por kga333
