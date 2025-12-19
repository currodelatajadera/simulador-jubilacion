import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
st.set_page_config(
    page_title="Simulador de Jubilación",
    layout="centered"
)

# -------------------------------
# ESTILOS (CSS)
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #eaf4fb;
}

.main {
    background-color: #eaf4fb;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

h1, h2, h3 {
    color: #0a3d62;
}

label {
    font-weight: 600;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background-color: white;
    border-radius: 8px;
}

.stButton > button {
    background-color: #0a3d62;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}

.result {
    font-size: 28px;
    font-weight: 700;
    color: #0a3d62;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TÍTULO
# -------------------------------
st.markdown("<h1>Simulador de Jubilación</h1>", unsafe_allow_html=True)
st.markdown("Herramienta profesional de apoyo comercial")

# -------------------------------
# TARJETA: DATOS CLIENTE
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Datos del cliente</h3>", unsafe_allow_html=True)

nombre = st.text_input("Nombre del cliente")
anio_nacimiento = st.number_input("Año de nacimiento", min_value=1900, max_value=2025, value=1978)
edad_jubilacion = st.number_input("Edad de jubilación prevista", min_value=60, max_value=70, value=67)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# TARJETA: DATOS COTIZACIÓN
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Datos de cotización</h3>", unsafe_allow_html=True)

anios_cotizados = st.number_input("Años cotizados", min_value=0, max_value=50, value=35)
base_mensual = st.number_input("Base de cotización media mensual (€)", min_value=0, value=3000)

tipo_jubilacion = st.selectbox(
    "Tipo de jubilación",
    ["Ordinaria", "Anticipada"],
    index=0
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# BOTÓN SIMULAR
# -------------------------------
simular = st.button("Simular jubilación")

# -------------------------------
# CÁLCULO
# -------------------------------
if simular:
    # Porcentaje según años cotizados (simplificado)
    if anios_cotizados < 15:
        porcentaje = 0.50
    elif anios_cotizados < 36:
        porcentaje = 0.75
    else:
        porcentaje = 1.00

    # Penalización por jubilación anticipada
    penalizacion = 0
    if tipo_jubilacion == "Anticipada":
        penalizacion = 0.15

    pension_mensual = base_mensual * porcentaje * (1 - penalizacion)

    # -------------------------------
    # RESULTADOS
    # -------------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Resultado de la simulación</h3>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='result'>{pension_mensual:,.2f} € / mes</div>",
        unsafe_allow_html=True
    )

    st.write(f"**Porcentaje aplicado:** {int(porcentaje*100)} %")
    if penalizacion > 0:
        st.write("⚠️ Incluye penalización por jubilación anticipada")

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # PDF
    # -------------------------------
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Simulación de Jubilación")

    c.setFont("Helvetica", 11)
    c.drawString(50, 760, f"Cliente: {nombre}")
    c.drawString(50, 740, f"Año de nacimiento: {anio_nacimiento}")
    c.drawString(50, 720, f"Edad jubilación: {edad_jubilacion}")
    c.drawString(50, 700, f"Años cotizados: {anios_cotizados}")
    c.drawString(50, 680, f"Base media mensual: {base_mensual} €")
    c.drawString(50, 660, f"Tipo de jubilación: {tipo_jubilacion}")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, 620, f"Pensión estimada mensual: {pension_mensual:,.2f} €")

    c.showPage()
    c.save()

    buffer.seek(0)

    st.download_button(
        label="📄 Descargar PDF para el cliente",
        data=buffer,
        file_name="simulacion_jubilacion.pdf",
        mime="application/pdf"
    )
