import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Simulador Profesional de Jubilación",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# ESTILOS CSS
# -------------------------------------------------
st.markdown("""
<style>

/* Fondo azul celeste */
.stApp {
    background-color: #eaf3fb;
}

/* Tarjetas */
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
    font-size: 36px;
}
h2, h3 {
    color: #1e293b;
}

/* Inputs blancos */
div[data-baseweb="input"] input {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}

/* SELECT: anchura y altura corregidas */
div[data-baseweb="select"] {
    width: 60% !important;   /* 👈 AQUÍ controlamos el ancho */
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    min-height: 34px !important;
    font-size: 14px !important;
}

/* Resultado */
.resultado {
    background-color: #d1fae5;
    padding: 32px;
    border-radius: 18px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #065f46;
}

/* Botones */
div.stButton > button {
    background-color: #2563eb;
    color: white;
    font-size: 15px;
    padding: 8px 16px;
    border-radius: 10px;
    border: none;
    font-weight: 500;
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

# -------------------------------------------------
# CABECERA
# -------------------------------------------------
st.title("Simulador Profesional de Jubilación")
st.caption("Herramienta de asesoramiento previsional para clientes")

st.divider()

# -------------------------------------------------
# FORMULARIO
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

    submitted = st.form_submit_button("📊 Simular jubilación")

# -------------------------------------------------
# CÁLCULO
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

    # RESULTADO
    st.markdown(f"""
    <div class="resultado">
        Pensión estimada<br>
        {pension_mensual:,.2f} € / mes
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Detalle del cálculo")

    st.write(f"Cliente: **{nombre}**")
    st.write(f"Modalidad: **{tipo_jubilacion}**")
    st.write(f"Años cotizados: **{años_cotizados}**")
    st.write(f"Porcentaje aplicado: **{porcentaje*100:.1f}%**")

    if tipo_jubilacion == "Anticipada":
        st.write("Penalización por jubilación anticipada: **-15%**")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------
    # GENERAR PDF
    # -------------------------------------------------
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Simulación de Jubilación</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Cliente: {nombre}", styles["Normal"]))
    story.append(Paragraph(f"Edad actual: {edad_actual}", styles["Normal"]))
    story.append(Paragraph(f"Años cotizados: {años_cotizados}", styles["Normal"]))
    story.append(Paragraph(f"Modalidad: {tipo_jubilacion}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Pensión estimada:</b> {pension_mensual:,.2f} € / mes", styles["Normal"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Simulación orientativa. No constituye cálculo oficial.", styles["Italic"]))

    doc.build(story)
    buffer.seek(0)

    st.download_button(
        label="📄 Descargar PDF",
        data=buffer,
        file_name="simulacion_jubilacion.pdf",
        mime="application/pdf"
    )

# -------------------------------------------------
# LEGAL
# -------------------------------------------------
st.markdown("""
<div class="footer">
Simulación orientativa. No constituye oferta vinculante ni cálculo oficial de la Seguridad Social.
</div>
""", unsafe_allow_html=True)




