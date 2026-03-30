import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import time

# --- CONFIGURACIÓN DE PÁGINA (MODERNA) ---
st.set_page_config(page_title="Carnicería Cloud 🥩", layout="wide", initial_sidebar_state="collapsed")

# --- VARIABLES MAESTRAS (TU NEGOCIO) ---
MI_CVU_COMISION = "0000003100094545267439"
COMISION_PORCENTAJE = 0.05  # Tu 5%

# --- 1. BASE DE DATOS (EL CEREBRO) ---
def init_db():
    conn = sqlite3.connect('carniceria_cloud.db')
    c = conn.cursor()
    # Tabla de Carniceros (Multitenant)
    c.execute('''CREATE TABLE IF NOT EXISTS perfiles 
                 (user_id TEXT PRIMARY KEY, nombre_local TEXT, cvu_vendedor TEXT, ventas_totales INTEGER DEFAULT 0)''')
    # Tabla de Mensajes (Chat)
    c.execute('''CREATE TABLE IF NOT EXISTS mensajes 
                 (id INTEGER PRIMARY KEY, remitente TEXT, mensaje TEXT, leido INTEGER DEFAULT 0)''')
    conn.commit()
    return conn

conn = init_db()

# --- 2. LÓGICA DE SONIDO Y NOTIFICACIÓN ---
def sonar_chaching():
    st.components.v1.html("""
        <audio autoplay><source src="https://www.myinstants.com/media/sounds/cash-register-purchase.mp3" type="audio/mp3"></audio>
    """, height=0)

# --- 3. INTERFAZ: REGISTRO DE CARNICERO (ONBOARDING) ---
def seccion_registro():
    st.title("🚀 Unite a Carnicería Cloud")
    with st.form("registro"):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre de tu Carnicería", placeholder="Ej: La Granja de Claudio")
        cvu = col2.text_input("Tu CBU/CVU (22 dígitos)", help="Aquí recibís tu 95%")
        passw = st.text_input("Contraseña de Acceso", type="password")
        
        if st.form_submit_button("REGISTRAR MI LOCAL"):
            if len(cvu) == 22:
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO perfiles VALUES (?, ?, ?, 0)", (passw, nombre, cvu))
                conn.commit()
                st.success("¡Local verificado! Ya podés vender.")
                st.balloons()
            else:
                st.error("CBU/CVU inválido. Deben ser 22 números.")

# --- 4. INTERFAZ: EL "TINDER" DEL CLIENTE (DESLIZABLE) ---
def vista_cliente():
    st.markdown("<h1 style='text-align: center;'>🥩 Elegí tu Carnicería</h1>", unsafe_allow_html=True)
    perfiles = pd.read_sql_query("SELECT * FROM perfiles", conn)
    
    if perfiles.empty:
        st.info("Buscando carniceros en Merlo... (Registrá el primero arriba)")
    else:
        # Carrusel Moderno
        for idx, p in perfiles.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="border-radius:15px; padding:20px; background:#fff; border-left:8px solid #cc0000; box-shadow: 2px 2px 10px #eee; margin-bottom:15px;">
                    <span style="color:#cc0000; font-weight:bold;">🛡️ CARNICERO VERIFICADO</span>
                    <h2 style="margin:0;">{p['nombre_local']}</h2>
                    <p style="color:gray;">📍 Merlo, Buenos Aires</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if c1.button(f"🛒 Ver Vitrina - {p['nombre_local']}", key=f"btn_{idx}"):
                    st.session_state.vendedor_activo = p['nombre_local']
                if c2.button(f"💬 Chatear con Raúl", key=f"chat_{idx}"):
                    st.session_state.chat_activo = True

# --- 5. EL BOTÓN VERDE Y SPLIT DE PAGO ---
def procesar_pago(monto):
    st.warning(f"Procesando pago de ${monto}...")
    time.sleep(2) # Simulación de red
    
    # SPLIT MATEMÁTICO (Analista de Sistemas)
    mi_comision = monto * COMISION_PORCENTAJE
    pago_carnicero = monto - mi_comision
    
    st.success(f"✅ ¡PAGO APROBADO!")
    sonar_chaching()
    
    col1, col2 = st.columns(2)
    col1.metric("Para el Carnicero (95%)", f"${pago_carnicero:,.2f}")
    col2.metric("Tu Comisión (5%)", f"${mi_comision:,.2f}", delta="A tu CVU ...7439")
    
    st.markdown("<h1 style='text-align: center; color: green;'>🟢 OK - ENTREGAR</h1>", unsafe_allow_html=True)

# --- 6. PROTOCOLO DE EMERGENCIA SOS ---
def boton_falla():
    with st.sidebar:
        if st.button("⚠️ FALLA TÉCNICA (SOS)"):
            st.error("🚨 ALERTA ENVIADA AL SOPORTE")
            st.write("**Protocolo de Emergencia:**")
            st.write("1. Reiniciá la App.")
            st.write("2. Usá el QR de Respaldo físico.")
            st.write(f"3. Rendí el 5% manual a: `{MI_CVU_COMISION}`")

# --- NAVEGACIÓN PRINCIPAL ---
opcion = st.sidebar.selectbox("Ir a:", ["Vista Cliente", "Panel Carnicero", "Registro Nuevo Local"])

if opcion == "Registro Nuevo Local":
    seccion_registro()
elif opcion == "Panel Carnicero":
    boton_falla()
    st.title("👨‍🍳 Panel de Control")
    # Simulación de una venta de $10.000 para probar el sistema
    if st.button("Simular Venta de $10.000"):
        procesar_pago(10000)
else:
    vista_cliente()

