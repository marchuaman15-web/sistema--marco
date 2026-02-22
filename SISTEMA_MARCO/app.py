import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sistema OTs Marco", layout="wide")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar base de datos de EQUIPOS
try:
    df_equipos = conn.read(worksheet="EQUIPOS")
except:
    st.error("Error: No se encontró la pestaña 'EQUIPOS' en el Excel.")
    st.stop()

st.title("🚜 Registro de Orden de Trabajo (OT)")

with st.form("form_ot"):
    col1, col2 = st.columns(2)
    with col1:
        cod_unidad = st.selectbox("Seleccione COD_UNIDAD", options=df_equipos["COD_EQUIPO"].unique())
        # Buscar info del equipo
        equipo_info = df_equipos[df_equipos["COD_EQUIPO"] == cod_unidad].iloc[0]
        
        n_ot = st.text_input("ORDEN DE TRABAJO (N°)")
        placa = st.text_input("PLACA", value=equipo_info["PLACA"])
    
    with col2:
        descripcion = st.text_input("DESCRIPCION", value=equipo_info["DESCRIPCION"])
        flota = st.text_input("FLOTA", value=equipo_info["FLOTA"])
        km = st.number_input("KILOMETRAJE", min_value=0)

    boton_guardar = st.form_submit_button("Guardar Registro")

if boton_guardar:
    if not n_ot:
        st.warning("Escriba el número de OT")
    else:
        df_ots = conn.read(worksheet="OTs")
        nueva_fila = pd.DataFrame([{
            "ORDEN DE TRABAJO": n_ot, 
            "COD_UNIDAD": cod_unidad, 
            "PLACA": placa, 
            "DESCRIPCION": descripcion, 
            "FLOTA": flota, 
            "KILOMETRAJE": km
        }])
        df_final = pd.concat([df_ots, nueva_fila], ignore_index=True)
        conn.update(worksheet="OTs", data=df_final)
        st.success(f"✅ OT {n_ot} guardada!")
        st.balloons()
