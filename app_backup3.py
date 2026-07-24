# ============================================
# INICIALIZACIONES GLOBALES (ANTES DEL BLOQUE 1)
# ============================================

brecha = 0.0
capital_necesario = 0.0
capital_real_final_cliente = 0.0
capital_real_final_recom = 0.0
tipo_brecha_descripcion = ""
evolucion_cliente = []
evolucion_recom = [{"mes": 0, "aportada": 0, "total": 0, "inflacion": 0, "neta": 0}]

# ============================================
# BLOQUE 1 — IMPORTS, CSS Y FUNCIONES BASE
# ============================================

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime
# ============================================================
# 🟦 ESTILOS GLOBALES SRG
# ============================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #101522 !important;
    color: #EAF2FF !important;
}

div[data-testid="stMetricValue"] {
    color: #00BFFF !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricLabel"] {
    color: #A8DFFF !important;
}

input[type="number"], input[type="text"], select, textarea {
    background-color: #141A2B !important;
    border: 1px solid #00BFFF !important;
    color: #EAF2FF !important;
}

h1, h2, h3, h4 {
    color: #EAF2FF !important;
}

.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
}

button[kind="primary"] {
    background-color: #0055A4 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
}

button[kind="secondary"] {
    background-color: #1E3A5F !important;
    color: #EAF2FF !important;
}

.srg-box {
    background-color: #182235 !important;
    border: 1px solid #00BFFF !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    margin-bottom: 12px !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Simulador de Jubilación SRG",
    page_icon="💼",
    layout="wide"
)
st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    color: white !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.9rem !important;
    color: #00cc66 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ======== NÚMEROS AZUL FUTURISTA (Cloud + Local) ======== */
input[type="number"] {
    color: #00BFFF !important;
    font-weight: 600 !important;
}

/* ======== PLACEHOLDER TAMBIÉN AZUL CLARO ======== */
input[type="number"]::placeholder {
    color: #A8DFFF !important;
    opacity: 0.7 !important;
}

/* ======== INPUTS OSCUROS PARA QUE EL AZUL RESALTE ======== */
input[type="number"] {
    background-color: #0C1426 !important;
    border: 1px solid #00BFFF !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ======== NÚMEROS AZUL FUTURISTA — Streamlit Cloud ======== */
input[type="number"], 
input[type="number"]::-webkit-inner-spin_button, 
input[type="number"]::-webkit-outer-spin_button {
    color: #00BFFF !important;
    font-weight: 600 !important;
}

/* ======== Forzar color del texto dentro del input ======== */
div[data-baseweb="input"] input {
    color: #00BFFF !important;
}

/* ======== Fondo oscuro y borde neón ======== */
div[data-baseweb="input"] {
    background-color: #0C1426 !important;
    border: 1px solid #00BFFF !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ======== TOOLTIP: fondo oscuro y texto claro ======== */
[data-testid="stTooltipHoverTarget"] div {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4);
    padding: 6px 10px !important;
    border-radius: 6px !important;
}

/* ======== ICONO DEL TOOLTIP: azul neón ======== */
[data-testid="stTooltipIcon"] svg {
    fill: #00BFFF !important;
    filter: drop-shadow(0 0 6px rgba(0,191,255,0.6));
}

/* ======== INPUTS: fondo oscuro uniforme ======== */
input[type="number"], input[type="text"], select, textarea {
    background-color: #0C1426 !important;
    border: 1px solid #00BFFF !important;
    color: #EAF2FF !important;
}

/* ======== PLACEHOLDER: texto visible ======== */
input::placeholder {
    color: #EAF2FF !important;
    opacity: 0.6 !important;
}

</style>
""", unsafe_allow_html=True)

if "mostrar_explicacion" not in st.session_state:
    st.session_state.mostrar_explicacion = False

st.markdown("""
<style>

/* TOOLTIP: fondo oscuro y texto claro */
[data-testid="stTooltipHoverTarget"] div {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4);
    padding: 6px 10px !important;
    border-radius: 6px !important;
}

/* ICONO DEL TOOLTIP: azul futurista */
[data-testid="stTooltipIcon"] svg {
    fill: #00BFFF !important;
    filter: drop-shadow(0 0 6px rgba(0,191,255,0.6));
}

/* INPUTS: fondo oscuro */
input[type="number"], input[type="text"], select, textarea {
    background-color: #0C1426 !important;
    border: 1px solid #00BFFF !important;
    color: #EAF2FF !important;
}

/* NÚMEROS: azul futurista */
input[type="number"] {
    color: #00BFFF !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&display=swap');

/* BLOQUE ANTI-FLASH — Fondo oscuro desde el primer frame */
html, body, #root, section.main, div[data-testid="stAppViewContainer"] {
    background-color: #05070D !important;
    background-image: none !important;
    transition: none !important;
    color: #EAF2FF !important;
}

/* TOOLTIP SRG FINAL — Fondo oscuro y texto visible */
[data-testid="stTooltipHoverTarget"] div,
[data-testid="stTooltipHoverTarget"]:hover div {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4);
    padding: 6px 10px !important;
    border-radius: 6px !important;
    transition: background-color 0.3s ease-in-out;
}
[data-testid="stTooltipHoverTarget"] * {
    color: #EAF2FF !important;
    background-color: transparent !important;
    opacity: 1 !important;
}
[data-testid="stTooltipHoverTarget"] p,
[data-testid="stTooltipHoverTarget"] span,
[data-testid="stTooltipHoverTarget"] li {
    color: #EAF2FF !important;
    font-size: 0.9rem !important;
    line-height: 1.4 !important;
}

/* TOOLTIP SRG UNIVERSAL — Hover personalizado */
.srg-tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
    color: #00BFFF;
    font-weight: 500;
}
.srg-tooltip .srg-tooltip-text {
    visibility: hidden;
    width: 260px;
    background-color: #0A0F1F;
    color: #EAF2FF;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    border: 1px solid #00BFFF;
    box-shadow: 0 0 10px rgba(0,191,255,0.4);
    position: absolute;
    z-index: 999;
    top: 24px;
    left: 0;
    font-size: 0.85rem;
}
.srg-tooltip:hover .srg-tooltip-text {
    visibility: visible;
}

/* HEADER SRG */
.srg-header {
    padding: 14px 24px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #003366, #0055A4);
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}
.srg-header-inner {
    max-width: 980px;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    text-align: center;
}
.srg-header-title-main {
    font-family: 'Dancing Script', cursive !important;
    font-size: 3.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1.1;
}
.srg-header-title-sub {
    font-family: 'Dancing Script', cursive !important;
    font-size: 1.8rem;
    font-weight: 400;
    color: #d0d8e8;
    margin-top: 6px;
}

/* TITULOS Y BLOQUES */
.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

/* SELECTBOX Y RADIO SRG OSCUROS */
div[data-baseweb="select"] > div {
    background-color: #0A0F1F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
    box-shadow: 0 0 6px rgba(0,191,255,0.3) !important;
}
div[data-baseweb="select"] span {
    color: #EAF2FF !important;
}
div[data-baseweb="select"] svg {
    fill: #00BFFF !important;
}
div[data-baseweb="radio"] {
    background-color: #0A0F1F !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
    padding: 6px 10px !important;
    box-shadow: 0 0 6px rgba(0,191,255,0.3) !important;
}
div[data-baseweb="radio"] label {
    color: #EAF2FF !important;
    font-size: 0.9rem !important;
}
div[data-baseweb="radio"] svg {
    fill: #00BFFF !important;
}

