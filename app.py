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
