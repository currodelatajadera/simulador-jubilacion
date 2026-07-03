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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&display=swap');

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

/* ============================================================
   TITULOS Y BLOQUES
   ============================================================ */
.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

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
    )

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
        min_value=edad_actual + 1,
        max_value=75,
        help="Edad a la que deseas jubilarte. No puede ser menor o igual que tu edad actual.",
        key="edad_prevista_jub_input"
    )

    esperanza_vida = st.number_input(
        "Esperanza de vida",
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
    )

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
        min_value=0,
        max_value=max_anos_futuros,
        help="Años adicionales que seguirás cotizando.",
        key="anos_futuros_input"
    )

    st.markdown('</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
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

    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
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
    )

    reval = st.number_input(
        "Revalorización anual pensión (%)",
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

    modo_brecha = st.radio(
        "¿Qué quieres cubrir?",
        ["Objetivo económico", "Gastos reales"],
        horizontal=True,
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

  
