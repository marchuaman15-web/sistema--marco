import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sistema OTs Marco", layout="wide")

st.title("🚜 Registro de Orden de Trabajo (OT)")

# Conexión con el Excel
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lee la pestaña EQUIPOS
    df_equipos = conn.read(worksheet="EQUIPOS")
    
    with st.form("form_ot"):
        col1, col2 = st.columns(2)
        with col1:
            cod_unidad = st.selectbox("Seleccione COD_UNIDAD", options=df_equipos["COD_EQUIPO"].unique())
            n_ot = st.text_input("N° DE ORDEN DE TRABAJO")
        
        with col2:
            km = st.number_input("KILOMETRAJE ACTUAL", min_value=0)
            detalles = st.text_area("DETALLES DEL TRABAJO")

        boton = st.form_submit_button("Guardar en Excel")

    if boton:
        if not n_ot:
            st.warning("Escribe el número de OT")
        else:
            # Aquí se guarda la info en la pestaña OTs
            df_ots = conn.read(worksheet="OTs")
            nueva_fila = pd.DataFrame([{"OT": n_ot, "UNIDAD": cod_unidad, "KM": km, "DETALLE": detalles}])
            df_final = pd.concat([df_ots, nueva_fila], ignore_index=True)
            conn.update(worksheet="OTs", data=df_final)
            st.success(f"✅ OT {n_ot} guardada con éxito")
            st.balloons()

except Exception as e:
    st.error("Error: Verifica que el link del Excel esté en 'Misterios' y las pestañas se llamen EQUIPOS y OTs."
