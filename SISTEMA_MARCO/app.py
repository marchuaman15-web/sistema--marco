[10:49 p.m., 21/2/2026] Marco Antonio: import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sistema OTs Marco", layout="wide")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar base de datos de EQUIPOS
df_equipos = conn.read(worksheet="EQUIPOS")

st.title("🚜 Registro de Orden de Trabajo (OT)")

with st.form("form_ot"):
    col1, col2 = st.columns(2)
    with col1:
        cod_unidad = st.selectbox("Seleccione COD_UNIDAD", options=df_equipos["COD_EQUIPO"].tolist())
        # Buscar info del equipo seleccionado
        equipo_info = df_equipos[df_equipos["COD_EQUIPO"] == cod_unidad].iloc[0]
        
        n_ot = st.text_input("ORDEN DE TRABAJO (N°)")
        placa = st.text_input("PLACA", value=equipo_info["PLACA"])
    
    with col2:
        descripcion = st.text_input("DESCRIPCION", value=equipo_info["DESCRIPCION"])
        flota = st.text_input("FLOTA", value=equipo_info["FLOTA"])
        km = st.number_input("KILOMETRAJE", min_value=0)

    boton_guardar = st.form_submit_button("Guardar Registro")

if boton_guardar:
    # Leer OTs actuales
    df_ots = conn.read(worksheet="OTs")
    # Nueva fila
    nueva_fila = pd.DataFrame([{
        "ORDEN DE TRABAJO": n_ot, 
        "COD_UNIDAD": cod_unidad, 
        "PLACA": placa, 
        "DESCRIPCION": descripcion, 
        "FLOTA": flota, 
        "KILOMETRAJE": km
    }])
    # Unir y actualizar
    df_final = pd.concat([df_ots, nueva_fila], ignore_index=True)
    conn.update(worksheet="OTs", data=df_final)
    st.success(f"✅ OT {n_ot} guardada con éxito!")
[10:51 p.m., 21/2/2026] Marco Antonio: streamlit
streamlit-gsheets
pandas
[11:01 p.m., 21/2/2026] Marco Antonio: import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración visual de la aplicación
st.set_page_config(page_title="Sistema OTs Marco", layout="wide")

# Conector con tu Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer los datos de la pestaña "EQUIPOS"
try:
    df_equipos = conn.read(worksheet="EQUIPOS")
except Exception as e:
    st.error("No se pudo leer la pestaña 'EQUIPOS'. Revisa el nombre en tu Excel.")
    st.stop()

st.title("🚜 Registro de Orden de Trabajo (OT)")
st.markdown("---")

# Formulario de entrada
with st.form("form_ot"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Menú desplegable con los códigos de equipo
        cod_unidad = st.selectbox("Seleccione COD_UNIDAD", options=df_equipos["COD_EQUIPO"].unique())
        
        # Filtramos la info automáticamente según el equipo elegido
        datos_auto = df_equipos[df_equipos["COD_EQUIPO"] == cod_unidad].iloc[0]
        
        n_ot = st.text_input("N° DE ORDEN DE TRABAJO (OT)")
        placa = st.text_input("PLACA", value=datos_auto["PLACA"], disabled=True)
    
    with col2:
        descripcion = st.text_input("DESCRIPCIÓN", value=datos_auto["DESCRIPCION"], disabled=True)
        flota = st.text_input("FLOTA", value=datos_auto["FLOTA"], disabled=True)
        km = st.number_input("KILOMETRAJE ACTUAL", min_value=0, step=1)

    enviar = st.form_submit_button("Guardar en Excel")

# Lógica para guardar los datos
if enviar:
    if not n_ot:
        st.warning("⚠️ Por favor, ingresa el número de OT.")
    else:
        # Preparamos la nueva fila
        nueva_fila = pd.DataFrame([{
            "ORDEN DE TRABAJO": n_ot,
            "COD_UNIDAD": cod_unidad,
            "PLACA": datos_auto["PLACA"],
            "DESCRIPCION": datos_auto["DESCRIPCION"],
            "FLOTA": datos_auto["FLOTA"],
            "KILOMETRAJE": km
        }])
        
        # Leemos lo que ya hay en la pestaña "OTs" y sumamos lo nuevo
        df_existente = conn.read(worksheet="OTs")
        df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
        
        # Subimos todo de vuelta al Excel
        conn.update(worksheet="OTs", data=df_actualizado)
        st.success(f"✅ ¡OT {n_ot} registrada correctamente!")
        st.balloons()
