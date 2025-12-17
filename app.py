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

/* Fondo azul celeste */
.stApp {
    background-color: #eaf3fb;
}

/* Tarjetas principales */
.card {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    margin-bottom: 25px;
}

/* Títulos */
h1 {
    color: #0f172a;
    font-size: 40px;
}
h2, h3 {
    color: #1e293b;
}

/* INPUTS: todos blancos, borde suave */
input, select, textarea {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: inset 0px 1px 2px rgba(0,0,0,0.05);
}

/* Inputs de Streamlit */
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}

/* Resultado destacado */
.resultado {
    background-color: #d1fae5;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #065f46;
}

/* Botón principal */
div.stButton > button {
    background-color: #2563eb;
    color: white;
    font-size: 20px;
    padding: 12px;
    border-radius: 12px;
    border: none;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
}

/* Footer */
.footer {
    font-size: 12px;
    color: #475569;
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
# COLUMNAS
# -------------------------------
col1, col2 = st.columns(2)

# -------------------------------
# DATOS DEL CLIENTE
# -------------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Datos del Cliente")

    nombre = st.text_input("Nombre del cliente", placeholder="Ej. Juan Pérez")
    edad_actual = st.number_input("Edad actual", min_value=18, max_value=67, value=45)
    base_media = st.number_input("Base media de cotización (€ / mes)", min_value=0, value=2000)
    años_cotizados = st.number_input("Años cotizados", min_value=0, max_value=45, value=25)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# DATOS JUBILACIÓN
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
# SIMULACIÓN
# -------------------------------
st.divider()

if st.button("📊 SIMULAR JUBILACIÓN", use_container_width=True):

    if años_cotizados < 15:
        porcentaje = 0
    elif años_cotizados >= 36:
        porcentaje = 1
    else:
        porcentaje = años_cotizados / 36

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
# LEGAL
# -------------------------------
st.markdown("""
<div class="footer">
Simulación orientativa. No constituye oferta vinculante ni cálculo oficial de la Seguridad Social.
</div>
""", unsafe_allow_html=True)
