<<<<<<< HEAD

import streamlit as st
import numpy as np
import streamlit.components.v1 as components
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Simulador de Jubilación SRG", page_icon="💼", layout="wide")

# ============================
#   CSS GLOBAL PREMIUM SRG
# ============================
=======
# ============================================
# BLOQUE 1 — IMPORTS, CSS Y FUNCIONES BASE
# ============================================

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime

st.set_page_config(
    page_title="Simulador de Jubilación SRG",
    page_icon="💼",
    layout="wide"
)

# Estado del botón de explicación
if "mostrar_explicacion" not in st.session_state:
    st.session_state.mostrar_explicacion = False

# ============================================
#   CSS GLOBAL PREMIUM SRG (HEADER + TÍTULOS)
# ============================================
>>>>>>> origin/main

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&display=swap');

<<<<<<< HEAD
body, html {
    font-family: 'Montserrat', sans-serif;
}

/* HEADER SRG — degradado sin tocar tipografía */
.srg-header {
    padding: 14px 24px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #003366, #0055A4); /* degradado SRG */
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}

=======
/* ============================================================
   BLOQUE ANTI-FLASH — Fondo oscuro desde el primer frame
   ============================================================ */
html, body, #root, section.main, div[data-testid="stAppViewContainer"] {
    background-color: #05070D !important;
    background-image: none !important;
    transition: none !important;
    color: #EAF2FF !important;
}

/* ============================================================
   TOOLTIP SRG FINAL — Fondo oscuro y texto visible
   ============================================================ */
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

/* ============================================================
   TOOLTIP SRG UNIVERSAL — Hover personalizado
   ============================================================ */
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

/* ============================================================
   HEADER SRG
   ============================================================ */
.srg-header {
    padding: 14px 24px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #003366, #0055A4);
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}
>>>>>>> origin/main
.srg-header-inner {
    max-width: 980px;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    text-align: center;
}
<<<<<<< HEAD

/* TÍTULO PRINCIPAL — tipografía intacta */
=======
>>>>>>> origin/main
.srg-header-title-main {
    font-family: 'Dancing Script', cursive !important;
    font-size: 3.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1.1;
}
<<<<<<< HEAD

/* SUBTÍTULO — tipografía intacta */
=======
>>>>>>> origin/main
.srg-header-title-sub {
    font-family: 'Dancing Script', cursive !important;
    font-size: 1.8rem;
    font-weight: 400;
    color: #d0d8e8;
    margin-top: 6px;
}

<<<<<<< HEAD
/* TITULOS DE SECCIÓN — ahora con degradado suave */
=======
/* ============================================================
   TITULOS Y BLOQUES
   ============================================================ */
>>>>>>> origin/main
.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

<<<<<<< HEAD
/* CAJAS — más limpias y coherentes con informes */
.srg-box {
    background: linear-gradient(180deg, #ffffff, #f2f6fb);
    padding: 14px;
    border-radius: 6px;
    border: 1px solid #c7d4e5;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* FOOTER — degradado SRG */
=======
/* ============================================================
   SELECTBOX Y RADIO SRG OSCUROS
   ============================================================ */
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

/* ============================================================
   FOOTER SRG
   ============================================================ */
>>>>>>> origin/main
.srg-footer {
    margin-top: 30px;
    padding: 16px 12px;
    background: linear-gradient(135deg, #003366, #0055A4);
    color: #ffffff;
    text-align: center;
    font-size: 0.85rem;
    border-radius: 6px 6px 0 0;
}
<<<<<<< HEAD

=======
>>>>>>> origin/main
.srg-footer a {
    color: #ffffff;
    text-decoration: underline;
}
<<<<<<< HEAD

/* MÉTRICAS */
[data-testid="stMetricValue"] {
    font-size: 1.1rem;
}

</style>
""", unsafe_allow_html=True)

# ============================
#   HEADER SIN LOGO
# ============================
=======
</style>
""", unsafe_allow_html=True)
import streamlit as st

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

# ============================================
#   HEADER SRG
# ============================================
>>>>>>> origin/main

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

<<<<<<< HEAD
# ============================
#   FUNCIONES AUXILIARES
# ============================

def calcular_objetivo_y_gastos_futuros(ingresos_hoy, gastos_hoy, pct, inflacion, anos):
    factor = (1 + inflacion/100) ** anos
    return ingresos_hoy * factor, gastos_hoy * (pct/100) * factor

def calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, aportacion):
    meses = anos_hasta_jub * 12
    r_mensual = rentabilidad / 12

    capital = 0
=======
# ============================================
#   FUNCIONES BASE
# ============================================

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
>>>>>>> origin/main
    lista = []

    for mes in range(meses + 1):
        if mes > 0:
<<<<<<< HEAD
            capital = capital * (1 + r_mensual) + aportacion

        capital_aportado = aportacion * mes
        capital_real = capital / ((1 + inflacion/100) ** (mes/12))
=======
            capital = (capital + aportacion) * (1 + r_mensual)

        capital_aportado = aportacion * mes
        capital_real = capital / ((1 + infl_mensual) ** mes) if mes > 0 else 0.0
>>>>>>> origin/main
        inflacion_perdida = capital - capital_real

        lista.append({
            "mes": mes,
            "aportada": capital_aportado,
            "total": capital,
            "inflacion": inflacion_perdida,
            "neta": capital_real
        })

    return lista

<<<<<<< HEAD
# ============================
#   MARCA DE AGUA DIAGONAL
# ============================
=======
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
>>>>>>> origin/main

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

<<<<<<< HEAD
# ============================
#   PORTADA CON DEGRADADO
# ============================

def portada_srg(titulo, fecha):
    return f"""
    <div style="
        height: 420px;
        background: linear-gradient(to bottom, #003366, #0055AA);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    ">
        <div style="font-size: 2.2rem; font-weight: 600;">{titulo}</div>
        <div style="font-size: 1.1rem; opacity: 0.9;">Samuel Ruiz González</div>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">Fecha: {fecha}</div>
    </div>
    """

# ============================
#   TABLA MENSUAL (5 COLUMNAS)
# ============================

def tabla_mensual_y_anual_html(evolucion, anos_hasta_jub):
    filas = ""

    # --- Primeros 12 meses (sin mes 0) ---
    for mes in range(1, 13):
        fila = evolucion[mes]
        filas += f"""
        <tr>
            <td>{mes} (mes)</td>
            <td>{fila['aportada']:,.0f} €</td>
            <td>{fila['total']:,.0f} €</td>
            <td>{fila['inflacion']:,.0f} €</td>
            <td>{fila['neta']:,.0f} €</td>
        </tr>
        """

    # --- Después año a año ---
    for ano in range(2, anos_hasta_jub + 1):
        fila = evolucion[ano * 12]
        filas += f"""
        <tr>
            <td>{ano} (año)</td>
            <td>{fila['aportada']:,.0f} €</td>
            <td>{fila['total']:,.0f} €</td>
            <td>{fila['inflacion']:,.0f} €</td>
            <td>{fila['neta']:,.0f} €</td>
        </tr>
        """

    return filas


# ============================================
#   FILA 1 — DATOS PRINCIPALES
=======
# ============================================
# BLOQUE 2 — INTERFAZ PRINCIPAL (PARTE 1)
>>>>>>> origin/main
# ============================================

col1, col2, col3, col4 = st.columns(4)

<<<<<<< HEAD
with col1:
    st.markdown('<div class="srg-title">Datos personales</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    edad_actual = st.number_input(
        "Edad actual",
        18, 70, 40,
        help="Tu edad hoy. Se usa para calcular los años que faltan hasta la jubilación."
=======
# DATOS PERSONALES
if "edad_actual_input" not in st.session_state:
    st.session_state.edad_actual_input = 47
if "edad_prevista_jub_input" not in st.session_state:
    st.session_state.edad_prevista_jub_input = 67
if "esperanza_vida_input" not in st.session_state:
    st.session_state.esperanza_vida_input = 85

with col1:
    st.markdown('<div class="srg-title">Datos personales</div>', unsafe_allow_html=True)
    st.caption("Información básica necesaria para calcular tu horizonte de jubilación.")

    edad_actual = st.number_input(
        "Edad actual",
        min_value=18,
        max_value=70,
        help="Tu edad hoy. Se usa para calcular cuántos años faltan hasta la jubilación.",
        key="edad_actual_input"
>>>>>>> origin/main
    )

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
<<<<<<< HEAD
        60, 75, 67,
        help="La edad a la que deseas jubilarte. Afecta a la pensión y al tiempo de ahorro."
=======
        min_value=edad_actual + 1,
        max_value=75,
        help="Edad a la que deseas jubilarte. No puede ser menor o igual que tu edad actual.",
        key="edad_prevista_jub_input"
>>>>>>> origin/main
    )

    esperanza_vida = st.number_input(
        "Esperanza de vida",
<<<<<<< HEAD
        75, 100, 85,
        help="Años que se estima que vivirás. Se usa para calcular cuántos años necesitarás ingresos en jubilación."
    )
# --- Corrección suave de edades para evitar errores ---
if edad_actual >= edad_prevista_jub:
    st.warning("La edad prevista de jubilación debe ser mayor que la edad actual. Se ajusta automáticamente.")
    edad_prevista_jub = edad_actual + 1

if esperanza_vida <= edad_prevista_jub:
    st.warning("La esperanza de vida debe ser mayor que la edad de jubilación. Se ajusta automáticamente.")
    esperanza_vida = edad_prevista_jub + 1

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    anos_cotizados_hoy = st.number_input(
        "Años cotizados hoy",
        0, edad_actual - 16, 10,
        help="Años que ya has cotizado a la Seguridad Social."
=======
        min_value=75,
        max_value=100,
        help="Estimación de años que vivirás según estadísticas.",
        key="esperanza_vida_input"
    )

    st.markdown('</div>', unsafe_allow_html=True)

if edad_prevista_jub <= edad_actual:
    edad_prevista_jub = edad_actual + 1
if esperanza_vida <= edad_prevista_jub:
    esperanza_vida = edad_prevista_jub + 1

# COTIZACIÓN
if "anos_cotizados_hoy_input" not in st.session_state:
    st.session_state.anos_cotizados_hoy_input = 15
if "anos_futuros_input" not in st.session_state:
    st.session_state.anos_futuros_input = 20

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
        help="Años cotizados a la Seguridad Social.",
        key="anos_cotizados_hoy_input"
    )

    max_anos_futuros = max(0, edad_prevista_jub - edad_actual)
    st.session_state.anos_futuros_input = min(
        st.session_state.anos_futuros_input, max_anos_futuros
>>>>>>> origin/main
    )

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
<<<<<<< HEAD
        0, edad_prevista_jub - edad_actual, 0,
        help="Años que te quedan por cotizar hasta la jubilación."
=======
        min_value=0,
        max_value=max_anos_futuros,
        help="Años adicionales que seguirás cotizando.",
        key="anos_futuros_input"
>>>>>>> origin/main
    )

    st.markdown('</div>', unsafe_allow_html=True)

<<<<<<< HEAD
with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    tipo_jubilacion = st.selectbox(
        "Tipo prevista",
        ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"],
        help="La modalidad determina penalizaciones o bonificaciones en la pensión."
    )

    meses_anticipo = st.number_input(
        "Meses anticipo (+) / demora (-)",
        -120, 60, 0,
        help="Meses que adelantas o retrasas tu jubilación. Afecta al coeficiente de ajuste."
    )
=======
anos_totales = anos_cotizados_hoy + anos_futuros
anos_hasta_jub = max(1, edad_prevista_jub - edad_actual)
anos_jubilacion = max(1, esperanza_vida - edad_prevista_jub)

# ============================================
# TIPO DE JUBILACIÓN — LÓGICA 2026 COMPLETA
# ============================================

EDAD_LEGAL_2026 = 67

if "tipo_jubilacion_input" not in st.session_state:
    st.session_state.tipo_jubilacion_input = "Ordinaria"

