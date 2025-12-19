import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="Simulador de Jubilación",
    layout="centered"
)

# -------------------------------
# ESTILOS
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(180deg, #e8f4fb 0%, #f7fbfe 100%);
}

.card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

h1 {
    color: #0b3c5d;
    font-weight: 700;
}

h3 {
    color: #145a86;
    font-weight: 600;
}

.stButton button {
    background: linear-gradient(90deg, #1e88e5, #42a5f5);
    color: white;
    border-radius: 10px;
    padding: 12px 26px;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.result-box {
    background: linear-gradient(90deg, #1e88e5, #42a5f5);
    color: white;
    padding: 25px;
    border-radius: 16px;
    text-align: center;
}

.result-value {
    font-size: 34px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TÍTULO
# -------------------------------
st.markdown("<h1>Simulador de Jubilación</h1>", unsafe_allow_html=True)

# -------------------------------
# DATOS
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Datos personales</h3>", unsafe_allow_html=True)

nombre = st.text_input("Nombre del cliente")
anio_nacimiento = st.number_input("Año de nacimiento", min_value=1900, max_value=2025, value=1975)
edad_jubilacion = st.number_input("Edad de jubilación prevista", min_value=60, max_value=70, value=67)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Datos de cotización</h3>", unsafe_allow_html=True)

anios_cotizados = st.number_input("Años cotizados", min_value=0, max_value=50, value=35)
base_mensual = st.number_input("Base de cotización media mensual (€)", min_value=0, value=3000)
tipo_jubilacion = st.selectbox("Tipo de jubilación", ["Ordinaria", "Anticipada"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# BOTÓN
# -------------------------------
simular = st.button("Calcular pensión")

# -------------------------------
# RESULTADO
# -------------------------------
if simular:

    if anios_cotizados < 15:
        porcentaje = 0.5
    elif anios_cotizados < 36:
        porcentaje = 0.75
    else:
        porcentaje = 1

    penalizacion = 0.15 if tipo_jubilacion == "Anticipada" else 0
    pension = base_mensual * porcentaje * (1 - penalizacion)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Resultado estimado</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-box">
        <div class="result-value">{pension:,.2f} €</div>
        <div>Pensión mensual estimada</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # PDF
    # -------------------------------
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    azul = HexColor("#1e88e5")

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(azul)
    c.drawString(50, 800, "Simulación de Jubilación")

    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#000000"))

    y = 750
    datos = [
        ("Cliente", nombre),
        ("Año de nacimiento", anio_nacimiento),
        ("Edad jubilación", edad_jubilacion),
        ("Años cotizados", anios_cotizados),
        ("Base media mensual", f"{base_mensual} €"),
        ("Tipo de jubilación", tipo_jubilacion),
    ]

    for k, v in datos:
        c.drawString(60, y, f"{k}: {v}")
        y -= 22

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(azul)
    c.drawString(60, y - 20, f"Pensión mensual estimada: {pension:,.2f} €")

    c.showPage()
    c.save()
    buffer.seek(0)

    st.download_button(
        label="📄 Descargar informe en PDF",
        data=buffer,
        file_name="simulacion_jubilacion.pdf",
        mime="application/pdf"
    )

