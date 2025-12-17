```python
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Simulador Profesional de Jubilación",
    page_icon="📊",
    layout="wide"
)

# ---------- ESTILOS ----------
st.markdown("""
<style>
body { background-color: #f5f6fa; }
.block-container { padding: 2rem 3rem; }
.card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}
.title {
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    font-size: 20px;
    color: #555;
}
.result {
    font-size: 40px;
    font-weight: 700;
    color: #1a7f37;
}
.small {
    font-size: 14px;
    color: #777;
}
</style>
""", unsafe_allow_html=True)

# ---------- CABECERA ----------
col_logo, col_title = st.columns([1,4])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Logo_placeholder.png", width=90)
with col_title:
    st.markdown('<div class="title">Simulador Profesional de Jubilación</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Herramienta de asesoramiento financiero – Uso en oficina</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- DATOS CLIENTE ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👤 Datos del cliente")
    nombre = st.text_input("Nombre del cliente")
    nacimiento = st.number_input("Año de nacimiento", 1940, 2005, 1978)
    edad_jubilacion = st.selectbox("Edad de jubilación", [63, 64, 65, 66, 67], index=4)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📂 Cotización")
    anos_cotizados = st.number_input("Años cotizados", 0, 45, 15)
    base_mensual = st.number_input("Base de cotización mensual (€)", 500, 6000, 3000, step=50)
    tipo = st.radio("Tipo de jubilación", ["Ordinaria", "Anticipada"])
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CÁLCULOS ----------
def porcentaje_base(anos):
    if anos < 15:
        return 0
    elif anos >= 38:
        return 1
    else:
        return 0.5 + (anos - 15) * (0.5 / 23)

coef_anticipada = 0.85 if tipo == "Anticipada" else 1
porcentaje = porcentaje_base(anos_cotizados)
base_reguladora = base_mensual * 14
pension_anual = base_reguladora * porcentaje * coef_anticipada
pension_mensual = pension_anual / 14

# ---------- RESULTADOS ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📈 Resultado de la simulación")

if anos_cotizados < 15:
    st.error("❌ No alcanza el mínimo de años cotizados para acceder a pensión contributiva")
else:
    st.markdown(f'<div class="result">{pension_mensual:,.2f} € / mes</div>', unsafe_allow_html=True)
    st.write(f"Porcentaje aplicado: **{porcentaje*100:.1f}%**")
    if tipo == "Anticipada":
        st.write("Coeficiente reductor aplicado por jubilación anticipada")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- INFORME ----------
if st.button("📄 Generar informe para el cliente"):
    st.success("Informe generado correctamente (función ampliable a PDF)")

st.markdown("---")
st.markdown('<div class="small">Simulación orientativa. No sustituye el cálculo oficial de la Seguridad Social.</div>', unsafe_allow_html=True)
```