with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    st.caption("Modalidad, requisitos, anticipos, penalizaciones y bonificaciones según normativa 2026.")

    opciones_jub = ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"]
    idx_tipo = opciones_jub.index(st.session_state.tipo_jubilacion_input)

    # ⭐ Label alineado como los demás inputs
    st.markdown("Tipo prevista")

    # ⭐ Sustituimos selectbox por radio (estilo select SRG)
    tipo_jubilacion = st.radio(
        "",
        opciones_jub,
        index=idx_tipo,
        key="tipo_jubilacion_input",
        label_visibility="collapsed"
    )

    modo_valido = True
    motivo_error = ""
    coef_ajuste = 1.0
    meses_anticipo = 0

    # ⭐ Explicaciones SRG premium (títulos más pequeños)
    if tipo_jubilacion == "Ordinaria":
        st.markdown("""
        #### 🟦 Jubilación ordinaria
        **Edad legal:** 67 años (o 65 si se acreditan 38 años y 6 meses cotizados).  
        **Requisitos de acceso:** mínimo **15 años cotizados**.  
        **Porcentaje de la pensión:** depende de los años cotizados totales.  
        - 15 años → 50%  
        - De 16 a 36 años → +0,21% por mes  
        - De 36 a 37 años → +0,19% por mes  
        **100%** solo si se alcanzan **37 años cotizados**.  
        **No hay penalización**, simplemente se aplica el porcentaje correspondiente.
        """)

        if anos_totales < 15:
            modo_valido = False
            motivo_error = "No cumples los 15 años cotizados mínimos para la jubilación ordinaria."
        elif edad_prevista_jub < EDAD_LEGAL_2026:
            st.warning(f"La edad prevista ({edad_prevista_jub}) es inferior a la edad legal ({EDAD_LEGAL_2026}). Se aplicará la edad legal.")
            edad_prevista_jub = EDAD_LEGAL_2026

    elif tipo_jubilacion == "Anticipada voluntaria":
        st.markdown("""
        #### 🟧 Anticipada voluntaria
        **Adelanto máximo:** 24 meses.  
        **Requisitos:** 35 años cotizados y no despido forzoso.  
        **Penalización por trimestre:**
        - < 38a6m → 5,25%  
        - 38a6m–41a6m → 4,75%  
        - 41a6m–44a6m → 4,25%  
        - > 44a6m → 3,25%
        """)

        if anos_totales < 35:
            modo_valido = False
            motivo_error = "No cumples los 35 años cotizados para la anticipada voluntaria."

        meses_anticipo = st.number_input(
            "Meses de anticipo",
            1, 24, 1
        )

        edad_prevista_jub = EDAD_LEGAL_2026 - meses_anticipo / 12

        def coef_voluntaria(anos, meses):
            trimestres = meses // 3
            if anos < 38.5:
                red = 0.0525
            elif anos < 41.5:
                red = 0.0475
            elif anos < 44.5:
                red = 0.0425
            else:
                red = 0.0325
            return 1 - red * trimestres

        coef_ajuste = coef_voluntaria(anos_totales, meses_anticipo)

    elif tipo_jubilacion == "Anticipada involuntaria":
        st.markdown("""
        #### 🟥 Anticipada involuntaria
        **Adelanto máximo:** 48 meses.  
        **Requisitos:** 33 años cotizados y despido objetivo/ERE.  
        **Penalización por trimestre:**
        - < 38a6m → 7,5%  
        - 38a6m–41a6m → 7%  
        - 41a6m–44a6m → 6,5%  
        - > 44a6m → 5,5%
        """)

        if anos_totales < 33:
            modo_valido = False
            motivo_error = "No cumples los 33 años cotizados para la anticipada involuntaria."

        meses_anticipo = st.number_input(
            "Meses de anticipo",
            1, 48, 1
        )

        edad_prevista_jub = EDAD_LEGAL_2026 - meses_anticipo / 12

        def coef_involuntaria(anos, meses):
            trimestres = meses // 3
            if anos < 38.5:
                red = 0.075
            elif anos < 41.5:
                red = 0.070
            elif anos < 44.5:
                red = 0.065
            else:
                red = 0.055
            return 1 - red * trimestres

        coef_ajuste = coef_involuntaria(anos_totales, meses_anticipo)

    elif tipo_jubilacion == "Demorada":
        st.markdown("""
        #### 🟩 Jubilación demorada
        **Edad:** mayor de 67 años.  
        **Bonificación:** +4% por cada año completo de demora.
        """)

        if edad_prevista_jub <= EDAD_LEGAL_2026:
            modo_valido = False
            motivo_error = f"Para demorada, la edad prevista debe ser mayor que {EDAD_LEGAL_2026}."
        else:
            anos_demora = edad_prevista_jub - EDAD_LEGAL_2026
            coef_ajuste = 1 + anos_demora * 0.04
            meses_demora = int(anos_demora * 12)
            st.metric("Meses de demora", f"{meses_demora} meses")

    if not modo_valido:
        st.markdown(
            f'<div class="msg-error-srg">{motivo_error}</div>',
            unsafe_allow_html=True
        )
>>>>>>> origin/main

    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
<<<<<<< HEAD
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    ingresos = st.number_input(
        "Ingresos mensuales (€)",
        0, 20000, 2500,
        help="Tus ingresos actuales. Se usan para calcular tu capacidad de ahorro."
    )

    gastos = st.number_input(
        "Gastos mensuales (€)",
        0, 20000, 1800,
        help="Tus gastos actuales. Se usan para calcular tu capacidad de ahorro."
    )

=======
    st.caption("Tus ingresos y gastos actuales nos permiten estimar tu objetivo económico futuro.")

    ingresos = st.number_input(
        "Ingresos mensuales (€)",
        min_value=0,
        max_value=20000,
        help="Tus ingresos netos actuales.",
        key="ingresos_input"
    )

    if "gastos_input" not in st.session_state:
        st.session_state.gastos_input = min(1800, ingresos)

    st.session_state.gastos_input = min(st.session_state.gastos_input, ingresos)

    gastos = st.number_input(
        "Gastos mensuales (€)",
        min_value=0,
        max_value=20000,
        help="Tus gastos mensuales actuales.",
        key="gastos_input"
    )

    if gastos > ingresos:
        st.warning("Has indicado más gastos que ingresos. Ajustamos los gastos al máximo igual a tus ingresos.")
        gastos = ingresos

>>>>>>> origin/main
    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
<<<<<<< HEAD
#   CÁLCULOS LEGALES
# ============================================

REQUISITOS = {
    "Ordinaria": 15,
    "Anticipada voluntaria": 35,
    "Anticipada involuntaria": 33,
    "Demorada": 15
}

LIMITES = {
    "Anticipada voluntaria": 24,
    "Anticipada involuntaria": 48
}

anos_totales = anos_cotizados_hoy + anos_futuros
anos_hasta_jub = edad_prevista_jub - edad_actual
anos_jubilacion = esperanza_vida - edad_prevista_jub

modo_valido = True

if anos_totales < REQUISITOS[tipo_jubilacion]:
    modo_valido = False

if tipo_jubilacion in ["Anticipada voluntaria", "Anticipada involuntaria"]:
    if meses_anticipo <= 0 or meses_anticipo > LIMITES[tipo_jubilacion]:
        modo_valido = False

if tipo_jubilacion == "Demorada" and meses_anticipo >= 0:
    modo_valido = False

coef_ajuste = 1.0
if modo_valido:
    if "Anticipada" in tipo_jubilacion:
        coef_ajuste -= 0.005 * meses_anticipo
    elif tipo_jubilacion == "Demorada":
        coef_ajuste -= 0.004 * meses_anticipo

coef_ajuste = max(0, coef_ajuste)

# ============================================
#   EXPLICACIÓN DETALLADA
# ============================================

st.markdown('<div class="srg-title">Explicación detallada</div>', unsafe_allow_html=True)

if modo_valido:
    st.success("La modalidad seleccionada es válida.")
else:
    st.error("La modalidad seleccionada NO es válida según los años cotizados o los meses de anticipo/demora.")

with st.expander("Ver explicación detallada"):
    st.write(f"**Modalidad:** {tipo_jubilacion}")
    st.write(f"**Años cotizados hoy:** {anos_cotizados_hoy}")
    st.write(f"**Años que te quedan por cotizar:** {anos_futuros}")
    st.write(f"**Total años cotizados previstos:** {anos_totales}")
    st.write(f"**Años hasta la jubilación:** {anos_hasta_jub}")
    st.write(f"**Años estimados en jubilación:** {anos_jubilacion}")
    st.write(f"**Meses anticipo/demora:** {meses_anticipo}")
    st.write(f"**Coeficiente aplicado:** {coef_ajuste:.3f}")

# ============================================
#   FILA 2 — PENSIÓN, OBJETIVO Y BRECHA
# ============================================

colA, colB, colC, colD = st.columns(4)

