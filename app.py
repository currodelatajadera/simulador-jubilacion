import streamlit as st

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Simulador Profesional de Jubilación",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# ESTILOS (CSS)
# -------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #eaf3fb;
}

.card {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    margin-bottom: 25px;
}

h1 {
    color: #0f172a;
    font-size: 38px;
}

h2, h3 {
    color: #1e293b;
}

input, textarea {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    font-size: 14px !important;
    min-height: 36px !important;
}

.resultado {
    background-color: #d1fae5;
    padding: 32px;
    border-radius: 18px;
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #065f46;
}

.footer {
    font-size: 12px;
    color: #475569;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CABECERA
# -------------------------------------------------
st.title("Simulador Profesional de Jubilación")
st.caption("Herramienta de asesoramiento previsional para clientes")

st.divider()

# -------------------------------------------------
# FORMULARIO (CLAVE)
# -------------------------------------------------
with st.form("form_jubilacion"):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Datos del Cliente")

        nombre = st.text_input("Nombre del cliente")
        edad_actual = st.number_input("Edad actual", 18, 67, 45)
        base_media = st.number_input("Base media de cotización (€ / mes)", 0, 10000, 2000)
        años_cotizados = st.number_input("Años cotizados", 0, 45, 25)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Tipo de Jubilación")

        tipo_jubilacion = st.selectbox(
            "Modalidad",
            ["Ordinaria", "Anticipada"]
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # BOTÓN REAL
    submitted = st.form_submit_button("📊 Simular jubilación")

# -------------------------------------------------
# CÁLCULO SOLO AL PULSAR BOTÓN
# -------------------------------------------------
if submitted:

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

# -------------------------------------------------
# LEGAL
# -------------------------------------------------
st.markdown("""
<div class="footer">
Simulación orientativa. No constituye oferta vinculante ni cálculo oficial de la Seguridad Social.
</div>
""", unsafe_allow_html=True)



