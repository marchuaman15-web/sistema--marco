import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Sistema OTs Marco", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

# Intentamos leer la pestaña EQUIPOS
try:
    df_equipos = conn.read(worksheet="EQUIPOS")
except Exception as e:
    st.error(f"Error: No se encontró la pestaña 'EQUIPOS'. Verifica que en tu Excel se llame exactamente así.")
    st.stop()

st.title("🚜 Registro de Orden de Trabajo (OT)")

with st.form("form_ot"):
    col1, col2 = st.columns(2)
    with col1:
        # Usamos unique() para evitar errores si hay códigos duplicados
        cod_unidad = st.selectbox("Seleccione COD_UNIDAD", options=df_equipos["COD_EQUIPO"].unique().tolist())
        equipo_info = df_equipos[df_equipos["COD_EQUIPO"] == cod_unidad].iloc[0]
        
        n_ot = st.text_input("N° DE ORDEN DE TRABAJO")
        placa = st.text_input("PLACA", value=equipo_info["PLACAS"] if "PLACAS" in equipo_info else equipo_info["PLACA"])
    
    with col2:
        descripcion = st.text_input("DESCRIPCIÓN", value=equipo_info["DESCRIPCION"])
        flota = st.text_input("FLOTA", value=equipo_info["FLOTA"])
        km = st.number_input("KILOMETRAJE", min_value=0)

    boton_guardar = st.form_submit_button("Guardar Registro")

if boton_guardar:
    if not n_ot:
        st.warning("⚠️ Por favor, ingrese el número de OT.")
    else:
        df_ots = conn.read(worksheet="OTs")
        nueva_fila = pd.DataFrame([{
            "ORDEN DE TRABAJO": n_ot, "COD_UNIDAD": cod_unidad, 
            "PLACA": placa, "DESCRIPCION": descripcion, 
            "FLOTA": flota, "KILOMETRAJE": km
        }])
        df_final = pd.concat([df_ots, nueva_fila], ignore_index=True)
        conn.update(worksheet="OTs", data=df_final)
        st.success(f"✅ OT {n_ot} guardada con éxito!")
        st.balloons()
