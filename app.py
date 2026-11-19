
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="Monitoreo de Calidad del Agua",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Sistema de Monitoreo de Calidad del Agua")
st.subheader("Prototipo digital para zonas rurales de Tolima")
st.info("Esta aplicación es una simulación académica. Los valores no provienen de sensores reales ni certifican la potabilidad del agua.")

st.sidebar.header("Panel de sensores")
st.sidebar.write("Modifica los valores para simular las mediciones.")

ph = st.sidebar.slider("Nivel de pH", 0.0, 14.0, 7.0, 0.1)
turbidez = st.sidebar.number_input("Turbidez (NTU)", min_value=0.0, value=2.0, step=0.1)
tds = st.sidebar.number_input("Sólidos disueltos (mg/L)", min_value=0, value=300, step=10)
temperatura = st.sidebar.slider("Temperatura (°C)", 0.0, 60.0, 22.0, 0.5)

if "historial" not in st.session_state:
    st.session_state.historial = []

st.header("1. Lectura de los sensores")

col1, col2, col3, col4 = st.columns(4)

col1.metric("pH", f"{ph:.1f}")
col2.metric("Turbidez", f"{turbidez:.1f} NTU")
col3.metric("TDS", f"{tds} mg/L")
col4.metric("Temperatura", f"{temperatura:.1f} °C")

st.header("2. Evaluación de las mediciones")

alertas = []

if not 6.5 <= ph <= 8.5:
    alertas.append("El pH está fuera del rango ilustrativo configurado.")
if turbidez > 5:
    alertas.append("La turbidez supera el umbral ilustrativo configurado.")
if tds > 500:
    alertas.append("Los sólidos disueltos superan el umbral ilustrativo configurado.")
if temperatura > 30:
    alertas.append("La temperatura supera el umbral ilustrativo configurado.")

if alertas:
    st.error("Se detectaron valores que requieren revisión:")
    for alerta in alertas:
        st.write("⚠️", alerta)
else:
    st.success("Las mediciones están dentro de los umbrales ilustrativos configurados.")

st.caption("Los umbrales son parámetros demostrativos del prototipo, no una evaluación normativa de potabilidad.")

st.header("3. Registro de mediciones")

if st.button("Guardar medición"):
    registro = {
        "Fecha y hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pH": ph,
        "Turbidez (NTU)": turbidez,
        "TDS (mg/L)": tds,
        "Temperatura (°C)": temperatura
    }
    st.session_state.historial.append(registro)
    st.success("Medición guardada correctamente.")

if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Descargar registros en CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="mediciones_calidad_agua.csv",
        mime="text/csv"
    )

    st.header("4. Gráfica de mediciones")
    figura, eje = plt.subplots()
    eje.plot(df.index + 1, df["pH"], marker="o", label="pH")
    eje.set_xlabel("Número de medición")
    eje.set_ylabel("Nivel de pH")
    eje.set_title("Variación del pH en las mediciones")
    eje.legend()
    eje.grid(True)
    st.pyplot(figura)

else:
    st.warning("Todavía no hay mediciones guardadas. Modifica los sensores y pulsa 'Guardar medición'.")


st.header("5. Componentes simulados del sistema")

st.write("""
- **ESP32:** representa la unidad de procesamiento de las lecturas.
- **Sensor de pH:** simula la medición del nivel de acidez o alcalinidad.
- **Sensor de turbidez:** simula la presencia de partículas suspendidas.
- **Sensor TDS:** simula la medición de sólidos disueltos totales.
- **Sensor de temperatura:** simula la temperatura del agua.
- **Pantalla OLED:** se representa mediante los indicadores del panel.
- **LoRa:** representa la comunicación de datos hacia un punto de monitoreo.
- **MicroSD:** se representa mediante el registro y descarga de mediciones.
- **Panel solar y batería:** representan la alimentación autónoma contemplada en el diseño.
""")