/* FOOTER SRG */
.srg-footer {
    margin-top: 30px;
    padding: 16px 12px;
    background: linear-gradient(135deg, #003366, #0055A4);
    color: #ffffff;
    text-align: center;
    font-size: 0.85rem;
    border-radius: 6px 6px 0 0;
}
.srg-footer a {
    color: #ffffff;
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)
srg_css = """
<style>
.srg-header-box {
    background: linear-gradient(90deg, #0b3c5d, #3282b8);
    color: #ffffff;
    padding: 18px 22px;
    border-radius: 10px;
    margin-bottom: 18px;
}
.srg-header-box h4 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
}
.srg-header-box p {
    margin: 4px 0 0 0;
    font-size: 0.9rem;
    opacity: 0.9;
}
.srg-card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}
.srg-card h4 {
    margin: 0 0 8px 0;
    font-size: 1rem;
    font-weight: 600;
}
</style>
"""
st.markdown(srg_css, unsafe_allow_html=True)


tooltip_fix = """
<script>
const observer = new MutationObserver(() => {
  document.querySelectorAll('[data-testid="stTooltipHoverTarget"] div').forEach(el => {
    el.style.backgroundColor = '#0A1A2F';
    el.style.color = '#EAF2FF';
    el.style.border = '1px solid #00BFFF';
    el.style.boxShadow = '0 0 12px rgba(0,191,255,0.4)';
    el.style.borderRadius = '6px';
    el.style.padding = '6px 10px';
  });
});
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""
st.markdown(tooltip_fix, unsafe_allow_html=True)

header_html = """
<div class="srg-header">
  <div class="srg-header-inner">
      <div>
        <div class="srg-header-title-main">Simulador de Jubilación SRG</div>
        <div class="srg-header-title-sub">Planificación de tu pensión de forma clara y profesional</div>
      </div>
  </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
# 🔧 Ajuste visual para títulos dentro de expanders
st.markdown("""
<style>
div[data-testid="stExpander"] h1,
div[data-testid="stExpander"] h2,
div[data-testid="stExpander"] h3 {
    font-size: 16px !important;
    font-weight: 600 !important;
    margin-top: 4px !important;
    margin-bottom: 4px !important;
}
</style>
""", unsafe_allow_html=True)


def calcular_objetivo_y_gastos_futuros(ingresos_hoy, gastos_hoy, pct, inflacion, anos):
    factor = (1 + inflacion/100) ** anos
    ingresos_fut = ingresos_hoy * factor
    gastos_fut = gastos_hoy * (pct/100) * factor
    return ingresos_fut, gastos_fut

def calcular_evolucion_mensual(anos_hasta_jub, rentabilidad_anual_pct, inflacion_anual_pct, aportacion):
    meses = int(max(0, anos_hasta_jub)) * 12
    if meses < 1:
        meses = 1

    r_mensual = (1 + rentabilidad_anual_pct/100) ** (1/12) - 1
    infl_mensual = (1 + inflacion_anual_pct/100) ** (1/12) - 1

    capital = 0.0
    lista = []

    for mes in range(meses + 1):
        if mes > 0:
            capital = (capital + aportacion) * (1 + r_mensual)

        capital_aportado = aportacion * mes
        capital_real = capital / ((1 + infl_mensual) ** mes) if mes > 0 else 0.0
        inflacion_perdida = capital - capital_real

        lista.append({
            "mes": mes,
            "aportada": capital_aportado,
            "total": capital,
            "inflacion": inflacion_perdida,
            "neta": capital_real
        })

    return lista

def tabla_mensual_y_anual_html(evolucion, anos_hasta_jub):
    if not evolucion or not isinstance(evolucion, list):
        return "<tr><td colspan='5'>No hay datos de evolución.</td></tr>"

    filas = []
    max_mes = min(12, len(evolucion) - 1)
    for mes in range(1, max_mes + 1):
        fila = evolucion[mes]
        aport = fila.get('aportada', 0.0)
        tot = fila.get('total', 0.0)
        infl = fila.get('inflacion', 0.0)
        net = fila.get('neta', tot - infl)
        filas.append(
            f"<tr><td>{mes} (mes)</td><td>{aport:,.0f} €</td><td>{tot:,.0f} €</td><td>{infl:,.0f} €</td><td>{net:,.0f} €</td></tr>"
        )

    for ano in range(1, int(max(1, anos_hasta_jub)) + 1):
        idx = ano * 12
        if idx < len(evolucion):
            fila = evolucion[idx]
            aport = fila.get('aportada', 0.0)
            tot = fila.get('total', 0.0)
            infl = fila.get('inflacion', 0.0)
            net = fila.get('neta', tot - infl)
            filas.append(
                f"<tr><td>{ano} (año)</td><td>{aport:,.0f} €</td><td>{tot:,.0f} €</td><td>{infl:,.0f} €</td><td>{net:,.0f} €</td></tr>"
            )

    return "\n".join(filas)

def marca_agua_srg():
    return """
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.06;
        z-index: 0;
        background-image: repeating-linear-gradient(
            -45deg,
            transparent 0 80px,
            #000000 80px 82px
        );
        color: #000;
        font-size: 120px;
        text-align: center;
        line-height: 200px;
        transform: rotate(-30deg);
    ">
        SRG SRG SRG SRG SRG SRG SRG
    </div>
    """

# ============================================
# BLOQUE 2 — INTERFAZ PRINCIPAL (PARTE 1)
# ============================================

col1, col2, col3, col4 = st.columns(4)

# ===== DATOS PERSONALES =====
if "edad_actual_input" not in st.session_state:
    st.session_state.edad_actual_input = 16
if "edad_prevista_jub_input" not in st.session_state:
    st.session_state.edad_prevista_jub_input = 17
if "esperanza_vida_input" not in st.session_state:
    st.session_state.esperanza_vida_input = 75

with col1:
    st.markdown('<div class="srg-title">Datos personales</div>', unsafe_allow_html=True)
    st.caption("Información básica necesaria para calcular tu horizonte de jubilación.")

    edad_actual = st.number_input(
        "Edad actual",
        min_value=16,
        max_value=70,
        value=st.session_state.edad_actual_input,
        help="Tu edad hoy. Se usa para calcular cuántos años faltan hasta la jubilación.",
        key="edad_actual_input"
    )

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
        min_value=edad_actual + 1,
        max_value=75,
        value=max(edad_actual + 1, st.session_state.edad_prevista_jub_input),
        help="Edad a la que deseas jubilarte. No puede ser menor o igual que tu edad actual.",
        key="edad_prevista_jub_input"
    )

    esperanza_vida = st.number_input(
        "Esperanza de vida",
        min_value=75,
        max_value=100,
        value=st.session_state.esperanza_vida_input,
        help="Estimación de años que vivirás según estadísticas.",
        key="esperanza_vida_input"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# Correcciones de coherencia
if edad_prevista_jub <= edad_actual:
    edad_prevista_jub = edad_actual + 1
if esperanza_vida <= edad_prevista_jub:
    esperanza_vida = edad_prevista_jub + 1

# ===== COTIZACIÓN =====
if "anos_cotizados_hoy_input" not in st.session_state:
    st.session_state.anos_cotizados_hoy_input = 0
if "anos_futuros_input" not in st.session_state:
    st.session_state.anos_futuros_input = 0

with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    st.caption("Tus años cotizados determinan si puedes acceder a modalidades anticipadas.")

    max_cotizables_hoy = max(0, edad_actual - 16)
    st.session_state.anos_cotizados_hoy_input = min(
        st.session_state.anos_cotizados_hoy_input, max_cotizables_hoy
    )

    anos_cotizados_hoy = st.number_input(
        "Años cotizados hoy",
        min_value=0,
        max_value=max_cotizables_hoy,
        value=st.session_state.anos_cotizados_hoy_input,
        help="Años cotizados a la Seguridad Social.",
        key="anos_cotizados_hoy_input"
    )

    max_anos_futuros = max(0, edad_prevista_jub - edad_actual)
    st.session_state.anos_futuros_input = min(
        st.session_state.anos_futuros_input, max_anos_futuros
    )

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
        min_value=0,
        max_value=max_anos_futuros,
        value=st.session_state.anos_futuros_input,
        help="Años adicionales que seguirás cotizando.",
        key="anos_futuros_input"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Cálculos base del bloque 2
anos_totales = anos_cotizados_hoy + anos_futuros
anos_hasta_jub = max(1, edad_prevista_jub - edad_actual)
anos_jubilacion = max(1, esperanza_vida - edad_prevista_jub)


# ===== TIPO DE JUBILACIÓN =====
EDAD_LEGAL_2026 = 67

if "tipo_jubilacion_input" not in st.session_state:
    st.session_state.tipo_jubilacion_input = "Ordinaria"

with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    st.caption("Modalidad, requisitos, anticipos, penalizaciones y bonificaciones según normativa 2026.")
    st.markdown("<div style='margin-top: 7px; height: 18px;'></div>", unsafe_allow_html=True)

    with st.expander("📘 Selecciona modalidad y requisitos", expanded=False):

        opciones_jub = ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"]
        idx_tipo = opciones_jub.index(st.session_state.tipo_jubilacion_input)

        tipo_jubilacion = st.radio(
            "Tipo prevista",
            opciones_jub,
            index=idx_tipo,
            key="tipo_jubilacion_input"
        )

        modo_valido = True
        motivo_error = ""
        coef_ajuste = 1.0

        # ===== ORDINARIA =====
        if tipo_jubilacion == "Ordinaria":
            st.markdown("""
            #### 🟦 Jubilación ordinaria
            **Edad legal:** 67 años  
            **Requisitos:** mínimo 15 años cotizados  
            """)

            # Solo mostrar validaciones si el usuario ya introdujo datos reales
            if anos_totales > 0:
                if anos_totales < 15:
                    modo_valido = False
                    motivo_error = "Para la jubilación ordinaria necesitas al menos 15 años cotizados."

                elif edad_prevista_jub < EDAD_LEGAL_2026:
                    st.warning(
                        "La edad prevista es inferior a la edad legal. "
                        "Con estos datos, **pasarías a una jubilación anticipada voluntaria** con penalización."
                    )

        # ===== ANTICIPADA VOLUNTARIA =====
        elif tipo_jubilacion == "Anticipada voluntaria":
            st.markdown("""
            #### 🟧 Anticipada voluntaria
            **Adelanto máximo:** 24 meses  
            **Requisitos:** 35 años cotizados  
            """)

            if anos_totales > 0 and anos_totales < 35:
                modo_valido = False
                motivo_error = "Para la anticipada voluntaria necesitas 35 años cotizados."

            meses_anticipo = st.number_input("Meses de anticipo", 1, 24, 1)
            edad_prevista_jub = EDAD_LEGAL_2026 - meses_anticipo / 12

            if edad_prevista_jub < 63:
                modo_valido = False
                motivo_error = "La anticipada voluntaria solo puede aplicarse desde los 63 años."

            def coef_voluntaria(anos, meses):
                trimestres = meses // 3
                if anos < 38.5: red = 0.0525
                elif anos < 41.5: red = 0.0475
                elif anos < 44.5: red = 0.0425
                else: red = 0.0325
                return 1 - red * trimestres

            coef_ajuste = coef_voluntaria(anos_totales, meses_anticipo)

        # ===== ANTICIPADA INVOLUNTARIA =====
        elif tipo_jubilacion == "Anticipada involuntaria":
            st.markdown("""
            #### 🟥 Anticipada involuntaria
            **Adelanto máximo:** 48 meses  
            **Requisitos:** 33 años cotizados  
            """)

            if anos_totales > 0 and anos_totales < 33:
                modo_valido = False
                motivo_error = "Para la anticipada involuntaria necesitas 33 años cotizados."

            meses_anticipo = st.number_input("Meses de anticipo", 1, 48, 1)
            edad_prevista_jub = EDAD_LEGAL_2026 - meses_anticipo / 12

            if edad_prevista_jub < 61:
                modo_valido = False
                motivo_error = "La anticipada involuntaria solo puede aplicarse desde los 61 años."

            def coef_involuntaria(anos, meses):
                trimestres = meses // 3
                if anos < 38.5: red = 0.075
                elif anos < 41.5: red = 0.070
                elif anos < 44.5: red = 0.065
                else: red = 0.055
                return 1 - red * trimestres

            coef_ajuste = coef_involuntaria(anos_totales, meses_anticipo)

        # ===== DEMORADA =====
        elif tipo_jubilacion == "Demorada":
            st.markdown("""
            #### 🟩 Jubilación demorada
            **Edad legal:** 67 años  
            **Bonificación:** +4% por cada año de demora  
            """)

            if anos_totales > 0 and anos_totales < 15:
                modo_valido = False
                motivo_error = "Para la jubilación demorada necesitas al menos 15 años cotizados."

            elif edad_actual < 60:
                modo_valido = False
                motivo_error = "La jubilación demorada solo aplica si ya estás próximo a la edad legal."

            else:
                meses_demora = st.number_input("Meses de demora", 1, 120, 1)
                anos_demora = meses_demora / 12
                coef_ajuste = 1 + anos_demora * 0.04
                edad_prevista_jub = EDAD_LEGAL_2026 + anos_demora

                st.metric("Meses de demora", f"{meses_demora} meses")
                st.metric("Bonificación aplicada", f"+{(coef_ajuste - 1) * 100:.1f}%")
                st.metric("Edad prevista de jubilación", f"{edad_prevista_jub:.1f} años")

                if edad_prevista_jub <= EDAD_LEGAL_2026:
                    modo_valido = False
                    motivo_error = "La edad prevista debe ser mayor que la edad legal."

        # ===== WARNING SRG (POSICIÓN CORRECTA) =====
        if not modo_valido:
            st.markdown(
                f"""
                <div style="
                    background-color:#b30000;
                    color:white;
                    padding:10px 15px;
                    border-radius:6px;
                    margin-top:10px;
                    font-weight:500;
                    text-align:center;">
                    ⚠️ {motivo_error}
                </div>
                """,
                unsafe_allow_html=True
            )
       
# ============================================================
# 🟦 Mensaje SRG para informes (post-selección)
# ============================================================

mensaje_jubilacion_srg = ""

# Caso ordinaria con edad inferior a la legal
if tipo_jubilacion == "Ordinaria" and edad_prevista_jub < EDAD_LEGAL_2026:
    mensaje_jubilacion_srg = (
        "La edad prevista es inferior a la edad legal. "
        "Con estos datos, pasarías a una jubilación anticipada voluntaria con penalización."
    )

# Caso anticipada voluntaria
elif tipo_jubilacion == "Anticipada voluntaria":
    mensaje_jubilacion_srg = (
        f"Has seleccionado jubilación anticipada voluntaria con un anticipo de {meses_anticipo} meses."
    )

# Caso anticipada involuntaria
elif tipo_jubilacion == "Anticipada involuntaria":
    mensaje_jubilacion_srg = (
        f"Has seleccionado jubilación anticipada involuntaria con un anticipo de {meses_anticipo} meses."
    )

# Caso demorada
elif tipo_jubilacion == "Demorada":
    mensaje_jubilacion_srg = (
        f"Has seleccionado jubilación demorada con una bonificación del {(coef_ajuste - 1) * 100:.1f}%."
    )
            

# ===== INGRESOS Y GASTOS =====
with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
    st.caption("Tus ingresos y gastos actuales nos permiten estimar tu objetivo económico futuro.")

    ingresos = st.number_input(
        "Ingresos mensuales (€)",
        min_value=0,
        max_value=20000,
        value=0,
        help="Tus ingresos netos actuales.",
        key="ingresos_input"
    )

    if "gastos_input" not in st.session_state:
        st.session_state.gastos_input = 0

    st.session_state.gastos_input = min(st.session_state.gastos_input, ingresos)

    gastos = st.number_input(
        "Gastos mensuales (€)",
        min_value=0,
        max_value=20000,
        value=st.session_state.gastos_input,
        help="Tus gastos mensuales actuales.",
        key="gastos_input"
    )

    if gastos > ingresos:
        st.warning("Has indicado más gastos que ingresos. Ajustamos los gastos al máximo igual a tus ingresos.")
        gastos = ingresos

    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# ===== PROTECCIÓN DE VARIABLES (EVITA NameError) =====
if "ingresos" not in locals():
    ingresos = 0
if "gastos" not in locals():
    gastos = 0

# ============================================
# BLOQUE 3 — PENSIÓN, OBJETIVO Y BRECHA (VERSIÓN PULIDA SRG)
# ============================================

# Límites reales de la Seguridad Social para 2026
PENSION_MAX_2026 = 3359.60
BASE_MAX_ESPANA_2026 = 4720
EXTRA_REVAL = 0.00115

colA, colB, colC, colD = st.columns(4)

# ============================================================
# 🟦 1. PENSIÓN E INFLACIÓN — SOLO BASE REGULADORA SRG
# ============================================================
with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    st.caption("Aquí calculamos tu pensión futura y ajustamos todo al coste de la vida.")

    # -----------------------------
    # INPUTS (van arriba)
    # -----------------------------
    st.markdown("#### Base reguladora SRG (automática)")
    st.caption("La aplicación calcula tu base reguladora automáticamente. No tienes que saberla ni calcularla.")

    salario_actual = st.number_input(
        "Salario mensual actual (€)",
        min_value=0,
        max_value=20000,
        value=0,
        help="Tu salario bruto mensual actual.",
        key="salario_actual_input"
    )

    crecimiento_salarial = st.number_input(
        "Crecimiento salarial anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.1,
        help="En España, el crecimiento salarial medio en 2026 ronda el 3 %. Dato basado en INE y Banco de España.",
        key="crecimiento_salarial_input"
    )

    ipc_actualizacion = st.number_input(
        "Actualización IPC anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.5,
        step=0.1,
        help="El IPC medio previsto para España en 2026 es del 2,5 %. Se usa para actualizar cotizaciones antiguas.",
        key="ipc_actualizacion_input"
    )

    # -----------------------------
    # CÁLCULO AUTOMÁTICO SRG
    # -----------------------------
    meses_totales = 29 * 12
    bases = []
    for i in range(meses_totales):
        anos_pasados = (meses_totales - 1 - i) / 12
        salario_estimado = salario_actual / ((1 + crecimiento_salarial/100) ** anos_pasados) if salario_actual > 0 else 0
        bases.append(salario_estimado)

    bases_actualizadas = []
    for i, base_i in enumerate(bases):
        anos_pasados = (meses_totales - 1 - i) / 12
        factor_ipc = (1 + ipc_actualizacion/100) ** anos_pasados
        bases_actualizadas.append(base_i * factor_ipc)

    mejores_322 = sorted(bases_actualizadas)[24:]
    base = sum(mejores_322) / 322 if len(mejores_322) == 322 else (sum(mejores_322) / max(1, len(mejores_322)))

    # Límite legal
    if base > BASE_MAX_ESPANA_2026:
        base = BASE_MAX_ESPANA_2026
        st.warning(f"La base reguladora supera el límite legal ({BASE_MAX_ESPANA_2026:,.0f} €). Se ajusta automáticamente.")

    # -----------------------------
    # RESULTADO PRINCIPAL (arriba)
    # -----------------------------
    st.markdown(f'<div class="msg-green-srg">Base reguladora calculada: {base:,.0f} €</div>', unsafe_allow_html=True)

    # -----------------------------
    # INPUTS ADICIONALES
    # -----------------------------
    inflacion = st.number_input(
        "Inflación anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.4,
        step=0.1,
        help="La inflación esperada en España para 2026 es del 2,4 %. Dato del Banco de España.",
        key="inflacion_input"
    )

    reval = st.number_input(
        "Revalorización anual pensión (%)",
        min_value=0.0,
        max_value=5.0,
        value=2.8,
        step=0.1,
        help="Las pensiones se revalorizan según el IPC medio del año anterior. En 2026 la subida aplicada fue del 2,8 %.",
        key="reval_input"
    )

    # -----------------------------
    # EXPLICACIONES (abajo)
    # -----------------------------
    with st.expander("📘 ¿Cómo calcula SRG tu base reguladora?"):
        st.markdown(f"""
        - Partimos de tu salario actual: **{salario_actual:,.0f} €**  
        - Retrocedemos año a año aplicando tu crecimiento salarial  
        - Actualizamos esas cotizaciones antiguas con el IPC  
        - Nos quedamos con las **322 mejores cotizaciones**  
        - La media es tu **base reguladora SRG**
        """)

    st.markdown(
        f'<div class="msg-ok-srg">📌 Límite máximo de cotización: <b>{BASE_MAX_ESPANA_2026:,.0f} €</b> al mes.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="msg-ok-srg">📌 Límite máximo de pensión: <b>{PENSION_MAX_2026:,.0f} €</b> al mes.</div>',
        unsafe_allow_html=True
    )

    with st.expander("📘 ¿Por qué existen límites máximos?"):
        st.markdown(f"""
        - Solo puedes cotizar hasta **{BASE_MAX_ESPANA_2026:,.0f} €**  
        - La pensión máxima es **{PENSION_MAX_2026:,.0f} €**
        """)

    with st.expander("📘 Inflación y revalorización"):
        st.markdown("""
        - La inflación mide cómo suben los precios  
        - La revalorización actualiza tu pensión cada año  
        """)

# ============================================================
# 🟦 2. RESUMEN PENSIÓN — EXPLICACIONES COLOQUIALES
# ============================================================
pct = min(1.0, anos_totales / 37) if modo_valido else 0.0
base_reguladora_ajustada = min(base, BASE_MAX_ESPANA_2026)
pension_hoy = base_reguladora_ajustada * pct * coef_ajuste
pension_futura_sin_tope = pension_hoy * ((1 + reval/100) ** anos_hasta_jub)

# Límite legal real: pensión máxima actualizada a futuro
pension_max_futura = PENSION_MAX_2026 * ((1 + inflacion/100 + EXTRA_REVAL) ** anos_hasta_jub)

# 🔧 Ajuste automático al límite legal
limite_aplicado = pension_futura_sin_tope > pension_max_futura
pension_futura = pension_max_futura if limite_aplicado else pension_futura_sin_tope

with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    st.caption("Tu pensión estimada según tus años cotizados y tu base reguladora.")

    # -----------------------------
    # ERROR SRG (igual que bloque anterior)
    # -----------------------------
    if not modo_valido:
        st.markdown(
            f"""
            <div style="
                background-color:#b30000;
                color:white;
                padding:10px 15px;
                border-radius:6px;
                margin-top:10px;
                font-weight:500;
                text-align:center;">
                ⚠️ {motivo_error}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # -----------------------------
        # MÉTRICAS (arriba)
        # -----------------------------
        st.metric("Porcentaje sobre base", f"{pct*100:,.1f} %")
        st.metric("Pensión ajustada hoy", f"{pension_hoy:,.0f} €")
        st.metric("Pensión futura estimada", f"{pension_futura:,.0f} €/mes")

        # 🔶 Aviso si se aplica el límite legal
        if limite_aplicado:
            st.warning(
                f"La pensión calculada (**{pension_futura_sin_tope:,.0f} €**) "
                f"supera el límite legal futuro. Se ajusta automáticamente a "
                f"**{pension_futura:,.0f} €**."
            )

        # -----------------------------
        # EXPLICACIONES (abajo)
        # -----------------------------
        with st.expander("📘 ¿De dónde sale cada número?"):
            st.markdown(f"""
### 🟦 ¿Cómo calcula la Seguridad Social tu pensión?

Tu pensión depende de tres elementos:

---

### 1️⃣ Tus años cotizados  
Has cotizado **{anos_totales} años**.  
Con esos años, la Seguridad Social te reconoce:  
**{pct*100:.1f}%** de la pensión completa sobre tu base reguladora.

---

### 2️⃣ Tu base reguladora  
Es la media de tus **322 mejores cotizaciones**.  
En tu caso, el simulador ha calculado una base reguladora de:  
**{base:,.0f} €**

---

### 3️⃣ Ajustes según tu tipo de jubilación  
La Seguridad Social aplica un ajuste según **cómo te jubiles**.  
Ese número (**{coef_ajuste:.3f}**) representa una **reducción o aumento** sobre la pensión completa.

A continuación tienes la explicación **según tu modalidad**:

---

## 🔵 Jubilación ordinaria (edad legal)
- No hay penalización ni bonificación.  
- El coeficiente suele ser **1.000**.  
- Significa: **“Tu pensión se calcula al 100 % según tus años cotizados.”**  
- El porcentaje **{pct*100:.1f}%** indica qué parte de la pensión completa te corresponde por tus años cotizados.

---

## 🟠 Jubilación anticipada voluntaria
Si decides jubilarte antes por decisión propia, la Seguridad Social aplica una **reducción proporcional**.

Penalizaciones típicas:
| Anticipo | Reducción |
|---------|-----------|
| 12 meses | 4% – 6% |
| 24 meses | 8% – 12% |
| 36 meses | 12% – 18% |
| 48 meses | 17% – 21% |

Tu coeficiente **{coef_ajuste:.3f}** equivale a una **reducción del {100 - coef_ajuste*100:.1f}%** sobre la pensión completa.

---

## 🔴 Jubilación anticipada involuntaria
Si el cese laboral **no fue voluntario**, la reducción es **más suave**.

Motivos reconocidos:
- Despido objetivo o colectivo  
- Cierre de empresa  
- Fuerza mayor  
- Fin de contrato sin renovación  
- Acoso laboral o violencia de género  

Penalizaciones típicas:
| Anticipo | Reducción |
|---------|-----------|
| 12 meses | 3% – 5% |
| 24 meses | 6% – 10% |
| 36 meses | 10% – 15% |
| 48 meses | 15% – 19% |

Tu coeficiente **{coef_ajuste:.3f}** refleja una **reducción del {100 - coef_ajuste*100:.1f}%**,  
que es **más baja que la penalización voluntaria**.

---

## 🟢 Jubilación demorada
Si decides jubilarte más tarde, la Seguridad Social **premia tu esfuerzo** con una bonificación.

Bonificaciones típicas:
| Retraso | Aumento |
|---------|---------|
| 12 meses | +4% |
| 24 meses | +8% |
| 36 meses | +12% |

Tu coeficiente **{coef_ajuste:.3f}** equivale a un **aumento del {(coef_ajuste*100 - 100):.1f}%** sobre la pensión completa.

---

## 🟦 En tu caso
Tu modalidad es **{tipo_jubilacion}**, con un coeficiente de **{coef_ajuste:.3f}**,  
lo que significa que tu pensión se ajusta según las condiciones de esa modalidad.

---

### 🟦 Resultado final  
Pensión hoy (antes de inflación):  
**{pension_hoy:,.0f} € / mes**

Pensión futura estimada (con revalorización y límite legal):  
**{pension_futura:,.0f} € / mes**

Así puedes ver exactamente de dónde sale cada número.
            """)

# ============================================================
# 🟦 3. TU NIVEL DE VIDA — EXPLICACIONES COLOQUIALES
# ============================================================
with colC:
    st.markdown('<div class="srg-title">Tu nivel de vida en la jubilación</div>', unsafe_allow_html=True)
    st.caption("Calculamos cuánto dinero necesitarás cada mes cuando te jubiles.")

    ingresos_hoy = ingresos
    gastos_hoy = gastos

    modo_nivel_vida = st.radio(
        "Modo de cálculo del nivel de vida",
        ["Objetivo económico (sobre ingresos)", "Gastos reales (sobre gastos)"],
        horizontal=True,
        key="modo_nivel_vida_input"
    )

    porcentaje_mantenimiento = st.number_input(
        "Porcentaje de mantenimiento del nivel de vida (%)",
        min_value=50,
        max_value=110,
        value=100,
        key="porcentaje_mantenimiento_input"
    )

    # Inflación anual y años hasta jubilación (ajusta nombres si en tu código son otros)
    # inflacion_anual debe estar definida antes (slider o input)
    # anos_hasta_jub = edad_prevista_jub - edad_actual debe existir antes
    factor_inflacion = (1 + inflacion / 100) ** anos_hasta_jub

    if "Objetivo económico" in modo_nivel_vida:
        nivel_vida_hoy = ingresos_hoy * (porcentaje_mantenimiento / 100)
    else:
        nivel_vida_hoy = gastos_hoy * (porcentaje_mantenimiento / 100)

    nivel_vida_futuro = nivel_vida_hoy * factor_inflacion

    st.metric("Lo que necesitarás cada mes al jubilarte", f"{nivel_vida_futuro:,.0f} €")

    # ============================
    # 📘 EXPANDER — EXPLICACIÓN CLARA PARA CLIENTES
    # ============================
    with st.expander("📘 ¿Cómo calculamos tu nivel de vida futuro?"):
        st.markdown(f"""
Aquí calculamos cuánto dinero necesitarás cada mes cuando te jubiles.

Lo hacemos a partir de tus ingresos o gastos actuales, aplicando el porcentaje que quieres mantener
y teniendo en cuenta la inflación acumulada hasta el año en que te jubiles.

Este valor representa el dinero que necesitarás cada mes para vivir con el mismo ritmo de vida que tienes hoy.

---

### 🟦 Datos utilizados en el cálculo

**Ingresos actuales:** {ingresos_hoy:,.0f} €  
**Gastos actuales:** {gastos_hoy:,.0f} €  
**Nivel de vida hoy:** {nivel_vida_hoy:,.0f} € / mes  
**Inflación anual considerada:** {inflacion:.1f}%  
**Años hasta tu jubilación:** {anos_hasta_jub} años  
**Factor acumulado por inflación:** x{factor_inflacion:.2f}

---

### 🟦 ¿De dónde sale el factor acumulado?

El factor x{factor_inflacion:.2f} indica cuánto habrán subido los precios desde hoy
hasta el año en que te jubiles.

Se calcula aplicando la inflación anual durante {anos_hasta_jub} años, con esta fórmula:

(1 + inflación anual) elevado al número de años hasta la jubilación.

En tu caso:

(1 + {inflacion/100:.4f}) elevado a {anos_hasta_jub} años = x{factor_inflacion:.2f}

Esto significa que dentro de {anos_hasta_jub} años, necesitarás aproximadamente
{(factor_inflacion - 1) * 100:.1f}% más dinero para mantener el mismo nivel de vida que hoy.

---

### 🟦 Resultado final

En el año de tu jubilación, esto equivale a:  
**{nivel_vida_futuro:,.0f} € / mes**
        """)

# ============================================================
# 🟩 CÁLCULO DEL NIVEL DE VIDA FUTURO — BASES PARA LA BRECHA
# ============================================================

pct_nivel_vida = porcentaje_mantenimiento

nivel_vida_futuro_objetivo = ingresos_hoy * (pct_nivel_vida / 100) * factor_inflacion
nivel_vida_futuro_gastos = gastos_hoy * (pct_nivel_vida / 100) * factor_inflacion

# ============================================================
# 🟦 4. BRECHA — EXPLICACIONES COLOQUIALES
# ============================================================
with colD:
    st.markdown('<div class="srg-title">Brecha</div>', unsafe_allow_html=True)
    st.caption("Aquí vemos si tu pensión futura cubre tu nivel de vida… o si falta dinero.")

    modo_brecha = st.radio(
        "¿Qué quieres cubrir?",
        ["Objetivo económico", "Gastos reales"],
        horizontal=True,
        key="modo_brecha_input"
    )

    # ============================
    # LÓGICA DEL SELECTOR
    # ============================
    if modo_brecha == "Objetivo económico":
        nivel_usado = nivel_vida_futuro_objetivo
        texto_modo = (
            "Tu nivel de vida futuro se calcula a partir de tus ingresos actuales, "
            "actualizados a precios del año en que te jubiles."
        )
    else:
        nivel_usado = nivel_vida_futuro_gastos
        texto_modo = (
            "Tu nivel de vida futuro se calcula a partir de tus gastos actuales, "
            "actualizados a precios del año en que te jubiles."
        )

    # ============================
    # CÁLCULO DE BRECHA
    # ============================
    brecha = max(0.0, nivel_usado - pension_futura)

    # ============================
    # VISUALIZACIÓN SRG
    # ============================
    st.metric("Brecha mensual a cubrir", f"{brecha:,.0f} €")
    st.caption(texto_modo)

    # 🔵 NUEVAS MÉTRICAS PARA QUE EL CLIENTE ENTIENDA DE DÓNDE SALE TODO
    st.metric("Nivel de vida futuro (ingresos)", f"{nivel_vida_futuro_objetivo:,.0f} €")
    st.metric("Nivel de vida futuro (gastos)", f"{nivel_vida_futuro_gastos:,.0f} €")

    # ============================
    # 📘 EXPANDER — EXPLICACIÓN CLARA PARA CLIENTES
    # ============================
    with st.expander("📘 ¿Qué es la brecha?"):
        st.markdown(f"""
Aquí comparamos lo que necesitarás cada mes cuando te jubiles con la pensión que tendrás.

La brecha es la diferencia entre esas dos cifras:

- Si tu pensión es menor que lo que necesitarás, aparece una brecha mensual a cubrir.
- Si tu pensión es igual o mayor, significa que tu nivel de vida está asegurado.

---

**Nivel de vida futuro usado en el cálculo:** {nivel_usado:,.0f} € / mes  
**Pensión futura estimada:** {pension_futura:,.0f} € / mes  

**Brecha mensual:** {brecha:,.0f} € / mes
        """)




import pandas as pd
import plotly.graph_objects as go


# ============================================================
# BLOQUE 4 — SIMULACIÓN DE AHORRO PERSONALIZADA SRG
# ============================================================

st.markdown("""
<div style='background: linear-gradient(90deg, #0f3b73 0%, #1e5aa8 100%);
            border-radius: 8px; padding: 10px 18px; text-align: center;
            font-family: "Poppins", "Segoe UI", sans-serif; color: #ffffff;'>
    <h2 style='font-size: 20px; font-weight: 600; margin-bottom: 4px; letter-spacing: 0.5px;'>
        Simulación de ahorro personalizada SRG
    </h2>
    <p style='font-size: 14px; font-weight: 400; margin: 0;'>
        Este bloque te muestra si tu pensión cubrirá tu nivel de vida y cuánto deberías ahorrar para garantizar tu tranquilidad futura.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 🟦 PANEL ALINEADO SRG — RESUMEN DE TU SITUACIÓN ACTUAL
# ============================================================

fila1_col1, fila1_col2, fila1_col3 = st.columns(3)

with fila1_col1:
    st.markdown("### 💰 Pensión futura estimada")
    st.markdown(f"<h2 style='color:#00cc66; margin-top:-10px;'>{pension_futura:,.0f} €</h2>", unsafe_allow_html=True)

with fila1_col2:
    st.markdown("### 🏠 Nivel de vida futuro")
    st.markdown(f"<h2 style='color:#00cc66; margin-top:-10px;'>{nivel_vida_futuro:,.0f} €</h2>", unsafe_allow_html=True)

with fila1_col3:
    st.markdown("### 📉 Brecha mensual")
    st.markdown(f"<h2 style='color:#00cc66; margin-top:-10px;'>{brecha:,.0f} €</h2>", unsafe_allow_html=True)


fila2_col1, fila2_col2, fila2_col3 = st.columns(3)

with fila2_col1:
    st.markdown("### ⏳ Años hasta tu jubilación")
    st.markdown(f"<h2 style='color:#00cc66; margin-top:-10px;'>{anos_hasta_jub}</h2>", unsafe_allow_html=True)

with fila2_col2:
    st.markdown("### 📈 Inflación anual estimada")
    st.markdown(f"<h2 style='color:#00cc66; margin-top:-10px;'>{inflacion:.1f} %</h2>", unsafe_allow_html=True)

capital_objetivo = brecha * 12 * anos_hasta_jub
with fila2_col3:
    st.markdown("### 🎯 Capital objetivo aproximado")
    st.markdown(f"<h2 style='color:#00cc66; margin-top:-10px;'>{capital_objetivo:,.0f} €</h2>", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #1e3a5f; margin-top:15px; margin-bottom:15px;'>", unsafe_allow_html=True)


# ============================================================
# 🟦 3. PARÁMETROS DEL PLAN — INTELIGENTE SRG
# ============================================================

st.markdown("""
<div class='srg-box'>
    <h4>Parámetros del plan de ahorro</h4>
    <p>El simulador SRG adapta automáticamente tu plan según exista brecha o no.</p>
</div>
""", unsafe_allow_html=True)

rentabilidad_base = 4.0  # valor por defecto si aún no se ha definido
inflacion_base = inflacion

# ============================================================
# 🟦 CASO 1 — HAY BRECHA → calcular cuota recomendada
# ============================================================

if brecha > 0:

    st.error("Tu pensión no cubre tu nivel de vida futuro.")
    st.info("💡 Vamos a calcular la cuota mensual recomendada para cubrir tu brecha.")

    colA, colB = st.columns(2)
    with colA:
        aportacion_inicial = st.number_input("Aportación inicial (€)", min_value=0.0, value=0.0, step=100.0)
    with colB:
        rentabilidad = st.number_input("Rentabilidad media anual (%)", min_value=0.0, value=rentabilidad_base, step=0.1)
        inflacion_media = st.number_input("Inflación media anual (%)", min_value=0.0, value=inflacion_base, step=0.1)

else:
    # ============================================================
    # 🟦 CASO 2 — NO HAY BRECHA → modo libre
    # ============================================================
    st.success("Tu pensión cubrirá tu nivel de vida. No aparece brecha mensual.")
    st.info("Puedes diseñar un plan de ahorro voluntario para tus objetivos personales.")

    colA, colB = st.columns(2)
    with colA:
        aportacion_inicial = st.number_input("Aportación inicial (€)", min_value=0.0, value=1000.0, step=100.0)
        rentabilidad = st.number_input("Rentabilidad media anual (%)", min_value=0.0, value=rentabilidad_base, step=0.1)
    with colB:
        inflacion_media = st.number_input("Inflación media anual (%)", min_value=0.0, value=inflacion_base, step=0.1)

# ============================================================
# 🔥 SINCRONIZACIÓN COMPLETA DE CUOTAS SRG
# ============================================================

r_mensual = rentabilidad / 100 / 12
n_meses = anos_hasta_jub * 12
capital_objetivo = brecha * 12 * anos_hasta_jub

# ============================================================
# 🟦 Cuota recomendada y entrada manual
# ============================================================

if brecha > 0:
    cuota_recomendada = (
        (capital_objetivo - aportacion_inicial * (1 + r_mensual) ** n_meses) * r_mensual
    ) / ((1 + r_mensual) ** n_meses - 1)

    st.info(f"💡 Cuota mensual recomendada para cubrir tu brecha: **{cuota_recomendada:,.0f} €**")
    st.caption("La cuota recomendada es la aportación teórica necesaria para cubrir tu brecha mensual según tus datos actuales.")

else:
    cuota_recomendada = 150.0

cuota_mensual = st.number_input(
    "Cuota mensual (€)",
    min_value=0.0,
    value=float(cuota_recomendada),
    step=50.0,
    key="cuota_mensual_srg"
)

if cuota_mensual < 80:
    st.warning("⚠️ En los productos Ocaso, la cuota mínima permitida es de **80 €**.")
    cuota_mensual = 80.0
# ============================================================
# 🟦 Función de simulación
# ============================================================

def simular_plan(cuota, aportacion_extra, rentabilidad_anual, inflacion_anual):
    r = rentabilidad_anual / 100 / 12
    inf_mensual = inflacion_anual / 100 / 12
    n = anos_hasta_jub * 12

    capital = aportacion_extra
    historial = []

    for mes in range(1, n + 1):
        capital_inicio = capital
        intereses = capital * r
        capital += intereses + cuota

        factor_inflacion = (1 + inf_mensual) ** mes
        capital_ajustado = capital / factor_inflacion

        historial.append({
            "Mes": mes,
            "Aportación mensual (€)": cuota,
            "Capital inicio (€)": capital_inicio,
            "Intereses ganados (€)": intereses,
            "Capital final (€)": capital,
            "Capital ajustado por inflación (€)": capital_ajustado
        })

    df = pd.DataFrame(historial)
    total_aportado = aportacion_extra + cuota * n
    beneficio_intereses = capital - total_aportado
    capital_ajustado_final = df["Capital ajustado por inflación (€)"].iloc[-1]
    rentabilidad_neta = (capital / total_aportado - 1) * 100 if total_aportado > 0 else 0

    return df, capital, total_aportado, beneficio_intereses, capital_ajustado_final, rentabilidad_neta
# ============================================================
# 🟦 Ajuste automático (referencia)
# ============================================================

def ajustar_cuota(capital_objetivo, aportacion_inicial, rentabilidad_anual, inflacion_anual):
    r_mensual_local = rentabilidad_anual / 100 / 12
    n_meses_local = anos_hasta_jub * 12

    cuota = (
        (capital_objetivo - aportacion_inicial * (1 + r_mensual_local) ** n_meses_local) * r_mensual_local
    ) / ((1 + r_mensual_local) ** n_meses_local - 1)

    paso = 10.0
    for _ in range(500):
        df_tmp, _, _, _, capital_ajustado_final_tmp, _ = simular_plan(
            cuota, aportacion_inicial, rentabilidad_anual, inflacion_anual
        )
        diferencia = capital_objetivo - capital_ajustado_final_tmp
        if abs(diferencia) < 50:
            break
        cuota += paso if diferencia > 0 else -paso

    return cuota

cuota_ajustada = ajustar_cuota(capital_objetivo, aportacion_inicial, rentabilidad, inflacion_media)

if cuota_ajustada < 80:
    cuota_ajustada = 80.0

st.info(f"🔧 Cuota ajustada automáticamente (referencia): **{cuota_ajustada:,.0f} €**")
st.caption("La cuota ajustada se calcula iterando el modelo SRG para alcanzar exactamente el capital objetivo, considerando inflación y rentabilidad.")
# ============================================================
# 🟦 Cuota real (la que manda)
# ============================================================

cuota_real = cuota_mensual

# ============================================================
# 🔄 Recalcular automáticamente al cambiar la cuota
# ============================================================

def actualizar_simulacion():
    df, capital_final, total_aportado, beneficio_intereses, capital_ajustado_final, rentabilidad_neta = simular_plan(
        cuota_real, aportacion_inicial, rentabilidad, inflacion_media
    )
    st.session_state["df"] = df
    st.session_state["capital_final"] = capital_final
    st.session_state["total_aportado"] = total_aportado
    st.session_state["beneficio_intereses"] = beneficio_intereses
    st.session_state["capital_ajustado_final"] = capital_ajustado_final
    st.session_state["rentabilidad_neta"] = rentabilidad_neta

actualizar_simulacion()

df = st.session_state["df"]
capital_final = st.session_state["capital_final"]
total_aportado = st.session_state["total_aportado"]
beneficio_intereses = st.session_state["beneficio_intereses"]
capital_ajustado_final = st.session_state["capital_ajustado_final"]
rentabilidad_neta = st.session_state["rentabilidad_neta"]
# ============================================================
# 🟩 Mensaje de cumplimiento del objetivo
# ============================================================

if capital_final >= capital_objetivo:
    st.success(
        f"🎯 Con una cuota de {cuota_real:,.0f} €, tu capital estimado ({capital_final:,.0f} €) "
        f"supera el capital objetivo ({capital_objetivo:,.0f} €). ¡Cumples tu objetivo de ahorro!"
    )
elif capital_final >= capital_objetivo * 0.95:
    st.info(
        f"✅ Estás muy cerca de cumplir tu objetivo: tu capital estimado ({capital_final:,.0f} €) "
        f"alcanza el 95 % del capital objetivo ({capital_objetivo:,.0f} €)."
    )
else:
    st.warning(
        f"⚠️ Con esta cuota ({cuota_real:,.0f} €), tu capital estimado ({capital_final:,.0f} €) "
        f"no llega al objetivo ({capital_objetivo:,.0f} €). Considera aumentar tu aportación."
    )
# ============================================================
# 🟦 Gráfico SRG
# ============================================================

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Mes"], y=df["Capital final (€)"], mode="lines",
                         name="Ahorro con crecimiento", line=dict(color="green", width=3)))
fig.add_trace(go.Scatter(x=df["Mes"], y=aportacion_inicial + df["Aportación mensual (€)"].cumsum(),
                         mode="lines", name="Ahorro aportado", line=dict(color="blue", width=2)))
fig.add_trace(go.Scatter(x=df["Mes"], y=df["Capital ajustado por inflación (€)"],
                         mode="lines", name="Ahorro ajustado por inflación",
                         line=dict(color="red", dash="dot", width=2)))

fig.update_layout(height=450, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)
# ============================================================
# 🟨 Tabla mensual SRG con estilo visual igual al informe (dentro de expander)
# ============================================================

# Convertimos el DataFrame a HTML con formato y estilo SRG
tabla_html = df.round(2).to_html(index=False)

# Aplicamos el estilo visual SRG (fondo amarillo + encabezado azul + borde dorado + bordes redondeados)
tabla_html = f"""
<style>
    .tabla-srg {{
        width: 100%;
        border-collapse: separate; /* IMPORTANTE para bordes redondeados */
        border-spacing: 0;         /* elimina huecos entre celdas */
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        margin-top: 10px;
        background-color: #fff8dc; /* Fondo amarillo claro */
        border: 2px solid #d4af37; /* Borde dorado */
        border-radius: 12px;       /* Bordes redondeados */
        overflow: hidden;          /* Mantiene redondeo en toda la tabla */
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}

    .tabla-srg th {{
        background-color: #0055A4; /* Azul SRG */
        color: white;
        text-align: center;
        padding: 10px;
        border: 1px solid #ccc;
        font-weight: 600;
    }}

    .tabla-srg td {{
        text-align: right;
        padding: 8px 10px;
        border: 1px solid #ccc;    /* Líneas internas visibles */
        color: #0A1A2F;
        background-color: #fff8dc; /* Fondo uniforme */
    }}

    .tabla-srg tr {{
        background-color: #fff8dc; /* Sin alternancia */
    }}
</style>

<table class="tabla-srg">
{tabla_html.split('<table border="1" class="dataframe">')[1].split('</table>')[0]}
</table>
"""

# Mostramos la tabla dentro de un expander para evitar scroll infinito
with st.expander("Ver detalle mes a mes del plan de ahorro"):
    st.markdown(tabla_html, unsafe_allow_html=True)

# ============================================================
# 🟦 Datos del cliente para informes
# ============================================================

st.markdown("""
<div class='srg-box'>
    <h4>Datos del cliente</h4>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    nombre_cliente = st.text_input("Nombre del cliente", value="Cliente SRG")
    apellido_cliente = st.text_input("Apellidos", value="")
with col2:
    telefono_cliente = st.text_input("Teléfono", value="")
    email_cliente = st.text_input("Email", value="")

fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
# ============================================================
# 🟦 Explicaciones SRG para informes
# ============================================================

explicaciones = {
    "exp_base_reguladora": "La base reguladora es la media de tus bases de cotización...",
    "exp_pension": "Tu pensión futura se calcula aplicando el porcentaje...",
    "exp_nivel_vida": "Tu nivel de vida futuro se obtiene inflando tus gastos...",
    "exp_brecha": "La brecha es la diferencia entre pensión futura y nivel de vida...",
    "exp_capital_objetivo": "El capital objetivo es la brecha mensual multiplicada por años...",
    "exp_plan_ahorro": "El plan SRG calcula automáticamente la cuota necesaria...",
    "exp_grafico": "La gráfica muestra ahorro aportado, crecimiento e inflación...",
    "exp_tabla": "La tabla evolutiva muestra aportación, intereses y capital..."
}
# ============================================================
# 🟦 Contexto para informes
# ============================================================

contexto_pdf = {
    "nombre_cliente": f"{nombre_cliente} {apellido_cliente}",
    "telefono": telefono_cliente,
    "email": email_cliente,
    "fecha": fecha_actual,
    "pension_futura": pension_futura,
    "nivel_vida": nivel_vida_futuro,
    "brecha": brecha,
    "cuota_recomendada": cuota_real,
    "capital_final": capital_final,
    "capital_objetivo": capital_objetivo,
    "capital_ajustado_final": capital_ajustado_final,
    "rentabilidad_neta": rentabilidad_neta,
    "rentabilidad": rentabilidad,
    "inflacion_media": inflacion_media,
    "tabla_evolucion": df.round(2).to_html(index=False),
}
contexto_pdf.update(explicaciones)
# ============================================================
# 🟦 Función Informe Cliente SRG — lenguaje cotidiano
# ============================================================

def informe_cliente(contexto, fig):
    grafica_html = fig.to_html(include_plotlyjs='cdn') if fig else ""

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            body {{
                font-family:'Segoe UI', Arial;
                background-color:#f7f9fc;
                color:#0A1A2F;
                margin:0;
            }}

            .bloque {{
                border:1px solid #0055A4;
                border-radius:8px;
                padding:20px;
                background-color:white;
                margin-top:25px;
            }}

            /* 🟨 Recuadro amarillo elegante */
            .bloque-amarillo {{
                border: 1px solid #d4af37;
                background-color: #fff8dc;
                border-radius: 10px;
                padding: 20px;
                margin-top: 25px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}

            .bloque-amarillo h2 {{
                color: #0A1A2F;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 15px;
            }}

            .bloque-amarillo p {{
                color: #0A1A2F;
                font-size: 14px;
                line-height: 1.5;
                margin-bottom: 10px;
            }}

            .bloque-amarillo b {{
                color: #0A1A2F;
            }}

            table {{
                width:100%;
                border-collapse:collapse;
                font-size:14px;
            }}

            th, td {{
                border:1px solid #ccc;
                padding:6px 8px;
                text-align:right;
            }}

            th {{
                background-color:#0055A4;
                color:white;
            }}

            tr:nth-child(even) {{
                background-color:#f2f4f8;
            }}
        </style>
    </head>

    <body>

        <div style="background: linear-gradient(180deg, #0055A4 0%, #003366 100%);
                    color:white; padding:25px; text-align:center;">
            <h1>Informe Cliente SRG</h1>
            <p>Cliente: <b>{contexto['nombre_cliente']}</b> — Tel: {contexto['telefono']} — Email: {contexto['email']}</p>
            <p>Fecha: {contexto['fecha']}</p>
        </div>

        <div style="padding:30px;">

            <div class="bloque-amarillo">
                <h2>1. Resumen de tu situación</h2>
                <p>Pensión futura estimada: <b>{contexto['pension_futura']:,.0f} €</b></p>
                <p>Nivel de vida futuro: <b>{contexto['nivel_vida']:,.0f} €</b></p>
                <p>Brecha mensual: <b>{contexto['brecha']:,.0f} €</b></p>
            </div>

            <div class="bloque-amarillo">
                <h2>2. Recomendación SRG</h2>
                <p>Cuota mensual aplicada: <b>{contexto['cuota_recomendada']:,.0f} €</b></p>
                <p>Capital estimado al jubilarte: <b>{contexto['capital_final']:,.0f} €</b></p>
                <p>Capital objetivo: <b>{contexto['capital_objetivo']:,.0f} €</b></p>
                <p>Capital ajustado por inflación: <b>{contexto['capital_ajustado_final']:,.0f} €</b></p>
                <p>Rentabilidad neta del plan: <b>{contexto['rentabilidad_neta']:.2f} %</b></p>
            </div>

            <div class="bloque-amarillo">
                <h2>3. Evolución de tu ahorro</h2>
                {contexto['tabla_evolucion']}
            </div>

            <div class="bloque-amarillo">
                <h2>4. Gráfica del plan</h2>
                {grafica_html}
            </div>

            <div class="bloque-amarillo">
                <h2>5. ¿Cómo hemos calculado tu resultado?</h2>

                <p><b>1. Tu pensión futura:</b><br>
                Hemos utilizado tu base reguladora estimada y el porcentaje que te corresponde según tus años cotizados.  
                Resultado: <b>{contexto['pension_futura']:,.0f} €</b> al mes.</p>

                <p><b>2. Tu nivel de vida futuro:</b><br>
                Partimos de tu gasto mensual actual y lo actualizamos con la inflación media anual del periodo.  
                Resultado: <b>{contexto['nivel_vida']:,.0f} €</b> al mes.</p>

                <p><b>3. Tu brecha mensual:</b><br>
                Diferencia entre tu pensión futura y tu nivel de vida futuro.  
                Resultado: <b>{contexto['brecha']:,.0f} €</b> al mes.</p>

                <p><b>4. Capital necesario para cubrir esa brecha:</b><br>
                Brecha × 12 meses × años hasta la jubilación.  
                Resultado: <b>{contexto['capital_objetivo']:,.0f} €</b>.</p>

                <p><b>5. Cuota mensual recomendada:</b><br>
                Calculamos la aportación mensual necesaria para alcanzar ese capital, teniendo en cuenta la rentabilidad y la inflación.  
                Resultado: <b>{contexto['cuota_recomendada']:,.0f} €</b>.</p>

                <p><b>6. Resultado final del plan:</b><br>
                Con la cuota aplicada, tu ahorro estimado al jubilarte será:  
                <b>{contexto['capital_final']:,.0f} €</b>.</p>
            </div>

        </div>
<div style="
    width:100%;
    text-align:center;
    padding:18px;
    margin-top:40px;
    background: linear-gradient(180deg, #0055A4 0%, #003366 100%);
    color:white;
    font-size:13px;
    border-radius:8px;
">
    Simulador SRG — © 2026 Samuel Ruiz González  
    <br>Herramienta educativa y formativa para Agentes
</div>

    </body>
    </html>
    """


# ============================================================
# 🟦 Función Informe Técnico SRG — Agente
# ============================================================

def informe_agente(contexto, fig):
    grafica_html = fig.to_html(include_plotlyjs='cdn') if fig else ""

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            body {{
                font-family:'Segoe UI', Arial;
                background-color:#f7f9fc;
                color:#0A1A2F;
                margin:0;
            }}

            .bloque {{
                border:1px solid #0055A4;
                border-radius:8px;
                padding:20px;
                background-color:white;
                margin-top:25px;
            }}

            .bloque-amarillo {{
                border: 1px solid #d4af37;
                background-color: #fff8dc;
                border-radius: 10px;
                padding: 20px;
                margin-top: 25px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}

            .bloque-amarillo h2 {{
                color: #0A1A2F;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 15px;
            }}

            .bloque-amarillo p {{
                color: #0A1A2F;
                font-size: 14px;
                line-height: 1.5;
                margin-bottom: 10px;
            }}

            .bloque-amarillo b {{
                color: #0A1A2F;
            }}

            table {{
                width:100%;
                border-collapse:collapse;
                font-size:14px;
            }}

            th, td {{
                border:1px solid #ccc;
                padding:6px 8px;
                text-align:right;
            }}

            th {{
                background-color:#0055A4;
                color:white;
            }}

            tr:nth-child(even) {{
                background-color:#f2f4f8;
            }}
        </style>
    </head>

    <body>

        <div style="background: linear-gradient(180deg, #0055A4 0%, #003366 100%);
                    color:white; padding:25px; text-align:center;">
            <h1>Informe Técnico SRG</h1>
            <p>Cliente: <b>{contexto['nombre_cliente']}</b> — Tel: {contexto['telefono']} — Email: {contexto['email']}</p>
            <p>Fecha: {contexto['fecha']}</p>
        </div>

        <div style="padding:30px;">

            <div class="bloque-amarillo">
                <h2>1. Datos técnicos considerados</h2>
                <p>Pensión futura estimada: <b>{contexto['pension_futura']:,.0f} €</b></p>
                <p>Nivel de vida objetivo: <b>{contexto['nivel_vida']:,.0f} €</b></p>
                <p>Brecha mensual: <b>{contexto['brecha']:,.0f} €</b></p>
                <p>Rentabilidad media anual: <b>{contexto['rentabilidad']} %</b></p>
                <p>Inflación media anual: <b>{contexto['inflacion_media']} %</b></p>
            </div>

            <div class="bloque-amarillo">
                <h2>2. Resultados del plan</h2>
                <p>Cuota aplicada: <b>{contexto['cuota_recomendada']:,.0f} €</b></p>
                <p>Capital final estimado: <b>{contexto['capital_final']:,.0f} €</b></p>
                <p>Capital objetivo: <b>{contexto['capital_objetivo']:,.0f} €</b></p>
                <p>Capital ajustado final: <b>{contexto['capital_ajustado_final']:,.0f} €</b></p>
                <p>Rentabilidad neta: <b>{contexto['rentabilidad_neta']:.2f} %</b></p>
            </div>

            <div class="bloque-amarillo">
                <h2>3. Evolución del ahorro</h2>
                {contexto['tabla_evolucion']}
            </div>

            <div class="bloque-amarillo">
                <h2>4. Gráfica del plan</h2>
                {grafica_html}
            </div>

            <div class="bloque-amarillo">
                <h2>5. Trazabilidad técnica del cálculo SRG</h2>

                <p><b>1. Base reguladora (BR):</b><br>
                BR = media ponderada de las bases de cotización actualizadas.  
                Valor utilizado: <b>{contexto['pension_futura']:,.0f} €</b> / porcentaje de cobertura.</p>

                <p><b>2. Pensión futura (PF):</b><br>
                PF = BR × porcentaje según años cotizados.  
                Resultado: <b>{contexto['pension_futura']:,.0f} €</b>.</p>

                <p><b>3. Nivel de vida futuro (NVF):</b><br>
                NVF = gasto_actual × (1 + inflación_media) ^ años.  
                Resultado: <b>{contexto['nivel_vida']:,.0f} €</b>.</p>

                <p><b>4. Brecha mensual (BM):</b><br>
                BM = NVF − PF  
                Resultado: <b>{contexto['brecha']:,.0f} €</b>.</p>

                <p><b>5. Capital objetivo (CO):</b><br>
                CO = BM × 12 × años_hasta_jubilación  
                Resultado: <b>{contexto['capital_objetivo']:,.0f} €</b>.</p>

                <p><b>6. Cuota recomendada (CR):</b><br>
                Fórmula de valor futuro de una renta periódica:  
                CR = (CO − A × (1+r)^n) × r / ((1+r)^n − 1)  
                Donde:<br>
                • A = aportación inicial<br>
                • r = rentabilidad mensual<br>
                • n = meses hasta jubilación<br>
                Resultado: <b>{contexto['cuota_recomendada']:,.0f} €</b>.</p>

                <p><b>7. Capital final del plan (CF):</b><br>
                CF = evolución mensual del ahorro con capitalización compuesta.  
                Resultado: <b>{contexto['capital_final']:,.0f} €</b>.</p>

                <p><b>8. Capital ajustado por inflación (CAI):</b><br>
                CAI = CF / (1 + inflación_media) ^ años  
                Resultado: <b>{contexto['capital_ajustado_final']:,.0f} €</b>.</p>

                <p><b>9. Rentabilidad neta del plan:</b><br>
                RN = (CF / total_aportado − 1) × 100  
                Resultado: <b>{contexto['rentabilidad_neta']:.2f} %</b>.</p>
            </div>

        </div>
    <div style="
    width:100%;
    text-align:center;
    padding:18px;
    margin-top:40px;
    background: linear-gradient(180deg, #0055A4 0%, #003366 100%);
    color:white;
    font-size:13px;
    border-radius:8px;
    ">
    Informe Técnico SRG — © 2026 Samuel Ruiz González  
    <br>Modelo SRG: trazabilidad completa de cálculos y proyecciones
</div>

    </body>
    </html>
    """

# ============================================================
# 🟦 BLOQUE FINAL SRG — VISTA PREVIA Y DESCARGAS
# ============================================================

html_cliente_recom = informe_cliente(contexto_pdf, fig)
html_agente_recom = informe_agente(contexto_pdf, fig)

bytes_cliente_recom = html_cliente_recom.encode("utf-8")
bytes_agente_recom = html_agente_recom.encode("utf-8")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white;
    padding: 20px 25px;
    border-radius: 12px;
    margin-top: 35px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
">
    <h2 style="margin-bottom: 10px;">Vista previa y descargas de informes SRG</h2>
    <p style="margin:0;">Cuota aplicada: <b>""" + f"{cuota_real:,.0f} €" + """</b></p>
</div>
""", unsafe_allow_html=True)

col_cli, col_ag = st.columns(2)

with col_cli:
    st.markdown("### Informe Cliente SRG")
    st.caption("Versión explicada en lenguaje cotidiano para el cliente.")

    with st.expander("Vista previa del informe"):
        st.components.v1.html(html_cliente_recom, height=350, scrolling=True)

    st.download_button(
        label="📄 Descargar Informe Cliente",
        data=bytes_cliente_recom,
        file_name="Informe_Cliente_SRG.html",
        mime="text/html"
    )

with col_ag:
    st.markdown("### Informe Técnico SRG — Agente")
    st.caption("Versión técnica con cálculos y metodología SRG.")

    with st.expander("Vista previa del informe"):
        st.components.v1.html(html_agente_recom, height=350, scrolling=True)

    st.download_button(
        label="📄 Descargar Informe Técnico",
        data=bytes_agente_recom,
        file_name="Informe_Agente_SRG.html",
        mime="text/html"
    )
st.markdown("""
<div style="
    width:100%;
    text-align:center;
    padding:20px;
    margin-top:40px;
    background: linear-gradient(135deg, #003366, #0055A4);
    color:white;
    font-size:14px;
    border-radius:8px;
">
    Simulador de Jubilación SRG — © 2026 Samuel Ruiz González  
    <br>Herramienta profesional de planificación financiera
</div>
""", unsafe_allow_html=True)

