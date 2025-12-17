import streamlit as st

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
st.set_page_config(
    page_title="Simulador Profesional de Jubilación",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# ESTILOS PROFESIONALES (CSS)
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f6f9;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

h1, h2, h3 {
    color: #1f2937;
}

.resultado {
    background-color: #e8f5e9;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #1b5e20;
}

.footer {
    font-size: 12px;
    color: #6b7280;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# CABECERA
# -------------------------------
st.title("Simulador Profesional de Jubilación")
st.caption("Herramienta de asesoramiento previsional para clientes")

st.divider()

# -------------------------------
# COLUMNAS PRINCIPALES
# -------------------------------
col1, col2 = st.columns(2)

# -------------------------------
# COLUMNA IZQUIERDA - DATOS
# -------------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Datos del Cliente")

    nombre = st.text_input("Nombre del cliente")
    edad_actual = st.number_input("Edad actual", min_value=18, max_value=67, value=45)
    base_media = st.number_input("Base media de cotización (€ / mes)", min_value=0, value=2000)
    años_cotizados = st.number_input("Años cotizados", min_value=0, max_value=45, value=25)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# COLUMNA DERECHA - JUBILACIÓN
# -------------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Tipo de Jubilación")

    tipo_jubilacion = st.selectbox(
        "Modalidad",
        ["Ordinaria", "Anticipada"]
    )

    edad_jubilacion = 65 if años_cotizados >= 38 else 67

    st.markdown(f"""
    **Edad legal estimada:** {edad_jubilacion} años  
    **Años para jubilarse:** {max(0, edad_jubilacion - edad_actual)}
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# BOTÓN SIMULACIÓN
# -------------------------------
st.divider()

if st.button("📊 SIMULAR JUBILACIÓN", use_container_width=True):

    # Porcentaje según años cotizados (simplificado)
    if años_cotizados < 15:
        porcentaje = 0
    elif años_cotizados >= 36:
        porcentaje = 1
    else:
        porcentaje = años_cotizados / 36

    # Penalización por anticipada
    penalizacion = 0.85 if tipo_jubilacion == "Anticipada" else 1

    pension_mensual = base_media * porcentaje * penalizacion

    st.markdown(f"""
    <div class="resultado">
        Pensión estimada<br>
        {pension_mensual:,.2f} € / mes
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Detalle del cálculo")

    st.write(f"Porcentaje aplicado por años cotizados: **{porcentaje*100:.1f}%**")

    if tipo_jubilacion == "Anticipada":
        st.write("Penalización por jubilación anticipada: **-15%**")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# FOOTER LEGAL
# -------------------------------
st.markdown("""
<div class="footer">
Simulación orientativa. No constituye oferta vinculante ni cálculo oficial de la Seguridad Social.
</div>
""", unsafe_allow_html=True)

