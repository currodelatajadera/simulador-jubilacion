import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

# ---------------- CONFIG PÁGINA ----------------
st.set_page_config(
    page_title="Simulador de Jubilación",
    page_icon="📊",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background-color: #d9f0ff;
}

.main {
    background-color: #d9f0ff;
}

h1, h2, h3, label, p {
    color: #000000;
}

.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.stButton > button {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 16px;
}

.stSelectbox > div {
    max-width: 250px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TÍTULO ----------------
st.title("📊 Simulador de Jubilación")

# ---------------- FORMULARIO ----------------
with st.form("simulador"):
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    edad = st.number_input("Edad actual", min_value=18, max_value=67, value=45)
    cotizados = st.number_input("Años cotizados", min_value=0, max_value=50, value=20)
    base = st.number_input("Base reguladora mensual (€)", min_value=500, value=1800)

    tipo = st.selectbox(
        "Tipo de jubilación",
        ["Ordinaria", "Anticipada"]
    )

    calcular = st.form_submit_button("Simular")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CÁLCULO ----------------
if calcular:
    if tipo == "Ordinaria":
        porcentaje = min(100, cotizados * 2)
    else:
        porcentaje = min(85, cotizados * 1.8)

    pension = base * porcentaje / 100

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Resultado")
    st.write(f"**Porcentaje aplicado:** {porcentaje:.1f}%")
    st.write(f"**Pensión estimada:** {pension:.2f} € / mes")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- PDF ----------------
    def generar_pdf():
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(tmp.name, pagesize=A4)
        c.setFont("Helvetica", 12)

        c.drawString(50, 800, "SIMULADOR DE JUBILACIÓN")
        c.drawString(50, 760, f"Edad actual: {edad}")
        c.drawString(50, 740, f"Años cotizados: {cotizados}")
        c.drawString(50, 720, f"Base reguladora: {base} €")
        c.drawString(50, 700, f"Tipo de jubilación: {tipo}")
        c.drawString(50, 660, f"Porcentaje aplicado: {porcentaje:.1f}%")
        c.drawString(50, 640, f"Pensión estimada: {pension:.2f} € / mes")

        c.showPage()
        c.save()
        return tmp.name

    pdf_path = generar_pdf()

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Descargar PDF",
            data=f,
            file_name="simulacion_jubilacion.pdf",
            mime="application/pdf"
        )