with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    base = st.number_input(
        "Base reguladora (€)",
        0, 50000, 1500,
        help="Promedio de tus bases de cotización. Determina tu pensión."
    )

    inflacion = st.number_input(
        "Inflación anual (%)",
        0.0, 10.0, 2.0, 0.1,
        help="La inflación reduce el poder adquisitivo del dinero con el tiempo."
=======
# BLOQUE 3 — PENSIÓN, OBJETIVO Y BRECHA
# ============================================

PENSION_MAX_2026 = 3359.60
EXTRA_REVAL = 0.00115
BASE_MAX_ESPANA_2026 = 4720

colA, colB, colC, colD = st.columns(4)

# PENSIÓN E INFLACIÓN
with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    st.caption("Estos valores determinan tu pensión futura ajustada a la inflación.")

    modo_br = st.radio(
        "Modo de cálculo de Base Reguladora",
        ["Introducir base reguladora manualmente", "Calcular base reguladora SRG"],
        help="La Base Reguladora se calcula con las bases de cotización de los últimos 29 años.",
        key="modo_br_input"
    )

    if modo_br == "Introducir base reguladora manualmente":
        base = st.number_input(
            "Base reguladora (€)",
            min_value=0,
            max_value=BASE_MAX_ESPANA_2026,
            value=1500,
            help="Introduce directamente tu base reguladora estimada.",
            key="base_reguladora_input"
        )
    else:
        st.markdown("#### Calcular base reguladora SRG")
        st.caption("Los cálculos respetan los límites legales de cotización y pensión.")

        salario_actual = st.number_input(
            "Salario mensual actual (€)",
            min_value=0,
            max_value=20000,
            value=2000,
            help="Salario bruto mensual aproximado.",
            key="salario_actual_input"
        )

        crecimiento_salarial = st.number_input(
            "Crecimiento salarial anual (%)",
            min_value=0.0,
            max_value=10.0,
            value=1.5,
            step=0.1,
            help="Incremento medio anual de tu salario.",
            key="crecimiento_salarial_input"
        )

        ipc_actualizacion = st.number_input(
            "Actualización IPC anual (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            help="Factor de actualización de bases antiguas.",
            key="ipc_actualizacion_input"
        )

        anos_con_salario = st.number_input(
            "Años cotizados con salario conocido",
            min_value=1,
            max_value=29,
            value=10,
            help="Años recientes con salario aproximado.",
            key="anos_con_salario_input"
        )

        meses_totales = 29 * 12
        bases = []
        for i in range(meses_totales):
            anos_pasados = (meses_totales - 1 - i) / 12
            salario_estimado = salario_actual / ((1 + crecimiento_salarial/100) ** anos_pasados)
            bases.append(salario_estimado)

        bases_actualizadas = []
        for i, base_i in enumerate(bases):
            anos_pasados = (meses_totales - 1 - i) / 12
            factor_ipc = (1 + ipc_actualizacion/100) ** anos_pasados
            bases_actualizadas.append(base_i * factor_ipc)

        bases_ordenadas = sorted(bases_actualizadas)
        mejores_322 = bases_ordenadas[24:]
        base = sum(mejores_322) / 322 if len(mejores_322) == 322 else (sum(mejores_322) / max(1, len(mejores_322)))

        if base > BASE_MAX_ESPANA_2026:
            base = BASE_MAX_ESPANA_2026
            st.warning(f"La base reguladora supera el límite legal ({BASE_MAX_ESPANA_2026:,.0f} €). Ajustada automáticamente.")

        st.markdown(
    f'<div class="msg-green-srg">Base reguladora calculada: {base:,.0f} €</div>',
    unsafe_allow_html=True
)


    inflacion = st.number_input(
        "Inflación anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="La inflación reduce el poder adquisitivo.",
        key="inflacion_input"
>>>>>>> origin/main
    )

    reval = st.number_input(
        "Revalorización anual pensión (%)",
<<<<<<< HEAD
        0.0, 5.0, 1.5, 0.1,
        help="Incremento anual estimado de la pensión pública."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# Cálculo pensión
if modo_valido:
    pct = min(1, anos_totales / 37)
else:
    pct = 0

pension_hoy = base * pct * coef_ajuste
pension_futura = pension_hoy * ((1 + reval/100) ** anos_hasta_jub)

with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.write(f"**Porcentaje sobre base:** {pct*100:,.1f} %")
    st.write(f"**Pensión ajustada hoy:** {pension_hoy:,.0f} €")
    st.write(f"**Pensión futura estimada:** {pension_futura:,.0f} €/mes")

    st.markdown('</div>', unsafe_allow_html=True)

with colC:
    st.markdown('<div class="srg-title">Objetivo económico</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    objetivo_hoy = st.number_input(
        "Ingresos deseados hoy (€)",
        0, 20000, 2000,
        help="Ingresos mensuales que te gustaría mantener en jubilación."
    )

    pct_mantener = st.number_input(
        "Gastos que mantendrás en jubilación (%)",
        50, 120, 90,
        help="Porcentaje de tus gastos actuales que mantendrás en jubilación."
    )

    st.markdown('</div>', unsafe_allow_html=True)

objetivo_futuro, gastos_futuros = calcular_objetivo_y_gastos_futuros(
    objetivo_hoy, gastos, pct_mantener, inflacion, anos_hasta_jub
)

with colC:
    st.metric("Objetivo mensual futuro", f"{objetivo_futuro:,.0f} €")
    st.metric("Gastos futuros estimados", f"{gastos_futuros:,.0f} €")

with colD:
    st.markdown('<div class="srg-title">Brecha</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
=======
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Incremento anual previsto de la pensión.",
        key="reval_input"
    )

    st.markdown(
    '<div class="msg-ok-srg">En España existe una base máxima de cotización. Aunque ganes más, solo se computa hasta ese límite.</div>',
    unsafe_allow_html=True
)


    with st.expander("📘 Explicación: IPC, inflación y revalorización"):
        st.markdown("""
        - **IPC anual**: se usa para actualizar las bases de cotización antiguas y calcular tu Base Reguladora SRG.  
        - **Inflación anual**: proyecta el coste de vida futuro y afecta a tu nivel de vida y brecha.  
        - **Revalorización de pensión**: estima cuánto subirá tu pensión cada año una vez jubilado.  
        """)

    st.markdown('</div>', unsafe_allow_html=True)

def pension_maxima_proyectada(anos, inflacion_pct):
    return PENSION_MAX_2026 * ((1 + inflacion_pct/100 + EXTRA_REVAL) ** anos)

if "modo_valido" not in locals():
    modo_valido = True
if "coef_ajuste" not in locals():
    coef_ajuste = 1.0

pct = min(1.0, anos_totales / 37) if modo_valido else 0.0

base_reguladora_ajustada = min(base, BASE_MAX_ESPANA_2026)
pension_hoy = base_reguladora_ajustada * pct * coef_ajuste
pension_futura_sin_tope = pension_hoy * ((1 + reval/100) ** anos_hasta_jub)
pension_max_futura = pension_maxima_proyectada(anos_hasta_jub, inflacion)
pension_futura = min(pension_futura_sin_tope, pension_max_futura)

# RESUMEN PENSIÓN
with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    st.caption("Tu pensión estimada según tus años cotizados y tu base reguladora.")

    if not modo_valido:
        st.markdown(
            '<div class="msg-error-srg">La modalidad de jubilación seleccionada no es válida con tus años cotizados o edad prevista.</div>',
            unsafe_allow_html=True
        )
        st.caption("Revisa el bloque de 'Tipo de jubilación' para ver los requisitos legales.")
    else:
        st.metric("Porcentaje sobre base", f"{pct*100:,.1f} %")
        st.metric("Pensión ajustada hoy", f"{pension_hoy:,.0f} €")
        st.metric("Pensión futura estimada", f"{pension_futura:,.0f} €/mes")

        if pension_futura == pension_max_futura:
            st.warning(
                f"La pensión futura calculada supera el límite legal permitido. "
                f"Se ha aplicado el tope máximo proyectado de {pension_max_futura:,.0f} €/mes."
            )

    st.markdown('</div>', unsafe_allow_html=True)

# NIVEL DE VIDA
with colC:
    st.markdown('<div class="srg-title">Tu nivel de vida en la jubilación</div>', unsafe_allow_html=True)
    st.caption("Estimamos cuánto necesitarás cada mes al jubilarte según tu nivel de vida actual.")

    if modo_br == "Calcular base reguladora SRG":
        ingresos_hoy = salario_actual
        st.markdown(
            f'<div class="msg-ok-srg">Usando tu salario mensual real ({ingresos_hoy:,.0f} €) para estimar tu nivel de vida.</div>',
            unsafe_allow_html=True
        )
    else:
        ingresos_hoy = st.number_input(
            "¿Cuánto ganas al mes ahora? (€)",
            min_value=0,
            max_value=20000,
            value=2000,
            help="Este dato nos permite estimar tu nivel de vida actual.",
            key="ingresos_hoy_input"
        )

    porcentaje_gastos = st.number_input(
        "¿Qué parte de tus gastos crees que seguirás teniendo al jubilarte? (%)",
        min_value=50,
        max_value=110,
        value=90,
        help="Por ejemplo, si crees que gastarás el 90% de lo que gastas hoy, introduce 90.",
        key="porcentaje_gastos_input"
    )

    objetivo_futuro = ingresos_hoy * (porcentaje_gastos / 100) * ((1 + inflacion/100) ** anos_hasta_jub)
    gastos_futuros = gastos * ((1 + inflacion/100) ** anos_hasta_jub)

    st.metric("Lo que necesitarás cada mes al jubilarte", f"{objetivo_futuro:,.0f} €")
    st.caption("Cantidad mensual necesaria para mantener tu estilo de vida cuando te jubiles.")

    st.markdown('</div>', unsafe_allow_html=True)

# BRECHA
with colD:
    st.markdown('<div class="srg-title">Brecha</div>', unsafe_allow_html=True)
    st.caption("Diferencia entre tu pensión futura y el nivel de vida que deseas mantener.")
>>>>>>> origin/main

    modo_brecha = st.radio(
        "¿Qué quieres cubrir?",
        ["Objetivo económico", "Gastos reales"],
        horizontal=True,
<<<<<<< HEAD
        help="Selecciona si quieres cubrir tu objetivo de ingresos o tus gastos reales futuros."
    )

    brecha = objetivo_futuro - pension_futura if modo_brecha == "Objetivo económico" else gastos_futuros - pension_futura

    st.metric("Brecha mensual a cubrir", f"{brecha:,.0f} €")

    with st.expander("¿Qué es la brecha?"):
        st.markdown("""
La **brecha** es la diferencia entre:

- lo que necesitarás cada mes en jubilación (tu *objetivo económico* o tus *gastos reales*),  
y  
- la pensión pública futura estimada.

En términos prácticos, la brecha representa **cuánto dinero faltaría cada mes** para mantener tu nivel de vida.

El plan de ahorro SRG se diseña precisamente para **cubrir esa brecha** de forma realista, sostenible y adaptada a tu situación personal.
""")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
#   PLAN DE AHORRO
# ============================================

colP1, colP2 = st.columns([1, 2])

with colP1:
    st.markdown('<div class="srg-title">Plan de ahorro recomendado</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    rentabilidad = st.number_input(
        "Rentabilidad anual asumida (%)",
        0.0, 15.0, 4.0, 0.1,
        help="Rentabilidad esperada de tus inversiones. Afecta al capital acumulado."
    ) / 100

    if brecha <= 0:
        st.success("Con la pensión futura estimada no necesitarías ahorro adicional para cubrir la brecha seleccionada.")
        aportacion = 0
        capital_necesario = 0
        evolucion = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, 0)
    else:
        if rentabilidad == 0:
            capital_necesario = brecha * 12 * anos_jubilacion
        else:
            capital_necesario = brecha * 12 * (1 - (1 + rentabilidad)**(-anos_jubilacion)) / rentabilidad

        meses_hasta_jub = anos_hasta_jub * 12
        r_mensual = rentabilidad / 12

        if meses_hasta_jub > 0:
            if rentabilidad == 0:
                aportacion = capital_necesario / meses_hasta_jub
            else:
                aportacion = capital_necesario * r_mensual / ((1 + r_mensual)**meses_hasta_jub - 1)
        else:
            aportacion = 0

        st.metric("Capital necesario al jubilarte", f"{capital_necesario:,.0f} €")
        st.metric("Aportación mensual recomendada", f"{aportacion:,.0f} €/mes")

        evolucion = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, aportacion)

    # Resumen capital
    capital_total = evolucion[-1]["total"]
    capital_aportado = evolucion[-1]["aportada"]
    capital_real_final = evolucion[-1]["neta"]
    capital_rendimientos = capital_total - capital_aportado

    st.markdown("### Desglose del capital acumulado al jubilarte")
    col_cap1, col_cap2 = st.columns(2)

    with col_cap1:
        st.metric("Capital aportado", f"{capital_aportado:,.0f} €")
        st.metric("Rendimientos obtenidos", f"{capital_rendimientos:,.0f} €")

    with col_cap2:
        st.metric("Capital total acumulado", f"{capital_total:,.0f} €")
        st.metric("Capital neto (ajustado inflación)", f"{capital_real_final:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
#   GRÁFICA EVOLUCIÓN CAPITAL (INTERACTIVA)
# ============================================

with colP2:
    st.markdown('<div class="srg-title">Evolución del capital</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    # Eliminamos el mes 0 para que la gráfica empiece en mes 1
    evolucion_sin_mes0 = evolucion[1:]

    anos_evol = [fila["mes"]/12 for fila in evolucion_sin_mes0]
    total = [fila["total"] for fila in evolucion_sin_mes0]
    aportada = [fila["aportada"] for fila in evolucion_sin_mes0]
    neta = [fila["neta"] for fila in evolucion_sin_mes0]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=anos_evol, y=total,
        mode='lines',
        name='Cantidad aportada + rendimientos',
        line=dict(color='#003366', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=anos_evol, y=aportada,
        mode='lines',
        name='Cantidad aportada',
        line=dict(color='#66a3ff', width=2, dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=anos_evol, y=neta,
        mode='lines',
        name='Cantidad neta (ajustada inflación)',
        line=dict(color='#009999', width=2)
    ))

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Años hasta jubilación",
        yaxis_title="Capital (€)"
=======
        help="Elige si quieres cubrir tu objetivo deseado (ingresos) o tus gastos reales proyectados.",
        key="modo_brecha_input"
    )

    if modo_brecha == "Objetivo económico":
        brecha = max(0.0, objetivo_futuro - pension_futura)
        tipo_brecha_descripcion = "tu objetivo económico (ingresos deseados en jubilación)"
    else:
        brecha = max(0.0, gastos_futuros - pension_futura)
        tipo_brecha_descripcion = "tus gastos reales proyectados en jubilación"

    st.metric("Brecha mensual a cubrir", f"{brecha:,.0f} €")

    if brecha == 0:
        st.caption("Tu pensión futura supera el nivel de vida estimado, por lo que no existe brecha que cubrir.")

    with st.expander("💡 Explicación de brecha y cómo afecta al plan de ahorro"):
        st.markdown(f"""
        **Brecha económica**  
        Es la diferencia mensual entre tu pensión futura y el dinero que necesitarás para mantener tu nivel de vida.

        - Si eliges **Objetivo económico**, la brecha se calcula respecto a {tipo_brecha_descripcion}.  
        - Si eliges **Gastos reales**, la brecha se calcula respecto a tus gastos actuales proyectados con inflación.

        Esta brecha es la base de todo el plan de ahorro:  
        - Se usa para calcular el **capital necesario** durante la jubilación.  
        - De ella se deriva la **cuota recomendada** y todas las **simulaciones de cuotas**.  
        """)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# BLOQUE 4 — PLAN DE AHORRO + GRÁFICA + SIMULACIONES
# ============================================

st.markdown('<div class="srg-title">Plan de ahorro recomendado</div>', unsafe_allow_html=True)
st.caption("El plan se construye para cubrir la brecha que has elegido (objetivo económico o gastos reales) usando la rentabilidad asumida.")

col_left, col_right = st.columns([0.42, 0.58])

with col_left:
    st.markdown("Rentabilidad anual esperada (%)")

    st.markdown(
        """
        <style>
        .srg-rentabilidad input {
            width: 110px !important;
            text-align: center;
            border-radius: 6px !important;
            border: 1px solid #c7d4e5 !important;
            background-color: #f8f9fb !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    rent_col, _ = st.columns([0.5, 0.5])
    with rent_col:
        rentabilidad_pct = st.number_input(
            "",
            0.0, 15.0, 4.0, 0.1,
            key="rentabilidad_pct_input",
            label_visibility="collapsed"
        )

    anos_jubilacion = max(1, esperanza_vida - edad_prevista_jub)
    capital_necesario = max(0.0, brecha * 12 * anos_jubilacion)

    if anos_hasta_jub > 0:
        r_m = (1 + rentabilidad_pct/100) ** (1/12) - 1
        n_meses = int(anos_hasta_jub * 12)
        if r_m > 0:
            aportacion_recom = capital_necesario * r_m / ((1 + r_m) ** n_meses - 1)
        else:
            aportacion_recom = capital_necesario / max(1, n_meses)
    else:
        aportacion_recom = capital_necesario / 12 if capital_necesario > 0 else 0.0

    evolucion_recom = calcular_evolucion_mensual(
        anos_hasta_jub, rentabilidad_pct, inflacion, aportacion_recom
    )

    capital_total_recom = evolucion_recom[-1].get("total", 0.0)
    capital_real_final_recom = evolucion_recom[-1].get("neta", 0.0)

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Capital necesario", f"{capital_necesario:,.0f} €")
        st.metric("Capital total recomendado", f"{capital_total_recom:,.0f} €")
    with m2:
        st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €")
        st.metric("Capital neto recomendado", f"{capital_real_final_recom:,.0f} €")

    with st.expander("📘 Explicación de la cuota recomendada y la rentabilidad"):
        st.markdown(f"""
        La **cuota recomendada** se calcula para cubrir la brecha mensual de **{brecha:,.0f} €** durante {anos_jubilacion} años de jubilación.

        - Se asume una **rentabilidad anual** del **{rentabilidad_pct:,.1f}%**, aplicada de forma mensual.  
        - Cuanto mayor sea la rentabilidad, menor cuota necesitas para alcanzar el mismo capital.  
        - Si la rentabilidad baja, la cuota recomendada aumenta para compensar.

        Esta cuota es el punto de referencia para todas las simulaciones posteriores (tu propia cuota y la comparativa de cuotas).
        """)

with col_right:
    evo_sin0 = evolucion_recom[1:] if len(evolucion_recom) > 1 else []
    anos_evo = [fila["mes"] / 12 for fila in evo_sin0]
    total_evo = [fila["total"] for fila in evo_sin0]
    aportada_evo = [fila["aportada"] for fila in evo_sin0]
    neta_evo = [fila["neta"] for fila in evo_sin0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=anos_evo, y=total_evo,
        mode='lines',
        name='Total',
        line=dict(color='#00BFFF', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=anos_evo, y=aportada_evo,
        mode='lines',
        name='Aportado',
        line=dict(color='#00FFAA', width=2, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=anos_evo, y=neta_evo,
        mode='lines',
        name='Neto',
        line=dict(color='#FF00AA', width=2)
    ))

    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor='#0A0F1F',
        paper_bgcolor='#0A0F1F',
        xaxis_title="Años",
        yaxis_title="Capital (€)",
        font=dict(color="#EAF2FF"),
        title=dict(
            text="<b>Evolución del capital recomendado</b>",
            x=0.5,
            y=0.95,
            font=dict(size=15, color="#EAF2FF", family="Montserrat")
        )
>>>>>>> origin/main
    )

    st.plotly_chart(fig, use_container_width=True)

<<<<<<< HEAD
    st.markdown('</div>', unsafe_allow_html=True)
# ============================================
#   FASE 1 — Diagnóstico + Escenarios SRG (2 columnas)
# ============================================

with st.expander(" Diagnóstico y Escenarios SRG"):

    col_left, col_right = st.columns(2)

    # -------------------------
    #   COLUMNA IZQUIERDA — DIAGNÓSTICO
    # -------------------------
    with col_left:
        st.markdown("### Diagnóstico SRG — Tu situación explicada con claridad")

        st.markdown(f"""
**1. ¿Qué significa tu brecha mensual?**  
La brecha es la diferencia entre lo que necesitarás cada mes en jubilación y lo que aportará tu pensión pública.  
Tu brecha actual es de **{brecha:,.0f} €/mes**.

**2. ¿Tienes capacidad real para cubrir esa brecha?**  
Tu capacidad de ahorro actual es de **{capacidad:,.0f} €/mes**.

**3. ¿Cuánto dependes de la pensión pública?**  
Tu pensión cubriría aproximadamente el **{(pension_futura/objetivo_futuro)*100:,.0f}%** de tus ingresos deseados.

**4. Conclusión SRG**  
Tu pensión futura estimada es de **{pension_futura:,.0f} €/mes**,  
tu objetivo mensual es **{objetivo_futuro:,.0f} €**,  
y existe una brecha de **{brecha:,.0f} €/mes** que debe cubrirse con ahorro privado.
""")

    # -------------------------
    #   COLUMNA DERECHA — ESCENARIOS
    # -------------------------
    with col_right:
        st.markdown("### Escenarios SRG — Cómo interpretar la tabla")

        st.markdown("""
SRG ha calculado tres escenarios posibles para tu estrategia de ahorro:

- **Optimista**: si los mercados rinden mejor de lo esperado  
- **Base**: si se cumple la rentabilidad media asumida  
- **Pesimista**: si los mercados rinden por debajo del promedio  

Cada escenario muestra:

- La rentabilidad anual estimada  
- La brecha mensual que debes cubrir  
- El capital total que necesitarás acumular  
- La aportación mensual recomendada para alcanzar ese capital  
""")

        # Cálculo de escenarios
        rent_base = rentabilidad
        rent_opt = rent_base + 0.02
        rent_pes = max(0.0, rent_base - 0.02)

        def calcula_capital_y_aportacion(brecha_mensual, anos_jub, anos_hasta, rent_anual):
            if brecha_mensual <= 0:
                return 0, 0
            if rent_anual == 0:
                capital = brecha_mensual * 12 * anos_jub
            else:
                capital = brecha_mensual * 12 * (1 - (1 + rent_anual)**(-anos_jub)) / rent_anual

            meses = anos_hasta * 12
            r_mes = rent_anual / 12
            if meses <= 0:
                return capital, 0

            if rent_anual == 0:
                aport = capital / meses
            else:
                aport = capital * r_mes / ((1 + r_mes)**meses - 1)
            return capital, aport

        cap_opt, ap_opt = calcula_capital_y_aportacion(brecha, anos_jubilacion, anos_hasta_jub, rent_opt)
        cap_base, ap_base = calcula_capital_y_aportacion(brecha, anos_jubilacion, anos_hasta_jub, rent_base)
        cap_pes, ap_pes = calcula_capital_y_aportacion(brecha, anos_jubilacion, anos_hasta_jub, rent_pes)

        st.markdown("""
        <div style="overflow-x:auto;">
        """, unsafe_allow_html=True)

        st.markdown(f"""
| Escenario   | Rentabilidad | Brecha | Capital necesario | Aportación mensual |
|------------|--------------|--------|-------------------|---------------------|
| Optimista  | {rent_opt*100:,.1f}% | {brecha:,.0f} € | {cap_opt:,.0f} € | {ap_opt:,.0f} €/mes |
| Base       | {rent_base*100:,.1f}% | {brecha:,.0f} € | {cap_base:,.0f} € | {ap_base:,.0f} €/mes |
| Pesimista  | {rent_pes*100:,.1f}% | {brecha:,.0f} € | {cap_pes:,.0f} € | {ap_pes:,.0f} €/mes |
""")

        st.markdown("</div>", unsafe_allow_html=True)



# ============================================
#   MODO AGENTE SRG
# ============================================

st.markdown('<div class="srg-title">Modo Agente SRG</div>', unsafe_allow_html=True)
with st.expander("Guion comercial para explicar al cliente"):
    modo_agente = st.checkbox("Activar Modo Agente SRG", value=False)

    if modo_agente:
        st.markdown(f"""
**1. Situación actual**  
"Actualmente tienes **{anos_cotizados_hoy} años cotizados** y planeas cotizar **{anos_futuros} años más**, con una jubilación a los **{edad_prevista_jub} años**."

**2. Pensión pública estimada**  
"Con la modalidad **{tipo_jubilacion}**, tu pensión futura estimada sería de **{pension_futura:,.0f} €/mes**."

**3. Objetivo y brecha**  
"Tu objetivo de ingresos futuros es de **{objetivo_futuro:,.0f} €/mes**, y tus gastos futuros se estiman en **{gastos_futuros:,.0f} €/mes**.  
La brecha a cubrir es de **{brecha:,.0f} €/mes**."

**4. Plan de ahorro recomendado**  
"Para cubrir esta brecha, estimamos que necesitas acumular **{capital_necesario:,.0f} €** al jubilarte, con una aportación mensual aproximada de **{aportacion:,.0f} €/mes**, asumiendo una rentabilidad anual del **{rentabilidad*100:.1f}%** y una inflación del **{inflacion:.1f}%**."

**5. Cierre**  
"A partir de aquí, podemos diseñar juntos la combinación de productos de ahorro e inversión que mejor se adapte a tu perfil."
        """)
# ============================================
#   TEXTOS NARRATIVOS PARA INFORMES
# ============================================

def texto_cliente(contexto):
    return f"""
<h2>4. Conclusión personalizada</h2>

<p><b>Tu situación financiera actual demuestra que estás dando pasos sólidos hacia una jubilación estable y bien planificada.</b></p>

<p>Con los datos que nos has proporcionado, tu pensión futura estimada será de <b>{contexto['pension_futura']:,.0f} €/mes</b>, mientras que tu objetivo económico para mantener tu nivel de vida en jubilación asciende a <b>{contexto['objetivo_futuro']:,.0f} €/mes</b>.</p>

<p>Esto genera una brecha mensual de <b>{contexto['brecha']:,.0f} €</b>, que es completamente normal y aparece en la mayoría de los casos debido al efecto combinado de la inflación, la revalorización limitada de la pensión pública y el aumento del coste de vida.</p>

<p><b>La buena noticia es que esta brecha puede cubrirse con un plan de ahorro realista y perfectamente asumible.</b></p>

<p>Según tus datos, necesitarías acumular un capital aproximado de <b>{contexto['capital_necesario']:,.0f} €</b> al llegar a la jubilación, lo que se consigue con una aportación mensual estimada de <b>{contexto['aportacion']:,.0f} €/mes</b>, asumiendo una rentabilidad anual del <b>{contexto['rentabilidad']*100:.1f}%</b>.</p>

<p>Este plan te permite avanzar con seguridad hacia una jubilación tranquila, con ingresos suficientes para mantener tu estilo de vida y afrontar imprevistos.</p>

<p><b>Estás tomando decisiones inteligentes hoy que tendrán un impacto directo en tu bienestar futuro.</b></p>
"""


def texto_agente(contexto):
    return f"""
<h2>4. Explicación técnica detallada para el agente</h2>

<p><b>Cálculo de la pensión pública:</b><br>
La pensión futura se obtiene aplicando el porcentaje de base reguladora correspondiente a los años cotizados (<b>{contexto['anos_cotizados_hoy'] + contexto['anos_futuros']} años</b>) y ajustándolo por el coeficiente de jubilación (<b>{contexto['coef_ajuste']:.3f}</b>) según la modalidad seleccionada (<b>{contexto['tipo_jubilacion']}</b>). Posteriormente se proyecta hasta la edad de jubilación aplicando la revalorización anual.</p>

<p><b>Cálculo del objetivo económico:</b><br>
El objetivo mensual futuro se calcula actualizando los ingresos deseados mediante la inflación anual durante <b>{contexto['anos_hasta_jub']} años</b>.</p>

<p><b>Cálculo de la brecha:</b><br>
La brecha mensual (<b>{contexto['brecha']:,.0f} €</b>) es la diferencia entre el objetivo económico futuro y la pensión futura estimada.</p>

<p><b>Cálculo del capital necesario:</b><br>
El capital necesario (<b>{contexto['capital_necesario']:,.0f} €</b>) se obtiene descontando la renta mensual deseada durante los años de jubilación a la rentabilidad anual asumida.</p>

<p><b>Cálculo de la aportación mensual:</b><br>
La aportación mensual (<b>{contexto['aportacion']:,.0f} €/mes</b>) se calcula como la cuota necesaria para alcanzar el capital objetivo en <b>{contexto['anos_hasta_jub']} años</b>, aplicando la fórmula de acumulación con aportaciones periódicas y rentabilidad compuesta.</p>

<p><b>Evolución mensual del ahorro:</b><br>
La tabla y la gráfica muestran la evolución del capital mes a mes, desglosando aportaciones, rendimientos, inflación y capital neto real.</p>
"""

def informe_cliente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Informe Cliente SRG</title>

<style>

    /* FIX PARA STREAMLIT CLOUD */
    html, body {{
        width: 100% !important;
        max-width: 100% !important;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    body {{
        font-family: 'Montserrat', sans-serif;
        background-color: #f4f6fb;
        color: #222;
        margin: 0;
        padding: 0;
    }}

    /* PORTADA */
    .srg-cover {{
        height: 260px;
        background: linear-gradient(135deg, #003366, #0055A4);
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px 20px;
        border-bottom: 4px solid rgba(255,255,255,0.25);
    }}

    .srg-cover-title {{
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }}

    .srg-cover-subtitle {{
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }}

    .srg-cover-client {{
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }}

    .srg-cover-date {{
        font-size: 0.95rem;
        opacity: 0.85;
        margin-bottom: 2.5rem;
    }}

    .srg-cover-footer-line {{
        width: 240px;
        height: 1px;
        background-color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
    }}

    .srg-cover-footer-text {{
        font-size: 0.85rem;
        margin-top: 0.5rem;
        opacity: 0.9;
        letter-spacing: 0.05em;
    }}

    /* CONTENEDOR */
    .srg-container {{
        max-width: 900px;
        margin: 40px auto 60px auto;
        background-color: #ffffff;
        padding: 32px 40px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
        border-radius: 12px;
    }}

    h2 {{
        color: #003366;
        font-size: 1.4rem;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
        position: relative;
        padding-left: 14px;
    }}

    h2::before {{
        content: "";
        position: absolute;
        left: 0;
        top: 0.15rem;
        width: 4px;
        height: 1.3rem;
        background-color: #0055A4;
        border-radius: 4px;
    }}

    p {{
        line-height: 1.55;
        font-size: 0.98rem;
        margin-bottom: 0.7rem;
    }}

    /* TARJETAS */
    .srg-cards {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 10px;
        margin-bottom: 8px;
    }}

    .srg-card {{
        background-color: #f7f9fc;
        border-radius: 10px;
        padding: 12px 14px;
        border: 1px solid #e1e6f0;
    }}

    .srg-card-label {{
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #0055A4;
        margin-bottom: 2px;
    }}

    .srg-card-value {{
        font-size: 1.1rem;
        font-weight: 600;
    }}

    /* TABLAS */
    .srg-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 0.86rem;
    }}

    .srg-table th {{
        background-color: #0055A4;
        color: #ffffff;
        padding: 7px;
        text-align: left;
        font-weight: 600;
    }}

    .srg-table td {{
        border-bottom: 1px solid #e1e6f0;
        padding: 6px 7px;
    }}

    .srg-table tr:nth-child(even) td {{
        background-color: #f7f9fc;
    }}

    /* CAJA DESTACADA */
    .srg-highlight-box {{
        border: 1px solid #0055A4;
        border-radius: 10px;
        padding: 12px 16px;
        background-color: #f9fbff;
        margin-top: 8px;
    }}

    /* GRÁFICA */
    .srg-chart-container {{
        margin-top: 10px;
        margin-bottom: 10px;
        padding: 10px 12px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border: 1px solid #e1e6f0;
    }}

    /* FOOTER */
    .srg-footer {{
        text-align: center;
        font-size: 0.78rem;
        color: #777;
        margin: 30px 0 10px 0;
    }}

    .srg-footer-line {{
        width: 100%;
        height: 1px;
        background-color: #e1e6f0;
        margin-bottom: 6px;
    }}

</style>
</head>

<body>

<!-- PORTADA -->
<div class="srg-cover">
    <div class="srg-cover-title">Informe de Proyección de Jubilación SRG</div>
    <div class="srg-cover-subtitle">Simulación personalizada</div>
    <div class="srg-cover-client">Informe para: <b>{contexto['nombre_cliente'] or "Cliente SRG"}</b></div>
    <div class="srg-cover-date">Fecha de generación: {fecha}</div>
    <div class="srg-cover-footer-line"></div>
    <div class="srg-cover-footer-text">SRG Consultora Financiera · Herramienta de planificación y educación financiera</div>
</div>

<!-- CONTENIDO -->
<div class="srg-container">

    <h2>1. Resumen ejecutivo</h2>

    <div class="srg-cards">
        <div class="srg-card">
            <div class="srg-card-label">Pensión futura estimada</div>
            <div class="srg-card-value">{contexto['pension_futura']:,.0f} €/mes</div>
        </div>
        <div class="srg-card">
            <div class="srg-card-label">Objetivo mensual futuro</div>
            <div class="srg-card-value">{contexto['objetivo_futuro']:,.0f} €</div>
        </div>
        <div class="srg-card">
            <div class="srg-card-label">Brecha mensual</div>
            <div class="srg-card-value">{contexto['brecha']:,.0f} €</div>
        </div>
        <div class="srg-card">
            <div class="srg-card-label">Aportación mensual recomendada</div>
            <div class="srg-card-value">{contexto['aportacion']:,.0f} €/mes</div>
        </div>
    </div>

    <h2>2. Datos del cliente</h2>
    <table class="srg-table">
        <tr><th>Campo</th><th>Valor</th></tr>
        <tr><td>Nombre</td><td>{contexto['nombre_cliente']}</td></tr>
        <tr><td>Email</td><td>{contexto['email_cliente']}</td></tr>
        <tr><td>Teléfono</td><td>{contexto['telefono_cliente']}</td></tr>
        <tr><td>Edad actual</td><td>{contexto['edad_actual']} años</td></tr>
        <tr><td>Edad prevista de jubilación</td><td>{contexto['edad_prevista_jub']} años</td></tr>
    </table>

    <h2>3. Evolución del ahorro</h2>
    <table class="srg-table">
        <tr>
            <th>Mes</th>
            <th>Aportación acumulada</th>
            <th>Capital total</th>
            <th>Inflación</th>
            <th>Neto real</th>
        </tr>
        {tabla_mensual_y_anual_html(contexto['evolucion'], contexto['anos_hasta_jub'])}
    </table>

    <h2>4. Gráfica de evolución</h2>
    <div class="srg-chart-container">
        {fig.to_html(include_plotlyjs='cdn', full_html=False)}
    </div>

    <h2>5. Explicación de tus resultados</h2>
    <div class="srg-highlight-box">
        <p><b>Cómo se calcula tu pensión futura:</b> Tu pensión pública estimada se obtiene a partir de los años cotizados, el tipo de jubilación elegido y la revalorización anual prevista.</p>
        <p><b>Cómo calculamos tu objetivo económico:</b> Actualizamos tus gastos deseados aplicando la inflación durante los próximos <b>{contexto['anos_hasta_jub']} años</b>.</p>
        <p><b>Qué es la brecha mensual:</b> Es la diferencia entre lo que necesitarás para vivir y lo que aportará tu pensión pública.</p>
        <p><b>Cómo calculamos el capital necesario:</b> Para cubrir esa brecha durante tus años de jubilación, estimamos el capital total que deberías tener acumulado.</p>
        <p><b>Cómo se obtiene tu aportación mensual recomendada:</b> Calculamos cuánto deberías ahorrar cada mes desde hoy hasta tu jubilación.</p>
    </div>

    <h2>6. Conclusión personalizada</h2>
    <p><b>Estás dando un paso importante hacia una jubilación tranquila y bien planificada.</b></p>

    <div class="srg-footer">
        <div class="srg-footer-line"></div>
        <div>Informe generado automáticamente por SRG Consultora Financiera.</div>
        <div>{datetime.date.today().year}</div>
    </div>

</div>
</body>
</html>
"""
    return html


def informe_agente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Informe Agente SRG</title>

<style>

    /* FIX PARA STREAMLIT CLOUD */
    html, body {{
        width: 100% !important;
        max-width: 100% !important;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    body {{
        font-family: 'Montserrat', sans-serif;
        background-color: #f4f6fb;
        color: #222;
        margin: 0;
        padding: 0;
    }}

    /* PORTADA */
    .srg-cover {{
        height: 260px;
        background: linear-gradient(135deg, #003366, #0055A4);
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px 20px;
        border-bottom: 4px solid rgba(255,255,255,0.25);
    }}

    .srg-cover-title {{
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }}

    .srg-cover-subtitle {{
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }}

    .srg-cover-client {{
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }}

    .srg-cover-date {{
        font-size: 0.95rem;
        opacity: 0.85;
        margin-bottom: 2.5rem;
    }}

    .srg-cover-footer-line {{
        width: 240px;
        height: 1px;
        background-color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
    }}

    .srg-cover-footer-text {{
        font-size: 0.85rem;
        margin-top: 0.5rem;
        opacity: 0.9;
        letter-spacing: 0.05em;
    }}

    /* CONTENEDOR */
    .srg-container {{
        max-width: 950px;
        margin: 40px auto 60px auto;
        background-color: #ffffff;
        padding: 32px 40px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
        border-radius: 12px;
    }}

    h2 {{
        color: #003366;
        font-size: 1.4rem;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
        position: relative;
        padding-left: 14px;
    }}

    h2::before {{
        content: "";
        position: absolute;
        left: 0;
        top: 0.15rem;
        width: 4px;
        height: 1.3rem;
        background-color: #0055A4;
        border-radius: 4px;
    }}

    p {{
        line-height: 1.55;
        font-size: 0.98rem;
        margin-bottom: 0.7rem;
    }}

    /* TABLAS */
    .srg-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 0.86rem;
    }}

    .srg-table th {{
        background-color: #0055A4;
        color: #ffffff;
        padding: 7px;
        text-align: left;
        font-weight: 600;
    }}

    .srg-table td {{
        border-bottom: 1px solid #e1e6f0;
        padding: 6px 7px;
    }}

    .srg-table tr:nth-child(even) td {{
        background-color: #f7f9fc;
    }}

    /* CAJAS DESTACADAS */
    .srg-highlight-box {{
        border: 1px solid #0055A4;
        border-radius: 10px;
        padding: 12px 16px;
        background-color: #f9fbff;
        margin-top: 8px;
    }}

    /* GRÁFICA */
    .srg-chart-container {{
        margin-top: 10px;
        margin-bottom: 10px;
        padding: 10px 12px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border: 1px solid #e1e6f0;
    }}

    /* FOOTER */
    .srg-footer {{
        text-align: center;
        font-size: 0.78rem;
        color: #777;
        margin: 30px 0 10px 0;
    }}

    .srg-footer-line {{
        width: 100%;
        height: 1px;
        background-color: #e1e6f0;
        margin-bottom: 6px;
    }}

</style>
</head>

<body>

<!-- PORTADA -->
<div class="srg-cover">
    <div class="srg-cover-title">Informe Técnico SRG</div>
    <div class="srg-cover-subtitle">Uso interno para agente</div>
    <div class="srg-cover-client">Cliente: <b>{contexto['nombre_cliente'] or "Cliente SRG"}</b></div>
    <div class="srg-cover-date">Fecha de generación: {fecha}</div>
    <div class="srg-cover-footer-line"></div>
    <div class="srg-cover-footer-text">SRG Consultora Financiera · Soporte técnico para el análisis de jubilación</div>
</div>

<!-- CONTENIDO -->
<div class="srg-container">

    <h2>1. Resumen técnico</h2>
    <p>Este informe está diseñado como soporte para el agente, con foco en los parámetros técnicos, hipótesis y cálculos utilizados en la simulación.</p>

    <div class="srg-highlight-box">
        <p><b>Pensión futura estimada:</b> {contexto['pension_futura']:,.0f} €/mes</p>
        <p><b>Brecha mensual estimada:</b> {contexto['brecha']:,.0f} €</p>
        <p><b>Aportación mensual recomendada:</b> {contexto['aportacion']:,.0f} €/mes</p>
    </div>

    <h2>2. Datos del cliente</h2>
    <table class="srg-table">
        <tr><th>Campo</th><th>Valor</th></tr>
        <tr><td>Nombre</td><td>{contexto['nombre_cliente']}</td></tr>
        <tr><td>Email</td><td>{contexto['email_cliente']}</td></tr>
        <tr><td>Teléfono</td><td>{contexto['telefono_cliente']}</td></tr>
        <tr><td>Edad actual</td><td>{contexto['edad_actual']} años</td></tr>
        <tr><td>Edad prevista de jubilación</td><td>{contexto['edad_prevista_jub']} años</td></tr>
        <tr><td>Años cotizados hoy</td><td>{contexto['anos_cotizados_hoy']} años</td></tr>
        <tr><td>Años futuros hasta jubilación</td><td>{contexto['anos_futuros']} años</td></tr>
    </table>

    <h2>3. Parámetros y supuestos</h2>
    <div class="srg-highlight-box">
        <p><b>Tipo de jubilación:</b> {contexto['tipo_jubilacion']}</p>
        <p><b>Coeficiente aplicado:</b> {contexto['coef_ajuste']:.3f}</p>
        <p><b>Rentabilidad anual asumida:</b> {contexto['rentabilidad']*100:.1f}%</p>
        <p><b>Inflación anual asumida:</b> {contexto['inflacion']:.1f}%</p>
        <p><b>Años hasta la jubilación:</b> {contexto['anos_hasta_jub']} años</p>
        <p><b>Años estimados en jubilación:</b> {contexto['anos_jubilacion']} años</p>
    </div>

    <h2>4. Explicación técnica detallada</h2>
    <div class="srg-highlight-box">
        <p><b>Cálculo de la pensión pública:</b> La pensión futura se obtiene aplicando el porcentaje de base reguladora correspondiente a los años cotizados (<b>{contexto['anos_cotizados_hoy'] + contexto['anos_futuros']} años</b>) y ajustándolo por el coeficiente (<b>{contexto['coef_ajuste']:.3f}</b>).</p>

        <p><b>Cálculo del objetivo económico:</b> Se actualizan los ingresos deseados aplicando la inflación durante <b>{contexto['anos_hasta_jub']} años</b>.</p>

        <p><b>Cálculo de la brecha:</b> Diferencia entre objetivo económico (<b>{contexto['objetivo_futuro']:,.0f} €</b>) y pensión futura (<b>{contexto['pension_futura']:,.0f} €/mes</b>).</p>

        <p><b>Cálculo del capital necesario:</b> Se descuenta la renta mensual deseada durante <b>{contexto['anos_jubilacion']} años</b> a la rentabilidad asumida.</p>

        <p><b>Cálculo de la aportación mensual:</b> Cuota necesaria para alcanzar el capital objetivo en <b>{contexto['anos_hasta_jub']} años</b>.</p>
    </div>

    <h2>5. Evolución del ahorro</h2>
    <table class="srg-table">
        <tr>
            <th>Mes</th>
            <th>Aportación acumulada</th>
            <th>Capital total</th>
            <th>Inflación</th>
            <th>Capital neto real</th>
        </tr>
        {tabla_mensual_y_anual_html(contexto['evolucion'], contexto['anos_hasta_jub'])}
    </table>

    <h2>6. Gráfica de evolución</h2>
    <div class="srg-chart-container">
        {fig.to_html(include_plotlyjs='cdn', full_html=False)}
    </div>

    <h2>7. Comentario técnico</h2>
    <p>Este caso ilustra la importancia de complementar la pensión pública con ahorro privado.</p>

    <div class="srg-footer">
        <div class="srg-footer-line"></div>
        <div>Informe técnico interno para agentes SRG.</div>
        <div>SRG Consultora Financiera · {datetime.date.today().year}</div>
    </div>

</div>
</body>
</html>
"""
    return html



# ============================================
#   RESUMEN EJECUTIVO SRG
# ============================================

st.markdown('<div class="srg-title">Resumen ejecutivo</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

colR1, colR2, colR3, colR4 = st.columns(4)

with colR1:
    st.metric("Pensión futura", f"{pension_futura:,.0f} €/mes")

with colR2:
    st.metric("Objetivo mensual futuro", f"{objetivo_futuro:,.0f} €")

with colR3:
    st.metric("Brecha mensual", f"{brecha:,.0f} €")

with colR4:
    st.metric("Aportación mensual", f"{aportacion:,.0f} €")
=======
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIMULACIONES, INFORMES Y PANEL DE DESCARGA
# ============================================

st.markdown('<div class="srg-title">Simulaciones de ahorro</div>', unsafe_allow_html=True)
st.caption("Todas las simulaciones usan la misma brecha y la misma rentabilidad anual asumida para mantener coherencia en el análisis.")

tab1, tab2, tab3 = st.tabs(["Cuota recomendada", "Simular mi cuota", "Comparativa de cuotas"])

cuota_cliente = 0.0
capital_total_cliente = 0.0
porc_cobertura_cliente = 0.0
brecha_restante_cliente = brecha
comparativa_cuotas = []
evolucion_cliente = None

# TAB 1 — ESCENARIO RECOMENDADO
with tab1:
    st.markdown("### Escenario recomendado")
    st.write(
        "Este escenario utiliza la aportación mensual recomendada para cubrir la brecha "
        "calculada en función de tus datos y de la rentabilidad asumida."
    )
    st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €/mes")
    st.metric("Capital total al jubilarte", f"{capital_total_recom:,.0f} €")
    st.metric("Capital neto (ajustado por inflación)", f"{capital_real_final_recom:,.0f} €")

    with st.expander("📘 Explicación del escenario recomendado"):
        st.markdown(f"""
        - La brecha mensual que se quiere cubrir es de **{brecha:,.0f} €**, calculada según tu elección:  
          **{tipo_brecha_descripcion}**.  
        - La rentabilidad anual asumida es del **{rentabilidad_pct:,.1f}%**, aplicada de forma mensual.  
        - La cuota recomendada se diseña para que, al llegar a la jubilación, el capital acumulado permita cubrir esa brecha durante {anos_jubilacion} años.

        Este escenario es la referencia base para comparar otras cuotas y ver cómo cambian el capital y la cobertura.
        """)

# TAB 2 — SIMULAR CUOTA DEL CLIENTE
with tab2:
    st.markdown("### Simular mi cuota")

    cuota_cliente = st.number_input(
        "Cuota mensual que quieres aportar (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(round(aportacion_recom, 0)) if aportacion_recom > 0 else 100.0,
        step=10.0,
        help="Introduce la cuota mensual que deseas aportar.",
        key="cuota_cliente_input_tab2"
    )

    if cuota_cliente > 0:
        evolucion_cliente = calcular_evolucion_mensual(
            anos_hasta_jub, rentabilidad_pct, inflacion, cuota_cliente
        )

        capital_total_cliente = evolucion_cliente[-1].get("total", 0.0)
        capital_real_final_cliente = evolucion_cliente[-1].get("neta", 0.0)

        porc_cobertura_cliente = (
            min(capital_total_cliente / capital_necesario, 1.0) * 100
            if capital_necesario > 0 else 100.0
        )

        brecha_restante_cliente = brecha * (1 - porc_cobertura_cliente / 100.0)

        st.metric("Capital total con tu cuota", f"{capital_total_cliente:,.0f} €")
        st.metric("Capital neto con tu cuota", f"{capital_real_final_cliente:,.0f} €")
        st.metric("Cobertura de la brecha", f"{porc_cobertura_cliente:,.1f} %")
        st.metric("Brecha mensual restante", f"{brecha_restante_cliente:,.0f} €")

        st.write("#### Resumen de tu cuota")
        df_resumen_cuota = pd.DataFrame({
            "Concepto": [
                "Cuota mensual elegida",
                "Capital total estimado",
                "Capital neto ajustado por inflación",
                "Cobertura de la brecha",
                "Brecha mensual restante"
            ],
            "Valor": [
                f"{cuota_cliente:,.0f} €",
                f"{capital_total_cliente:,.0f} €",
                f"{capital_real_final_cliente:,.0f} €",
                f"{porc_cobertura_cliente:,.1f} %",
                f"{brecha_restante_cliente:,.0f} €"
            ]
        })
        st.table(df_resumen_cuota)

        with st.expander("📘 Explicación de la simulación de tu cuota"):
            st.markdown(f"""
            Esta simulación mantiene la misma brecha (**{brecha:,.0f} €**) y la misma rentabilidad anual (**{rentabilidad_pct:,.1f}%**),
            pero sustituye la cuota recomendada por la cuota que tú eliges.

            - Si tu cuota es **mayor** que la recomendada, el capital final y la cobertura de la brecha aumentan.  
            - Si tu cuota es **menor**, el capital final baja y la brecha restante aumenta.  
            - La rentabilidad actúa igual que en el escenario recomendado: cuanto mayor sea, más crece tu capital con el tiempo.

            Así puedes ver el impacto real de tu decisión de cuota sobre tu jubilación.
            """)

        with st.expander("Detalle de la evolución con tu cuota"):
            evo_cli = [row for row in evolucion_cliente if "mes" in row]
            if len(evo_cli) > 1:
                evo_cli_sin0 = evo_cli[1:]
                anos_cli = [fila["mes"]/12 for fila in evo_cli_sin0]
                total_cli = [fila["total"] for fila in evo_cli_sin0]
                aportada_cli = [fila["aportada"] for fila in evo_cli_sin0]
                neta_cli = [fila["neta"] for fila in evo_cli_sin0]

                fig_cli = go.Figure()
                fig_cli.add_trace(go.Scatter(
                    x=anos_cli, y=total_cli,
                    mode='lines', name='Total acumulado',
                    line=dict(color='#00BFFF', width=3)
                ))
                fig_cli.add_trace(go.Scatter(
                    x=anos_cli, y=aportada_cli,
                    mode='lines', name='Aportado',
                    line=dict(color='#00FFAA', width=2, dash='dash')
                ))
                fig_cli.add_trace(go.Scatter(
                    x=anos_cli, y=neta_cli,
                    mode='lines', name='Neto ajustado inflación',
                    line=dict(color='#FF00AA', width=2)
                ))

                fig_cli.update_layout(
                    height=380,
                    plot_bgcolor='#0A0F1F',
                    paper_bgcolor='#0A0F1F',
                    xaxis_title="Años hasta jubilación",
                    yaxis_title="Capital (€)",
                    font=dict(color="#EAF2FF")
                )
                st.plotly_chart(fig_cli, use_container_width=True)
            else:
                st.info("Evolución insuficiente para mostrar gráfico.")
    else:
        st.info("Introduce una cuota mensual mayor que 0 para simular tu propio escenario.")

# TAB 3 — COMPARATIVA DE CUOTAS
with tab3:
    st.markdown("### Comparativa de cuotas")
    st.write("Esta tabla compara distintos niveles de aportación y su impacto en el capital final y en la cobertura de la brecha.")

    cuota_base = st.number_input(
        "Cuota base para la comparativa (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(round(aportacion_recom, 0)),
        step=10.0,
        key="cuota_base_input_tab3"
    )

    rango = st.number_input(
        "Rango de variación por escenario (€)",
        min_value=10.0,
        max_value=1000.0,
        value=50.0,
        step=10.0,
        key="rango_input_tab3"
    )

    cuotas_escenarios = [
        max(cuota_base - rango, 0),
        cuota_base,
        cuota_base + rango,
        cuota_base + 2 * rango
    ]

    comparativa_cuotas = []

    for c in cuotas_escenarios:
        if c <= 0:
            continue
        evo = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad_pct, inflacion, c)
        cap_tot = evo[-1].get("total", 0.0)
        porc_cov = (
            min(cap_tot / capital_necesario, 1.0) * 100
            if capital_necesario > 0 else 100.0
        )
        brecha_rest = brecha * (1 - porc_cov / 100.0)
        comparativa_cuotas.append({
            "cuota": c,
            "capital": cap_tot,
            "porc_cobertura": porc_cov,
            "brecha_restante": brecha_rest
        })

    if comparativa_cuotas:
        st.write("#### Tabla comparativa de escenarios")
        df_comp = pd.DataFrame([{
            "Cuota mensual (€)": f"{x['cuota']:,.0f}",
            "Capital final (€)": f"{x['capital']:,.0f}",
            "Cobertura brecha (%)": f"{x['porc_cobertura']:,.1f}",
            "Brecha restante (€)": f"{x['brecha_restante']:,.0f}"
        } for x in comparativa_cuotas])
        st.table(df_comp)

        mejor = max(comparativa_cuotas, key=lambda x: x["porc_cobertura"])
        st.markdown("#### Resumen automático")
        st.markdown(
            f"- Con una cuota de **{mejor['cuota']:,.0f} €/mes** cubrirías aproximadamente **{mejor['porc_cobertura']:,.1f}%** de la brecha.\n"
            f"- La brecha mensual restante sería de **{mejor['brecha_restante']:,.0f} €**."
        )

        with st.expander("📘 Explicación de la comparativa de cuotas"):
            st.markdown(f"""
            La comparativa mantiene constante la brecha (**{brecha:,.0f} €**) y la rentabilidad anual (**{rentabilidad_pct:,.1f}%**),
            y solo varía la cuota mensual.

            - Escenarios con cuotas más altas generan más capital y mayor cobertura.  
            - Escenarios con cuotas más bajas dejan más brecha sin cubrir.  
            - Todos los escenarios se calculan con la misma lógica de rentabilidad y horizonte de jubilación.

            Esto te permite elegir el equilibrio entre esfuerzo mensual y nivel de cobertura que quieres alcanzar.
            """)
    else:
        st.info("Ajusta la cuota base y el rango para generar escenarios válidos.")
>>>>>>> origin/main

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
<<<<<<< HEAD
#   FILA — GENERAR INFORME + DESCARGAR INFORME
# ============================================

col_gen, col_desc = st.columns([1, 1])

# -------- COLUMNA 1: GENERAR INFORME --------
with col_gen:
    st.markdown('<div class="srg-title">Generar informe</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    subcol1, subcol2 = st.columns([1, 1])

    with subcol1:
        tipo_informe = st.radio(
            "Tipo de informe",
            ["Cliente", "Agente"],
            help="Selecciona el tipo de informe que deseas generar."
        )

    with subcol2:
        with st.expander("Datos del cliente"):
            nombre_cliente = st.text_input("Nombre del cliente")
            email_cliente = st.text_input("Email del cliente")
            telefono_cliente = st.text_input("Teléfono del cliente")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- CONTEXTO DEL INFORME --------
=======
# BLOQUE 5 — CONTEXTO PDF, INFORMES Y PANEL SRG
# ============================================

>>>>>>> origin/main
contexto_pdf = {
    "edad_actual": edad_actual,
    "edad_prevista_jub": edad_prevista_jub,
    "anos_cotizados_hoy": anos_cotizados_hoy,
    "anos_futuros": anos_futuros,
    "tipo_jubilacion": tipo_jubilacion,
    "pension_futura": pension_futura,
    "coef_ajuste": coef_ajuste,
    "objetivo_futuro": objetivo_futuro,
    "gastos_futuros": gastos_futuros,
    "brecha": brecha,
<<<<<<< HEAD
    "capital_necesario": capital_necesario,
    "aportacion": aportacion,
    "rentabilidad": rentabilidad,
    "inflacion": inflacion,
    "anos_hasta_jub": anos_hasta_jub,
    "anos_jubilacion": anos_jubilacion,
    "evolucion": evolucion,
    "nombre_cliente": nombre_cliente,
    "email_cliente": email_cliente,
    "telefono_cliente": telefono_cliente
}

# ============================
#   GENERAR INFORME + DESCARGA
# ============================

col_gen, col_desc = st.columns([1, 1])

with col_gen:
    st.markdown('<div class="srg-title">Generar informe</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    subcol1, subcol2 = st.columns([1, 1])

    with subcol1:
        tipo_informe = st.radio(
            "Tipo de informe",
            ["Cliente", "Agente"],
            help="Selecciona el tipo de informe que deseas generar."
        )

    with subcol2:
        with st.expander("Datos del cliente"):
            nombre_cliente = st.text_input("Nombre del cliente")
            email_cliente = st.text_input("Email del cliente")
            telefono_cliente = st.text_input("Teléfono del cliente")

    st.markdown('</div>', unsafe_allow_html=True)

# Contexto para informes
contexto_pdf = {
    "edad_actual": edad_actual,
    "edad_prevista_jub": edad_prevista_jub,
    "anos_cotizados_hoy": anos_cotizados_hoy,
    "anos_futuros": anos_futuros,
    "tipo_jubilacion": tipo_jubilacion,
    "pension_futura": pension_futura,
    "coef_ajuste": coef_ajuste,
    "objetivo_futuro": objetivo_futuro,
    "gastos_futuros": gastos_futuros,
    "brecha": brecha,
    "capital_necesario": capital_necesario,
    "aportacion": aportacion,
    "rentabilidad": rentabilidad,
    "inflacion": inflacion,
    "anos_hasta_jub": anos_hasta_jub,
    "anos_jubilacion": anos_jubilacion,
    "evolucion": evolucion,
    "nombre_cliente": nombre_cliente,
    "email_cliente": email_cliente,
    "telefono_cliente": telefono_cliente
}

# Generar HTML
if tipo_informe == "Cliente":
    html_informe = informe_cliente(contexto_pdf, fig)
else:
    html_informe = informe_agente(contexto_pdf, fig)

bytes_informe = html_informe.encode("utf-8")

with col_desc:
    st.markdown('<div class="srg-title">Vista previa y descarga</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    with st.expander("Resumen del informe"):
        st.write(f"**Pensión futura estimada:** {pension_futura:,.0f} €/mes")
        st.write(f"**Objetivo mensual futuro:** {objetivo_futuro:,.0f} €")
        st.write(f"**Gastos futuros estimados:** {gastos_futuros:,.0f} €")
        st.write(f"**Brecha mensual:** {brecha:,.0f} €")
        st.write(f"**Aportación mensual recomendada:** {aportacion:,.0f} €/mes")

        if nombre_cliente:
            st.write("---")
            st.write("### Datos del cliente")
            st.write(f"**Nombre:** {nombre_cliente}")
            st.write(f"**Email:** {email_cliente}")
            st.write(f"**Teléfono:** {telefono_cliente}")

    # Vista previa en pantalla (pantalla)
    with st.expander("Vista previa del informe (HTML)"):
        components.html(html_informe, height=700, scrolling=True)

    # Descarga HTML imprimible (PDF desde navegador)
    st.download_button(
        label="Descargar informe SRG (HTML imprimible)",
        data=bytes_informe,
        file_name="informe_jubilacion_srg.html",
        mime="text/html"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ============================
#   FOOTER PROFESIONAL SRG
# ============================

footer_html = """
<div class="srg-footer">
    <div><b>Simulador SRG — Samuel Ruiz González </b></div>
    <div>Herramienta educativa y formativa para Agentes.</div>
    <div>© 2025 Samuel Ruiz González · <a href="#">Política de privacidad</a> · <a href="#">Aviso legal</a></div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
=======
    "modo_brecha": modo_brecha,
    "tipo_brecha_descripcion": tipo_brecha_descripcion,
    "capital_necesario": capital_necesario,
    "aportacion_recom": aportacion_recom,
    "rentabilidad": rentabilidad_pct,
    "inflacion": inflacion,
    "anos_hasta_jub": anos_hasta_jub,
    "anos_jubilacion": anos_jubilacion,
    "evolucion_recom": evolucion_recom,
    "nombre_cliente": "",
    "email_cliente": "",
    "telefono_cliente": "",
    "cuota_cliente": cuota_cliente,
    "capital_total_cliente": capital_total_cliente,
    "porc_cobertura_cliente": porc_cobertura_cliente,
    "brecha_restante_cliente": brecha_restante_cliente,
    "comparativa_cuotas": comparativa_cuotas,
    "capital_total_recom": capital_total_recom,
    "capital_real_final_recom": capital_real_final_recom,
    "capital_real_final_cliente": 0.0,
    "modo_ahorro_extra": False,
    "cuota_ahorro_extra": 0.0,
    "objetivo_ahorro_extra": "",
    "evolucion_ahorro_extra": [],
    "comparativa_ahorro_extra": []
}

RANGO_COMPARATIVA = 40

# COMPARATIVA PARA INFORME RECOMENDADO (SI HAY BRECHA)
if brecha > 0:
    cuotas_recom = [
        max(aportacion_recom - RANGO_COMPARATIVA, 0),
        aportacion_recom,
        aportacion_recom + RANGO_COMPARATIVA,
        aportacion_recom + 2 * RANGO_COMPARATIVA
    ]

    comparativa_recom = []
    for c in cuotas_recom:
        if c <= 0:
            continue
        evo = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad_pct, inflacion, c)
        cap_tot = evo[-1].get("total", 0.0)
        porc_cov = min(cap_tot / capital_necesario, 1.0) * 100 if capital_necesario > 0 else 100.0
        brecha_rest = brecha * (1 - porc_cov / 100.0)
        comparativa_recom.append({
            "cuota": c,
            "capital": cap_tot,
            "porc_cobertura": porc_cov,
            "brecha_restante": brecha_rest
        })

    contexto_pdf["comparativa_cuotas"] = comparativa_recom
else:
    contexto_pdf["comparativa_cuotas"] = []

def informe_cliente(contexto, fig, tipo_informe="Cuota recomendada"):
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    brecha_valor = contexto.get("brecha", 0.0)
    brecha_rest = contexto.get("brecha_restante_cliente", 0.0)
    modo_ahorro_extra = contexto.get("modo_ahorro_extra", False)

    explicacion_brecha_html = ""
    if brecha_valor == 0:
        explicacion_brecha_html = """
        <div style="margin-top:8px;padding:10px 14px;background:#f9fbff;
        border-left:4px solid #0055A4;border-radius:6px;">
            <b>💡 Tu pensión cubre tu nivel de vida previsto.</b><br>
            No necesitas ahorrar para cubrir una brecha económica. A partir de aquí, cualquier ahorro que realices será
            <b>capital adicional</b> para tus objetivos personales: vivienda, estudios de tus hijos, viajes, protección frente a imprevistos o legado familiar.
        </div>
        """

    explicacion_brecha_rest_html = ""
    if brecha_rest == 0 and brecha_valor > 0:
        explicacion_brecha_rest_html = """
        <div style="margin-top:8px;padding:10px 14px;background:#f9fbff;
        border-left:4px solid #0055A4;border-radius:6px;">
            <b>💡 Brecha mensual restante 0 €.</b><br>
            Con tu cuota actual, la brecha económica queda completamente cubierta.
            Tu ahorro proyectado compensa toda la diferencia entre tu pensión futura y el nivel de vida deseado.
        </div>
        """

    pensiones_html = """
    <div style="margin-top:12px;padding:10px 14px;background:#fff7e6;
    border-left:4px solid #ff9900;border-radius:6px;font-size:0.9rem;">
        <b>📌 Sobre el sistema público de pensiones:</b><br>
        El sistema de pensiones funciona en régimen de <b>reparto</b>: las cotizaciones de los trabajadores de hoy
        financian las pensiones de los jubilados actuales. Esto implica que tu pensión futura dependerá de factores
        demográficos, económicos y políticos que no podemos controlar (envejecimiento de la población, nivel de empleo,
        decisiones presupuestarias, etc.).<br><br>
        Por eso, complementar la pensión pública con un <b>plan de ahorro privado</b> es una estrategia prudente:
        te permite construir tu propio capital, independiente de las decisiones futuras del Estado, aprovechando el
        interés compuesto y una planificación a largo plazo.
    </div>
    """

    capital_total_recom = contexto.get("capital_total_recom", 0.0)
    capital_real_final_recom = contexto.get("capital_real_final_recom", 0.0)
    capital_total_cliente = contexto.get("capital_total_cliente", 0.0)
    capital_real_final_cliente = contexto.get("capital_real_final_cliente", 0.0)

    ahorro_extra_html = ""
    if modo_ahorro_extra:
        cuota_ahorro = contexto.get("cuota_ahorro_extra", 0.0)
        objetivo_ahorro = contexto.get("objetivo_ahorro_extra", "")
        evo_extra = contexto.get("evolucion_ahorro_extra", [])
        cap_extra = evo_extra[-1].get("total", 0.0) if evo_extra else 0.0
        cap_extra_neto = evo_extra[-1].get("neta", 0.0) if evo_extra else 0.0

        ahorro_extra_html = f"""
        <h2>Plan de ahorro voluntario sin brecha</h2>
        <div class="srg-highlight-box">
            <p><b>Objetivo de ahorro:</b> {objetivo_ahorro or 'Capital adicional para tus proyectos personales'}</p>
            <p><b>Aportación mensual propuesta:</b> {cuota_ahorro:,.0f} €/mes</p>
            <p><b>Capital estimado al jubilarte:</b> {cap_extra:,.0f} €</p>
            <p><b>Capital neto estimado (ajustado por inflación):</b> {cap_extra_neto:,.0f} €</p>
            <p>Este plan no cubre una brecha, sino que <b>crea patrimonio adicional</b> para tus objetivos:
            vivienda, estudios de tus hijos, viajes, protección frente a imprevistos o legado familiar.</p>
        </div>

        <h2>Comparativa de cuotas de ahorro</h2>
        <table class="srg-table">
            <tr><th>Cuota</th><th>Capital final</th><th>Capital neto</th></tr>
        """

        for esc in contexto.get("comparativa_ahorro_extra", []):
            ahorro_extra_html += f"<tr><td>{esc['cuota']:,.0f} €</td><td>{esc['capital']:,.0f} €</td><td>{esc['neta']:,.0f} €</td></tr>"

        ahorro_extra_html += """
        </table>

        <h2>Gráfica del plan de ahorro voluntario</h2>
        """ + fig.to_html(include_plotlyjs='cdn', full_html=False)

    html = f"""
<html>
<head><meta charset="UTF-8"><title>Informe Cliente SRG</title>
<style>
body {{ font-family: 'Montserrat', sans-serif; background-color:#f4f6fb; margin:0; padding:0; }}
.srg-container {{ max-width:950px; margin:40px auto; background:white; padding:32px 40px; border-radius:12px; }}
.srg-table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:0.86rem; }}
.srg-table th {{ background-color:#0055A4; color:white; padding:7px; text-align:left; }}
.srg-table td {{ border-bottom:1px solid #e1e6f0; padding:6px 7px; }}
.srg-highlight-box {{ border:1px solid #0055A4; background:#f9fbff; padding:12px 16px; border-radius:10px; margin-top:8px; }}
.srg-footer {{ text-align:center; font-size:0.8rem; color:#666; margin-top:20px; }}
</style>
</head>
<body>
{marca_agua_srg()}

<div class="srg-cover" style="height:160px;background:linear-gradient(135deg,#003366,#0055A4);
color:white;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:20px;">
    <h1>Informe de Proyección de Jubilación SRG</h1>
    <p>Cliente: <b>{contexto['nombre_cliente'] or 'Cliente SRG'}</b> — Fecha: {fecha}</p>
</div>

<div class="srg-container">
    <div style="padding:6px 10px;border-radius:6px;background:#eef6ff;color:#003366;
    display:inline-block;font-weight:600;margin-bottom:8px;">{tipo_informe}</div>

    <h2>1. Resumen ejecutivo</h2>
    <div class="srg-highlight-box">
        <p><b>Pensión futura estimada:</b> {contexto['pension_futura']:,.0f} €/mes</p>
        <p><b>Objetivo mensual futuro:</b> {contexto['objetivo_futuro']:,.0f} €</p>
        <p><b>Brecha mensual:</b> {brecha_valor:,.0f} €</p>
        <p><b>Aportación recomendada:</b> {contexto['aportacion_recom']:,.0f} €/mes</p>
        <p><b>Capital total recomendado:</b> {capital_total_recom:,.0f} €</p>
        <p><b>Capital neto recomendado:</b> {capital_real_final_recom:,.0f} €</p>
    </div>
    {explicacion_brecha_html}
    {pensiones_html}

    <h2>2. Escenario con tu cuota</h2>
    <div class="srg-highlight-box">
        <p><b>Tu cuota:</b> {contexto.get('cuota_cliente', 0.0):,.0f} €/mes</p>
        <p><b>Capital final:</b> {capital_total_cliente:,.0f} €</p>
        <p><b>Capital neto:</b> {capital_real_final_cliente:,.0f} €</p>
        <p><b>Brecha mensual restante:</b> {brecha_rest:,.0f} €</p>
        {explicacion_brecha_rest_html}
    </div>

    <h2>3. Comparativa de cuotas</h2>
    <table class="srg-table">
        <tr><th>Cuota</th><th>Capital final</th><th>Cobertura</th><th>Brecha restante</th></tr>
"""

    for esc in contexto.get("comparativa_cuotas", []):
        html += f"<tr><td>{esc['cuota']:,.0f} €</td><td>{esc['capital']:,.0f} €</td><td>{esc['porc_cobertura']:,.1f}%</td><td>{esc['brecha_restante']:,.0f} €</td></tr>"

    html += f"""
    </table>

    <h2>4. Evolución del ahorro (brecha / cuota)</h2>
    <table class="srg-table">
        <tr><th>Mes/Año</th><th>Aportado</th><th>Total</th><th>Inflación</th><th>Neto</th></tr>
        {tabla_mensual_y_anual_html(contexto.get('evolucion_recom', []), contexto.get('anos_hasta_jub', 1))}
    </table>

    <h2>5. Gráfica</h2>
    {fig.to_html(include_plotlyjs='cdn', full_html=False)}

    {ahorro_extra_html}

    <div class="srg-footer">
        Simulador SRG — Samuel Ruiz González<br>
        Herramienta educativa y formativa para Agentes.<br>
        © 2026 Samuel Ruiz González
    </div>

</div>
</body>
</html>
"""
    return html

def informe_agente(contexto, fig, tipo_informe="Cuota recomendada"):
    return informe_cliente(contexto, fig, tipo_informe).replace(
        "Informe de Proyección de Jubilación SRG",
        "Informe Técnico SRG"
    )

html_cliente_recom = informe_cliente(contexto_pdf, fig, tipo_informe="Cuota recomendada")
html_agente_recom = informe_agente(contexto_pdf, fig, tipo_informe="Cuota recomendada")

bytes_cliente_recom = html_cliente_recom.encode("utf-8")
bytes_agente_recom = html_agente_recom.encode("utf-8")

# PANEL SRG
st.markdown('<div class="srg-title">Panel de herramientas SRG</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

col_left, col_right = st.columns([0.55, 0.45])

with col_left:
    st.markdown('<div class="srg-title">Modo Agente SRG</div>', unsafe_allow_html=True)
    modo_agente = st.checkbox("Activar Modo Agente SRG", value=False, key="modo_agente_input")

    with st.expander("Datos del cliente"):
        contexto_pdf["nombre_cliente"] = st.text_input(
            "Nombre del cliente",
            value=contexto_pdf.get("nombre_cliente", ""),
            key="nombre_cliente_input"
        )
        contexto_pdf["email_cliente"] = st.text_input(
            "Email del cliente",
            value=contexto_pdf.get("email_cliente", ""),
            key="email_cliente_input"
        )
        contexto_pdf["telefono_cliente"] = st.text_input(
            "Teléfono del cliente",
            value=contexto_pdf.get("telefono_cliente", ""),
            key="telefono_cliente_input"
        )

        if st.button("Regenerar informe recomendado (cuota recomendada)", key="regenerar_recom_btn"):
            html_cliente_recom = informe_cliente(contexto_pdf, fig, tipo_informe="Cuota recomendada")
            html_agente_recom = informe_agente(contexto_pdf, fig, tipo_informe="Cuota recomendada")
            bytes_cliente_recom = html_cliente_recom.encode("utf-8")
            bytes_agente_recom = html_agente_recom.encode("utf-8")
            st.success("Informes recomendados regenerados correctamente.")

with col_right:
    st.markdown('<div class="srg-title">Vista previa y descargas (Cuota recomendada)</div>', unsafe_allow_html=True)
    st.caption("Visualiza y descarga los informes generados para la cuota recomendada.")

    col_cli, col_ag = st.columns(2)

    with col_cli:
        st.markdown("**Informe Cliente SRG**")
        with st.expander("Vista previa"):
            components.html(html_cliente_recom, height=300, scrolling=True)
        st.download_button(
            label="Descargar Informe Cliente",
            data=bytes_cliente_recom,
            file_name=f"informe_cliente_recomendado_{datetime.date.today().isoformat()}.html",
            mime="text/html",
            key="download_recom_cliente"
        )

    with col_ag:
        st.markdown("**Informe Agente SRG**")
        with st.expander("Vista previa"):
            components.html(html_agente_recom, height=300, scrolling=True)
        st.download_button(
            label="Descargar Informe Agente",
            data=bytes_agente_recom,
            file_name=f"informe_agente_recomendado_{datetime.date.today().isoformat()}.html",
            mime="text/html",
            key="download_recom_agente"
        )

st.markdown('</div>', unsafe_allow_html=True)

# MÓDULO AZUL 1 — CUOTA ELEGIDA POR EL CLIENTE
st.markdown("""
<div style="
    background: linear-gradient(135deg, #004080, #0055A4);
    color: white;
    padding: 14px 20px;
    border-radius: 10px;
    margin-top: 20px;
    margin-bottom: 18px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
">
    <h3 style="margin-bottom: 6px; font-weight: 500;">Generar informe con la cuota elegida por el cliente</h3>
    <p style="font-size: 0.9rem; color: #e6e9ef; line-height: 1.4;">
        Introduce la cuota mensual que el cliente desea aportar para generar su informe personalizado.
        El resultado mostrará la evolución del ahorro y la comparativa de escenarios.
    </p>
</div>
""", unsafe_allow_html=True)

cuota_confirm_input = st.number_input(
    "Cuota elegida por el cliente para generar informe (€)",
    min_value=0.0,
    max_value=50000.0,
    value=float(contexto_pdf.get("cuota_cliente", aportacion_recom)),
    step=1.0,
    key="cuota_confirm_input_panel"
)

if st.button("Confirmar cuota elegida y generar informe", key="confirmar_cuota_btn"):
    cuota_cliente = cuota_confirm_input

    evolucion_cliente = calcular_evolucion_mensual(
        anos_hasta_jub, rentabilidad_pct, inflacion, cuota_cliente
    )
    capital_total_cliente = evolucion_cliente[-1].get("total", 0.0)
    capital_real_final_cliente = evolucion_cliente[-1].get("neta", 0.0)
    porc_cobertura_cliente = (
        min(capital_total_cliente / capital_necesario, 1.0) * 100
        if capital_necesario > 0 else 100.0
    )
    brecha_restante_cliente = brecha * (1 - porc_cobertura_cliente / 100.0)

    cuotas_cli = [
        max(cuota_cliente - RANGO_COMPARATIVA, 0),
        cuota_cliente,
        cuota_cliente + RANGO_COMPARATIVA,
        cuota_cliente + 2 * RANGO_COMPARATIVA
    ]

    comparativa_cli = []
    for c in cuotas_cli:
        if c <= 0:
            continue
        evo = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad_pct, inflacion, c)
        cap_tot = evo[-1].get("total", 0.0)
        porc_cov = (
            min(cap_tot / capital_necesario, 1.0) * 100
            if capital_necesario > 0 else 100.0
        )
        brecha_rest = brecha * (1 - porc_cov / 100.0)
        comparativa_cli.append({
            "cuota": c,
            "capital": cap_tot,
            "porc_cobertura": porc_cov,
            "brecha_restante": brecha_rest
        })

    contexto_cli = contexto_pdf.copy()
    contexto_cli.update({
        "cuota_cliente": cuota_cliente,
        "capital_total_cliente": capital_total_cliente,
        "capital_real_final_cliente": capital_real_final_cliente,
        "porc_cobertura_cliente": porc_cobertura_cliente,
        "brecha_restante_cliente": brecha_restante_cliente,
        "evolucion_recom": evolucion_cliente,
        "comparativa_cuotas": comparativa_cli,
        "modo_ahorro_extra": False
    })

    html_cli = informe_cliente(contexto_cli, fig, tipo_informe="Cuota elegida por el cliente")
    html_ag = informe_agente(contexto_cli, fig, tipo_informe="Cuota elegida por el cliente")

    bytes_cli_elegido = html_cli.encode("utf-8")
    bytes_ag_elegido = html_ag.encode("utf-8")

    st.download_button(
        "Descargar Informe Cliente (Cuota elegida)",
        bytes_cli_elegido,
        file_name=f"informe_cliente_cuota_elegida_{datetime.date.today().isoformat()}.html",
        mime="text/html",
        key="download_cli_elegida"
    )

    st.download_button(
        "Descargar Informe Agente (Cuota elegida)",
        bytes_ag_elegido,
        file_name=f"informe_agente_cuota_elegida_{datetime.date.today().isoformat()}.html",
        mime="text/html",
        key="download_ag_elegida"
    )

    st.success("Informes generados para la cuota elegida.")

# MÓDULO AZUL 2 — PLAN DE AHORRO SIN BRECHA
if brecha == 0:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #003366, #0055A4);
        color: white;
        padding: 25px 30px;
        border-radius: 12px;
        margin-top: 35px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <h2 style="margin-bottom: 10px;">Plan de ahorro recomendado (sin brecha económica)</h2>
        <p style="font-size: 0.95rem; color: #e6e9ef;">
            Tu pensión futura cubre tu nivel de vida previsto.
            Este módulo te permite construir capital adicional para tus objetivos personales,
            aprovechando el interés compuesto y la rentabilidad anual esperada.
        </p>
    </div>
    """, unsafe_allow_html=True)

    objetivo_ahorro_extra = st.text_input(
        "Objetivo de tu plan de ahorro (ej. vivienda, estudios hijos, viaje, legado)",
        value=contexto_pdf.get("objetivo_ahorro_extra", ""),
        key="objetivo_ahorro_extra_input"
    )

    cuota_ahorro_extra = st.number_input(
        "Cuota mensual de ahorro voluntario (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(contexto_pdf.get("cuota_ahorro_extra", 100.0)),
        step=10.0,
        key="cuota_ahorro_extra_input"
    )

    if st.button("Simular plan de ahorro voluntario", key="simular_ahorro_extra_btn"):
        evolucion_ahorro_extra = calcular_evolucion_mensual(
            anos_hasta_jub, rentabilidad_pct, inflacion, cuota_ahorro_extra
        )

        capital_extra = evolucion_ahorro_extra[-1].get("total", 0.0)
        capital_extra_neto = evolucion_ahorro_extra[-1].get("neta", 0.0)

        cuotas_extra = [
            max(cuota_ahorro_extra - RANGO_COMPARATIVA, 0),
            cuota_ahorro_extra,
            cuota_ahorro_extra + RANGO_COMPARATIVA,
            cuota_ahorro_extra + 2 * RANGO_COMPARATIVA
        ]

        comparativa_ahorro_extra = []
        for c in cuotas_extra:
            if c <= 0:
                continue
            evo = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad_pct, inflacion, c)
            cap_tot = evo[-1].get("total", 0.0)
            cap_neta = evo[-1].get("neta", 0.0)
            comparativa_ahorro_extra.append({
                "cuota": c,
                "capital": cap_tot,
                "neta": cap_neta
            })

        contexto_ahorro = contexto_pdf.copy()
        contexto_ahorro.update({
            "modo_ahorro_extra": True,
            "cuota_ahorro_extra": cuota_ahorro_extra,
            "objetivo_ahorro_extra": objetivo_ahorro_extra,
            "evolucion_ahorro_extra": evolucion_ahorro_extra,
            "comparativa_ahorro_extra": comparativa_ahorro_extra,
            "cuota_cliente": cuota_ahorro_extra,
            "capital_total_cliente": capital_extra,
            "capital_real_final_cliente": capital_extra_neto,
            "brecha_restante_cliente": 0.0,
            "comparativa_cuotas": [],
            "evolucion_recom": evolucion_ahorro_extra
        })

        html_cli_ahorro = informe_cliente(
            contexto_ahorro, fig, tipo_informe="Plan de ahorro recomendado sin brecha"
        )
        html_ag_ahorro = informe_agente(
            contexto_ahorro, fig, tipo_informe="Plan de ahorro recomendado sin brecha"
        )

        bytes_cli_ahorro = html_cli_ahorro.encode("utf-8")
        bytes_ag_ahorro = html_ag_ahorro.encode("utf-8")

        st.download_button(
            "Descargar Informe Cliente (Plan de ahorro)",
            bytes_cli_ahorro,
            file_name=f"informe_cliente_ahorro_extra_{datetime.date.today().isoformat()}.html",
            mime="text/html",
            key="download_cli_ahorro_extra"
        )

        st.download_button(
            "Descargar Informe Agente (Plan de ahorro)",
            bytes_ag_ahorro,
            file_name=f"informe_agente_ahorro_extra_{datetime.date.today().isoformat()}.html",
            mime="text/html",
            key="download_ag_ahorro_extra"
        )

        st.success("Plan de ahorro voluntario simulado y listo para descargar en informe.")

# FOOTER SRG
footer_html = """
<div class="srg-footer">
    Simulador SRG — Samuel Ruiz González<br>
    Herramienta educativa y formativa para Agentes.<br>
    © 2026 Samuel Ruiz González
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

# ============================================
# BLOQUE 6 — DISEÑO FUTURISTA SRG (CSS FINAL)
# ============================================

st.markdown("""
<style>
/* ============================================================
   FIX DEFINITIVO SRG — TOOLTIP, HELP, EXPLICACIONES, INPUT
   ============================================================ */

/* HELP TEXT (como el de “Ordinaria”) */
div[data-testid="stHelp"] {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4) !important;
}

/* TOOLTIP DEL SIGNO DE INTERROGACIÓN */
div[data-baseweb="tooltip"] {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4) !important;
}

/* TEXTO INTERNO DEL TOOLTIP */
div[data-baseweb="tooltip"] * {
    color: #EAF2FF !important;
}

/* EXPLICACIÓN DE BRECHA — fondo oscuro */
div[style*="background:#f9fbff"] {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
}

/* INPUT DE CUOTA — limitar ancho */
div[data-testid="stNumberInput"] {
    max-width: 600px !important;
    margin: 0 auto !important;
}

/* FONDO GENERAL */
html, body, [class*="css"], div[data-testid="stAppViewContainer"] {
    background-color: #05070D !important;
    background-image: none !important;
    color: #F5F9FF !important;
    font-family: 'Inter', 'Montserrat', sans-serif !important;
}

/* TEXTOS */
label, .stMarkdown, .stCaption, p, span {
    color: #EAF2FF !important;
}

/* INPUTS FUTURISTAS */
input[type="number"], input[type="text"], select, textarea {
    background-color: #0C1426 !important;
    color: #F5F9FF !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
    box-shadow: inset 0 0 12px rgba(0,191,255,0.4), 0 0 10px rgba(0,191,255,0.3) !important;
}
input:focus, select:focus, textarea:focus {
    outline: none !important;
    box-shadow: 0 0 22px rgba(0,191,255,0.8) !important;
}

/* MÉTRICAS */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"], div[data-testid="stMarkdownContainer"] strong {
    color: #00E0FF !important;
    text-shadow: 0 0 8px rgba(0,191,255,0.6) !important;
    font-weight: 600 !important;
}

/* MENSAJES POSITIVO / NEGATIVO */
.msg-ok-srg {
    background-color: #1E6FFF !important;
    border: 1px solid #4DA3FF !important;
    color: #FFFFFF !important;
    padding: 12px 16px !important;
    border-radius: 10px !important;
    margin-top: 10px !important;
    font-weight: 600 !important;
    text-shadow: none !important;
}
            /* ============================================================
   FIX DEFINITIVO — TOOLTIP, FONDO BLANCO Y INPUT DE CUOTA
   ============================================================ */

/* TOOLTIP — fondo oscuro estable incluso al perder hover */
[data-testid="stTooltipHoverTarget"] div {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4);
    padding: 6px 10px !important;
    border-radius: 6px !important;
    transition: background-color 0.3s ease-in-out;
}

/* Evitar que se ponga blanco al salir el ratón */
[data-testid="stTooltipHoverTarget"] * {
    color: #EAF2FF !important;
    background-color: transparent !important;
    opacity: 1 !important;
}

/* SELECTBOX — mantener estilo azul degradado */
div[data-testid="stSelectbox"] div[role="button"] {
    background: linear-gradient(135deg, #003366, #0055A4) !important;
    color: #FFFFFF !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
    box-shadow: 0 0 10px rgba(0,191,255,0.3) !important;
}

/* INPUT DE CUOTA — limitar ancho máximo y centrar */
input[id*="cuota_confirm_input_panel"] {
    max-width: 600px !important;
    width: 100% !important;
    margin: 0 auto !important;
    display: block !important;
}

.msg-error-srg {
    background-color: #FFCCCC !important;
    border: 1px solid #FF6666 !important;
    color: #660000 !important;
    padding: 12px 16px !important;
    border-radius: 10px !important;
    margin-top: 10px !important;
    font-weight: 700 !important;
    text-shadow: none !important;
}

/* GRÁFICAS */
.stPlotlyChart {
    background-color: #0A0F1F !important;
    border-radius: 12px !important;
    box-shadow: 0 0 20px rgba(0,191,255,0.35) !important;
}
.js-plotly-plot .plotly .bg {
    fill: #0A0F1F !important;
}
.js-plotly-plot .plotly .grid {
    stroke: rgba(0,191,255,0.25) !important;
}
.js-plotly-plot .plotly .axis text,
.js-plotly-plot .plotly .legend text {
    fill: #EAF2FF !important;
}

/* TOOLTIP FUTURISTA */
[data-testid="stTooltipIcon"] svg {
    fill: #00BFFF !important;
    filter: drop-shadow(0 0 6px rgba(0,191,255,0.6));
}
div[data-testid="stTooltipHoverTarget"] div,
div[data-testid="stTooltipHoverTarget"]:hover div {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4);
    padding: 6px 10px !important;
    border-radius: 6px !important;
}
div[data-testid="stTooltipHoverTarget"] * {
    color: #EAF2FF !important;
    text-shadow: none !important;
    opacity: 1 !important;
}
.msg-green-srg {
    background-color: #0F4D0F !important;
    border: 1px solid #33CC33 !important;
    color: #CCFFCC !important;
    padding: 12px 16px !important;
    border-radius: 10px !important;
    margin-top: 10px !important;
    font-weight: 600 !important;
}
/* EXPANDERS — FONDO OSCURO ESTABLE */
div[data-testid="stExpander"] {
    background-color: #0A0F1F !important;
    border: 1px solid #00BFFF !important;
    border-radius: 8px !important;
    color: #EAF2FF !important;
}

/* TÍTULO DEL EXPANDER */
div[data-testid="stExpander"] button {
    background-color: #0A0F1F !important;
    color: #EAF2FF !important;
    border-radius: 8px !important;
}

/* TEXTO INTERNO DEL EXPANDER */
div[data-testid="stExpander"] * {
    color: #EAF2FF !important;
}

/* EVITAR CAMBIO DE COLOR AL HACER HOVER */
div[data-testid="stExpander"]:hover,
div[data-testid="stExpander"] button:hover {
    background-color: #0A0F1F !important;
    color: #EAF2FF !important;
}
/* BOTONES FUTURISTAS */
button[kind="primary"],
button {
    background-color: #003366 !important;
    color: #FFFFFF !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
    box-shadow: 0 0 12px rgba(0,191,255,0.4) !important;
}

/* HOVER */
button:hover {
    background-color: #0055A4 !important;
    color: #FFFFFF !important;
}

/* EVITAR QUE SE PONGAN BLANCOS AL PERDER FOCUS */
button:focus:not(:active) {
    background-color: #003366 !important;
    color: #FFFFFF !important;
}
/* ALINEAR SELECTBOX "TIPO PREVISTO" CON LOS INPUTS */
div[data-testid="stSelectbox"] {
    margin-top: -6px !important;   /* sube el selectbox */
    vertical-align: middle !important;
}

/* Ajuste adicional para mantener coherencia con los inputs */
div[data-testid="stSelectbox"] label {
    margin-bottom: 4px !important;
    color: #EAF2FF !important;
}

</style>
""", unsafe_allow_html=True)


>>>>>>> origin/main
