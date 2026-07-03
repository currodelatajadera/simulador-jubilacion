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

/* Fuente global */
body, html {
    font-family: 'Montserrat', sans-serif !important;
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

/* TITULOS */
.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
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
        key="edad_actual_input"
    )

    with st.expander("ℹ️ Explicación: Edad actual"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Tu edad hoy. Se usa para calcular cuántos años faltan hasta la jubilación.
        </div>
        """, unsafe_allow_html=True)

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
        min_value=edad_actual + 1,
        max_value=75,
        key="edad_prevista_jub_input"
    )

    with st.expander("ℹ️ Explicación: Edad prevista de jubilación"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Edad a la que deseas jubilarte. No puede ser menor o igual que tu edad actual.
        </div>
        """, unsafe_allow_html=True)

    esperanza_vida = st.number_input(
        "Esperanza de vida",
        min_value=75,
        max_value=100,
        key="esperanza_vida_input"
    )

    with st.expander("ℹ️ Explicación: Esperanza de vida"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Estimación de años que vivirás según estadísticas.
        </div>
        """, unsafe_allow_html=True)

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
        key="anos_cotizados_hoy_input"
    )

    with st.expander("ℹ️ Explicación: Años cotizados hoy"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Años cotizados a la Seguridad Social.
        </div>
        """, unsafe_allow_html=True)

    max_anos_futuros = max(0, edad_prevista_jub - edad_actual)
    st.session_state.anos_futuros_input = min(
        st.session_state.anos_futuros_input, max_anos_futuros
    )

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
        min_value=0,
        max_value=max_anos_futuros,
        key="anos_futuros_input"
    )

    with st.expander("ℹ️ Explicación: Años futuros de cotización"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Años adicionales que seguirás cotizando.
        </div>
        """, unsafe_allow_html=True)

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
    st.caption("Modalidad,requisitos, anticipos, penalizaciones y bonificaciones según normativa 2026.")

    opciones_jub = ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"]
    idx_tipo = opciones_jub.index(st.session_state.tipo_jubilacion_input)

    tipo_jubilacion = st.selectbox(
        "Tipo prevista",
        opciones_jub,
        index=idx_tipo,
        key="tipo_jubilacion_input"
    )

    with st.expander("📘 Tipos de jubilación (Normativa España 2026)"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:16px;border-left:4px solid #00BFFF;border-radius:6px;">
        <b>1. Jubilación ordinaria</b><br>
        Edad legal: <b>67 años</b> (o 65 si se acreditan 38 años y 6 meses cotizados).<br>
        Requisitos: <b>mínimo 15 años cotizados</b>.<br>
        Penalización: <b>ninguna</b>.<br><br>

        <b>2. Anticipada voluntaria</b><br>
        Adelanto máximo: <b>24 meses</b>.<br>
        Requisitos: <b>35 años cotizados</b>.<br><br>

        <b>3. Anticipada involuntaria</b><br>
        Adelanto máximo: <b>48 meses</b>.<br>
        Requisitos: <b>33 años cotizados</b>.<br><br>

        <b>4. Demorada</b><br>
        Bonificación: <b>+4% por cada año completo de demora</b>.
        </div>
        """, unsafe_allow_html=True)

    modo_valido = True
    motivo_error = ""
    coef_ajuste = 1.0
    meses_anticipo = 0

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

    # ORDINARIA
    if tipo_jubilacion == "Ordinaria":
        if anos_totales < 15:
            modo_valido = False
            motivo_error = "No cumples los 15 años cotizados mínimos para la jubilación ordinaria."
        elif edad_prevista_jub < EDAD_LEGAL_2026:
            st.warning(f"La edad prevista ({edad_prevista_jub}) es inferior a la edad legal ({EDAD_LEGAL_2026}). Se aplicará la edad legal.")
            edad_prevista_jub = EDAD_LEGAL_2026

        st.markdown(
            '<div class="msg-ok-srg">La jubilación ordinaria requiere al menos 15 años cotizados y se aplica a la edad legal.</div>',
            unsafe_allow_html=True
        )

    # ANTICIPADA VOLUNTARIA
    elif tipo_jubilacion == "Anticipada voluntaria":
        if anos_totales < 35:
            modo_valido = False
            motivo_error = "No cumples los 35 años cotizados para la anticipada voluntaria."

        meses_anticipo = st.number_input(
            "Meses de anticipo",
            1, 24, 1,
            key="meses_anticipo_vol"
        )

        with st.expander("ℹ️ Explicación: Anticipada voluntaria"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
            Penalización según años cotizados, aplicada por trimestre de anticipo. Cuanto más cotizado, menor penalización.
            </div>
            """, unsafe_allow_html=True)

        edad_prevista_jub = EDAD_LEGAL_2026 - meses_anticipo / 12
        coef_ajuste = coef_voluntaria(anos_totales, meses_anticipo)

        st.markdown(
            '<div class="msg-ok-srg">Aplicando coeficientes reductores reales según años cotizados y meses de anticipo.</div>',
            unsafe_allow_html=True
        )

    # ANTICIPADA INVOLUNTARIA
    elif tipo_jubilacion == "Anticipada involuntaria":
        if anos_totales < 33:
            modo_valido = False
            motivo_error = "No cumples los 33 años cotizados para la anticipada involuntaria."

        meses_anticipo = st.number_input(
            "Meses de anticipo",
            1, 48, 1,
            key="meses_anticipo_inv"
        )

        with st.expander("ℹ️ Explicación: Anticipada involuntaria"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
            Penalización más suave que la voluntaria, depende de los años cotizados y se descuenta por trimestre.
            </div>
            """, unsafe_allow_html=True)

        edad_prevista_jub = EDAD_LEGAL_2026 - meses_anticipo / 12
        coef_ajuste = coef_involuntaria(anos_totales, meses_anticipo)

        st.markdown(
            '<div class="msg-ok-srg">Aplicando coeficientes reductores reales para anticipada involuntaria.</div>',
            unsafe_allow_html=True
        )

    # DEMORADA
    elif tipo_jubilacion == "Demorada":
        if edad_prevista_jub <= EDAD_LEGAL_2026:
            modo_valido = False
            motivo_error = f"Para demorada, la edad prevista debe ser mayor que {EDAD_LEGAL_2026}."
        else:
            anos_demora = edad_prevista_jub - EDAD_LEGAL_2026
            coef_ajuste = 1 + anos_demora * 0.04
            meses_demora = int(anos_demora * 12)
            st.metric("Meses de demora", f"{meses_demora} meses")

        st.markdown(
            '<div class="msg-ok-srg">Aplicando bonificación del 4% por cada año completo de demora.</div>',
            unsafe_allow_html=True
        )

    if not modo_valido:
        st.markdown(
            f'<div class="msg-error-srg">{motivo_error}</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# INGRESOS Y GASTOS
if "ingresos_input" not in st.session_state:
    st.session_state.ingresos_input = 2500

with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
    st.caption("Tus ingresos y gastos actuales nos permiten estimar tu objetivo económico futuro.")

    ingresos = st.number_input(
        "Ingresos mensuales (€)",
        min_value=0,
        max_value=20000,
        key="ingresos_input"
    )

    with st.expander("ℹ️ Explicación: Ingresos mensuales"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Tus ingresos netos actuales.
        </div>
        """, unsafe_allow_html=True)

    if "gastos_input" not in st.session_state:
        st.session_state.gastos_input = min(1800, ingresos)

    st.session_state.gastos_input = min(st.session_state.gastos_input, ingresos)

    gastos = st.number_input(
        "Gastos mensuales (€)",
        min_value=0,
        max_value=20000,
        key="gastos_input"
    )

    with st.expander("ℹ️ Explicación: Gastos mensuales"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        Tus gastos mensuales actuales.
        </div>
        """, unsafe_allow_html=True)

    if gastos > ingresos:
        st.warning("Has indicado más gastos que ingresos. Ajustamos los gastos al máximo igual a tus ingresos.")
        gastos = ingresos

    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)
# ============================================
# BLOQUE 4 — PENSIÓN, OBJETIVO Y BRECHA
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
        key="modo_br_input"
    )

    with st.expander("ℹ️ Explicación: Base reguladora"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
        La Base Reguladora se calcula con las bases de cotización de los últimos 29 años.
        </div>
        """, unsafe_allow_html=True)

    if modo_br == "Introducir base reguladora manualmente":
        base = st.number_input(
            "Base reguladora (€)",
            min_value=0,
            max_value=BASE_MAX_ESPANA_2026,
            value=1500,
            key="base_reguladora_input"
        )

        with st.expander("ℹ️ Explicación: Base reguladora manual"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
            Introduce directamente tu base reguladora estimada.
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("#### Calcular base reguladora SRG")
        st.caption("Los cálculos respetan los límites legales de cotización y pensión.")

        salario_actual = st.number_input(
            "Salario mensual actual (€)",
            min_value=0,
            max_value=20000,
            value=2000,
            key="salario_actual_input"
        )

        with st.expander("ℹ️ Explicación: Salario mensual actual"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
            Salario bruto mensual aproximado.
            </div>
            """, unsafe_allow_html=True)

        crecimiento_salarial = st.number_input(
            "Crecimiento salarial anual (%)",
            min_value=0.0,
            max_value=10.0,
            value=1.5,
            step=0.1,
            key="crecimiento_salarial_input"
        )

        with st.expander("ℹ️ Explicación: Crecimiento salarial"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
            Incremento medio anual de tu salario.
            </div>
            """, unsafe_allow_html=True)

        ipc_actualizacion = st.number_input(
            "Actualización IPC anual (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            key="ipc_actualizacion_input"
        )

        with st.expander("ℹ️ Explicación: IPC"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
            El IPC actualiza las bases antiguas para calcular la Base Reguladora SRG.
            </div>
            """, unsafe_allow_html=True)

        anos_con_salario = st.number_input(
            "Años cotizados con salario conocido",
            min_value=1,
            max_value=29,
            value=10,
            key="anos_con_salario_input"
        )

        with st.expander("ℹ️ Explicación: Años con salario conocido"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
            Años recientes con salario aproximado.
            </div>
            """, unsafe_allow_html=True)

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
        key="inflacion_input"
    )

    with st.expander("ℹ️ Explicación: Inflación"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
        La inflación reduce el poder adquisitivo.
        </div>
        """, unsafe_allow_html=True)

    reval = st.number_input(
        "Revalorización anual pensión (%)",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        key="reval_input"
    )

    with st.expander("ℹ️ Explicación: Revalorización"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
        Incremento anual previsto de la pensión.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="msg-ok-srg">En España existe una base máxima de cotización. Aunque ganes más, solo se computa hasta ese límite.</div>',
        unsafe_allow_html=True
    )

    with st.expander("📘 Explicación: IPC, inflación y revalorización"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:16px;border-left:4px solid #00BFFF;border-radius:6px;">
        - <b>IPC anual</b>: actualiza las bases antiguas.<br>
        - <b>Inflación anual</b>: proyecta el coste de vida futuro.<br>
        - <b>Revalorización</b>: cuánto subirá tu pensión cada año.
        </div>
        """, unsafe_allow_html=True)

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
            key="ingresos_hoy_input"
        )

        with st.expander("ℹ️ Explicación: Ingresos actuales"):
            st.markdown("""
            <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
            Este dato nos permite estimar tu nivel de vida actual.
            </div>
            """, unsafe_allow_html=True)

    porcentaje_gastos = st.number_input(
        "¿Qué parte de tus gastos crees que seguirás teniendo al jubilarte? (%)",
        min_value=50,
        max_value=110,
        value=90,
        key="porcentaje_gastos_input"
    )

    with st.expander("ℹ️ Explicación: Porcentaje de gastos"):
        st.markdown("""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:14px;border-left:4px solid #00BFFF;border-radius:6px;">
        Por ejemplo, si crees que gastarás el 90% de lo que gastas hoy, introduce 90.
        </div>
        """, unsafe_allow_html=True)

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
        <div style="background:#0A1A2F;color:#EAF2FF;padding:16px;border-left:4px solid #00BFFF;border-radius:6px;">
        <b>Brecha económica</b><br>
        Es la diferencia mensual entre tu pensión futura y el dinero que necesitarás para mantener tu nivel de vida.<br><br>
        - Si eliges <b>Objetivo económico</b>, la brecha se calcula respecto a {tipo_brecha_descripcion}.<br>
        - Si eliges <b>Gastos reales</b>, la brecha se calcula respecto a tus gastos actuales proyectados con inflación.<br><br>
        Esta brecha es la base de todo el plan de ahorro: determina el capital necesario y la cuota recomendada.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
# ============================================
# BLOQUE 5 — PLAN DE AHORRO + GRÁFICA + SIMULACIONES
# ============================================

st.markdown('<div class="srg-title">Plan de ahorro recomendado</div>', unsafe_allow_html=True)
st.caption("El plan se construye para cubrir la brecha que has elegido (objetivo económico o gastos reales) usando la rentabilidad asumida.")

col_left, col_right = st.columns([0.42, 0.58])

with col_left:
    st.markdown("Rentabilidad anual esperada (%)")

    # Estilo del input de rentabilidad
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

    # Explicación SRG oscura (sin tooltips)
    with st.expander("📘 Explicación de la cuota recomendada y la rentabilidad"):
        st.markdown(f"""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:16px;
                    border-left:4px solid #00BFFF;border-radius:6px;">
        La <b>cuota recomendada</b> se calcula para cubrir la brecha mensual de 
        <b>{brecha:,.0f} €</b> durante <b>{anos_jubilacion}</b> años de jubilación.<br><br>

        - Se asume una <b>rentabilidad anual</b> del <b>{rentabilidad_pct:,.1f}%</b>, aplicada de forma mensual.<br>
        - Cuanto mayor sea la rentabilidad, menor cuota necesitas.<br>
        - Si la rentabilidad baja, la cuota recomendada sube.<br><br>

        Esta cuota es el punto de referencia para todas las simulaciones posteriores.
        </div>
        """, unsafe_allow_html=True)

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
            font=dict(color="#EAF2FF", size=16)
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================
# SIMULACIÓN DE CUOTA ELEGIDA POR EL CLIENTE
# ============================================

st.markdown('<div class="srg-title">Cuota elegida por el cliente</div>', unsafe_allow_html=True)
st.caption("Simulación personalizada según la cuota que el cliente desea aportar.")

# Centrado y ancho controlado (sin moverse)
col_cuota, _ = st.columns([0.4, 0.6])
if "contexto_pdf" not in locals():
    contexto_pdf = {
        "cuota_cliente": aportacion_recom
    }

with col_cuota:
    cuota_confirm_input = st.number_input(
        "Cuota elegida por el cliente para generar informe (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(contexto_pdf.get("cuota_cliente", aportacion_recom)),
        step=1.0,
        key="cuota_confirm_input_panel"
    )

# Simulación con cuota del cliente
evolucion_cliente = calcular_evolucion_mensual(
    anos_hasta_jub, rentabilidad_pct, inflacion, cuota_confirm_input
)

capital_total_cliente = evolucion_cliente[-1].get("total", 0.0)
capital_real_final_cliente = evolucion_cliente[-1].get("neta", 0.0)

col_sim1, col_sim2 = st.columns(2)
with col_sim1:
    st.metric("Capital total con cuota del cliente", f"{capital_total_cliente:,.0f} €")
with col_sim2:
    st.metric("Capital neto con cuota del cliente", f"{capital_real_final_cliente:,.0f} €")

with st.expander("📘 Explicación de la simulación con cuota del cliente"):
    st.markdown(f"""
    <div style="background:#0A1A2F;color:#EAF2FF;padding:16px;
                border-left:4px solid #00BFFF;border-radius:6px;">
    Esta simulación calcula el capital final que obtendrás si aportas 
    <b>{cuota_confirm_input:,.0f} €</b> al mes durante <b>{anos_hasta_jub}</b> años.<br><br>

    - Si la cuota es mayor que la recomendada, alcanzarás el objetivo antes.<br>
    - Si es menor, el capital final será inferior al necesario.<br><br>

    Esta simulación te permite ajustar la cuota a tu capacidad real de ahorro.
    </div>
    """, unsafe_allow_html=True)
# ============================================
# BLOQUE 6 — DISEÑO FUTURISTA SRG (CSS FINAL)
# ============================================

st.markdown("""
<style>

/* ===========================
   ESTILO GLOBAL SRG
   =========================== */

html, body {
    background-color: #0A0F1F !important;
    color: #EAF2FF !important;
    font-family: 'Montserrat', sans-serif !important;
}

/* ===========================
   TITULOS SRG
   =========================== */

.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: #ffffff !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

/* ===========================
   MENSAJES OK / ERROR / INFO
   =========================== */

.msg-ok-srg {
    background-color: #0A1A2F;
    color: #EAF2FF;
    border-left: 4px solid #00BFFF;
    padding: 10px 14px;
    border-radius: 6px;
    margin-top: 6px;
}

.msg-error-srg {
    background-color: #2A0F1F;
    color: #FFB3B3;
    border-left: 4px solid #FF4D4D;
    padding: 10px 14px;
    border-radius: 6px;
    margin-top: 6px;
}

.msg-green-srg {
    background-color: #0A1A2F;
    color: #AAFFAA;
    border-left: 4px solid #00FFAA;
    padding: 10px 14px;
    border-radius: 6px;
    margin-top: 6px;
}

/* ===========================
   EXPANDERS SRG
   =========================== */

.streamlit-expanderHeader {
    background-color: #0C1426 !important;
    color: #EAF2FF !important;
    border-radius: 6px !important;
    padding: 6px !important;
}

.streamlit-expanderContent {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border-left: 4px solid #00BFFF !important;
    border-radius: 6px !important;
    padding: 12px 16px !important;
}

/* ===========================
   INPUTS SRG
   =========================== */

div[data-testid="stNumberInput"] input {
    background-color: #0C1426 !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
}

div[data-testid="stTextInput"] input {
    background-color: #0C1426 !important;
    color: #EAF2FF !important;
    border: 1px solid #00BFFF !important;
    border-radius: 6px !important;
}

/* ===========================
   SELECTBOX SRG
   =========================== */

div[data-baseweb="select"] {
    background-color: #0C1426 !important;
    color: #EAF2FF !important;
}

div[data-baseweb="select"] * {
    color: #EAF2FF !important;
}

/* ===========================
   RADIO BUTTONS SRG
   =========================== */

.stRadio > div {
    background-color: #0C1426 !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
}

.stRadio label {
    color: #EAF2FF !important;
}

/* ===========================
   MÉTRICAS SRG
   =========================== */

.css-1ht1j8u {
    background-color: #0C1426 !important;
    border-radius: 6px !important;
    padding: 12px !important;
}

.css-1ht1j8u * {
    color: #EAF2FF !important;
}

/* ===========================
   TABLAS SRG
   =========================== */

table {
    background-color: #0C1426 !important;
    color: #EAF2FF !important;
}

thead {
    background-color: #003366 !important;
    color: #ffffff !important;
}

tbody tr:nth-child(even) {
    background-color: #0A1A2F !important;
}

tbody tr:nth-child(odd) {
    background-color: #0C1426 !important;
}

/* ===========================
   BOTONES SRG
   =========================== */

.stButton button {
    background: linear-gradient(135deg, #0055A4, #0077CC) !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    border: none !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #0077CC, #0099FF) !important;
}

/* ===========================
   EXPANDER FIX (evita fondo blanco)
   =========================== */

div[style*="background:#f9fbff"] {
    background-color: #0A1A2F !important;
    color: #EAF2FF !important;
    border-left: 4px solid #00BFFF !important;
    border-radius: 6px !important;
}

/* ===========================
   CUOTA CLIENTE (centrado)
   =========================== */

div[data-testid="stNumberInput"] {
    max-width: 600px !important;
    margin: 0 auto !important;
}

</style>
""", unsafe_allow_html=True)
# ============================================
# BLOQUE 7 — INFORME PDF SRG (ARREGLADO)
# ============================================

st.markdown('<div class="srg-title">Informe PDF SRG</div>', unsafe_allow_html=True)
st.caption("Genera un informe profesional con todos los cálculos y simulaciones.")

# ============================
# PREPARACIÓN DEL CONTEXTO PDF
# ============================

contexto_pdf = {
    "edad_actual": edad_actual,
    "edad_prevista_jub": edad_prevista_jub,
    "esperanza_vida": esperanza_vida,
    "anos_cotizados_hoy": anos_cotizados_hoy,
    "anos_futuros": anos_futuros,
    "anos_totales": anos_totales,
    "tipo_jubilacion": tipo_jubilacion,
    "base_reguladora": base,
    "inflacion": inflacion,
    "reval": reval,
    "pension_hoy": pension_hoy,
    "pension_futura": pension_futura,
    "objetivo_futuro": objetivo_futuro,
    "gastos_futuros": gastos_futuros,
    "brecha": brecha,
    "capital_necesario": capital_necesario,
    "aportacion_recom": aportacion_recom,
    "capital_total_recom": capital_total_recom,
    "capital_real_final_recom": capital_real_final_recom,
    "cuota_cliente": cuota_confirm_input,
    "capital_total_cliente": capital_total_cliente,
    "capital_real_final_cliente": capital_real_final_cliente
}

# ============================
# HTML DEL INFORME (ARREGLADO)
# ============================

informe_html = f"""
<div style="background:#0A0F1F;color:#EAF2FF;padding:20px;font-family:Montserrat;">
    <h1 style="color:#00BFFF;">Informe de Jubilación SRG</h1>

    <h2 style="color:#00BFFF;">Datos personales</h2>
    <div style="background:#0A1A2F;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <p><b>Edad actual:</b> {edad_actual}</p>
        <p><b>Edad prevista de jubilación:</b> {edad_prevista_jub}</p>
        <p><b>Esperanza de vida:</b> {esperanza_vida}</p>
        <p><b>Años cotizados hoy:</b> {anos_cotizados_hoy}</p>
        <p><b>Años futuros de cotización:</b> {anos_futuros}</p>
        <p><b>Total años cotizados:</b> {anos_totales}</p>
    </div>

    <h2 style="color:#00BFFF;">Tipo de jubilación</h2>
    <div style="background:#0A1A2F;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <p><b>Modalidad:</b> {tipo_jubilacion}</p>
    </div>

    <h2 style="color:#00BFFF;">Base reguladora y pensión</h2>
    <div style="background:#0A1A2F;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <p><b>Base reguladora:</b> {base:,.0f} €</p>
        <p><b>Pensión ajustada hoy:</b> {pension_hoy:,.0f} €</p>
        <p><b>Pensión futura estimada:</b> {pension_futura:,.0f} €</p>
    </div>

    <h2 style="color:#00BFFF;">Nivel de vida y brecha</h2>
    <div style="background:#0A1A2F;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <p><b>Objetivo económico futuro:</b> {objetivo_futuro:,.0f} €</p>
        <p><b>Gastos futuros proyectados:</b> {gastos_futuros:,.0f} €</p>
        <p><b>Brecha mensual:</b> {brecha:,.0f} €</p>
    </div>

    <h2 style="color:#00BFFF;">Plan de ahorro recomendado</h2>
    <div style="background:#0A1A2F;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <p><b>Capital necesario:</b> {capital_necesario:,.0f} €</p>
        <p><b>Aportación mensual recomendada:</b> {aportacion_recom:,.0f} €</p>
        <p><b>Capital total recomendado:</b> {capital_total_recom:,.0f} €</p>
        <p><b>Capital neto recomendado:</b> {capital_real_final_recom:,.0f} €</p>
    </div>

    <h2 style="color:#00BFFF;">Simulación con cuota del cliente</h2>
    <div style="background:#0A1A2F;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <p><b>Cuota elegida:</b> {cuota_confirm_input:,.0f} €</p>
        <p><b>Capital total:</b> {capital_total_cliente:,.0f} €</p>
        <p><b>Capital neto:</b> {capital_real_final_cliente:,.0f} €</p>
    </div>

    <br><br>
    <p style="color:#00BFFF;text-align:center;">Simulador SRG — Informe generado automáticamente</p>
</div>
"""

# ============================
# BOTÓN PARA MOSTRAR HTML
# ============================

with st.expander("📄 Ver informe en HTML"):
    st.markdown(informe_html, unsafe_allow_html=True)

# ============================
# BOTÓN PARA GENERAR PDF
# ============================

if st.button("Generar PDF SRG"):
    try:
        import pdfkit
        pdfkit.from_string(informe_html, "informe_srg.pdf")
        st.success("PDF generado correctamente: informe_srg.pdf")
    except Exception as e:
        st.error(f"Error al generar PDF: {e}")
import shutil
if shutil.which("wkhtmltopdf") is None:
    st.error("wkhtmltopdf no está instalado. Descárgalo desde https://wkhtmltopdf.org/downloads.html")
else:
    import pdfkit
    pdfkit.from_string(informe_html, "informe_srg.pdf")
    st.success("PDF generado correctamente: informe_srg.pdf")
# ============================================
# BLOQUE 8 — SIMULACIONES AVANZADAS SRG
# ============================================

st.markdown('<div class="srg-title">Simulaciones avanzadas SRG</div>', unsafe_allow_html=True)
st.caption("Comparativa entre la evolución recomendada y la aportación elegida por el cliente.")

# ============================
# TABLA DE EVOLUCIÓN MENSUAL Y ANUAL
# ============================

html_tabla_recom = tabla_mensual_y_anual_html(evolucion_recom, anos_hasta_jub)
html_tabla_cliente = tabla_mensual_y_anual_html(evolucion_cliente, anos_hasta_jub)

col_tab1, col_tab2 = st.columns(2)

with col_tab1:
    st.markdown("### Evolución recomendada")
    st.markdown(
        f"""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <table style="width:100%;border-collapse:collapse;">
        <thead>
            <tr style="background:#003366;color:#ffffff;">
                <th>Periodo</th><th>Aportado</th><th>Total</th><th>Inflación</th><th>Neto</th>
            </tr>
        </thead>
        <tbody>
            {html_tabla_recom}
        </tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_tab2:
    st.markdown("### Evolución con cuota del cliente")
    st.markdown(
        f"""
        <div style="background:#0A1A2F;color:#EAF2FF;padding:12px;border-left:4px solid #00BFFF;border-radius:6px;">
        <table style="width:100%;border-collapse:collapse;">
        <thead>
            <tr style="background:#003366;color:#ffffff;">
                <th>Periodo</th><th>Aportado</th><th>Total</th><th>Inflación</th><th>Neto</th>
            </tr>
        </thead>
        <tbody>
            {html_tabla_cliente}
        </tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================
# COMPARATIVA FINAL
# ============================

st.markdown('<div class="srg-title">Comparativa final SRG</div>', unsafe_allow_html=True)
st.caption("Resumen de resultados entre la aportación recomendada y la cuota elegida por el cliente.")

col_comp1, col_comp2, col_comp3 = st.columns(3)

with col_comp1:
    st.metric("Aportación recomendada", f"{aportacion_recom:,.0f} €")
    st.metric("Capital neto recomendado", f"{capital_real_final_recom:,.0f} €")

with col_comp2:
    st.metric("Aportación cliente", f"{cuota_confirm_input:,.0f} €")
    st.metric("Capital neto cliente", f"{capital_real_final_cliente:,.0f} €")

with col_comp3:
    diferencia_capital = capital_real_final_cliente - capital_real_final_recom
    diferencia_pct = (diferencia_capital / capital_real_final_recom * 100) if capital_real_final_recom > 0 else 0.0
    st.metric("Diferencia de capital", f"{diferencia_capital:,.0f} €", f"{diferencia_pct:,.1f}%")

# ============================
# EXPLICACIÓN SRG OSCURA
# ============================

with st.expander("📘 Explicación de las simulaciones avanzadas"):
    st.markdown(f"""
    <div style="background:#0A1A2F;color:#EAF2FF;padding:16px;border-left:4px solid #00BFFF;border-radius:6px;">
    Las <b>simulaciones avanzadas SRG</b> comparan dos escenarios:<br><br>
    - <b>Escenario recomendado:</b> cuota óptima calculada para cubrir la brecha mensual de <b>{brecha:,.0f} €</b>.<br>
    - <b>Escenario cliente:</b> cuota real que el cliente decide aportar.<br><br>
    La diferencia de capital final muestra el impacto de ajustar la cuota.  
    Si el capital del cliente es menor, puede compensarse aumentando la rentabilidad o la duración del plan.<br><br>
    Estas simulaciones permiten visualizar el efecto de cada decisión en el horizonte de jubilación.
    </div>
    """, unsafe_allow_html=True)

# ============================
# FOOTER SRG
# ============================

st.markdown("""
<div class="srg-footer">
Simulador SRG © 2026 — Desarrollado por Samuel Ruiz González · Versión Premium SRG
</div>
""", unsafe_allow_html=True)
# ============================================
# BLOQUE 9 — GRÁFICAS COMPARATIVAS SRG FINALES
# ============================================

st.markdown('<div class="srg-title">Gráficas comparativas SRG</div>', unsafe_allow_html=True)
st.caption("Visualización final de los escenarios recomendados y personalizados del cliente.")

# ============================
# GRÁFICA 1 — CAPITAL FINAL (RECOMENDADO VS CLIENTE)
# ============================

fig_comp = go.Figure()

fig_comp.add_trace(go.Bar(
    name="Capital neto recomendado",
    x=["Recomendado"],
    y=[capital_real_final_recom],
    marker_color="#00BFFF"
))

fig_comp.add_trace(go.Bar(
    name="Capital neto cliente",
    x=["Cliente"],
    y=[capital_real_final_cliente],
    marker_color="#FF00AA"
))

fig_comp.update_layout(
    barmode='group',
    height=420,
    plot_bgcolor='#0A0F1F',
    paper_bgcolor='#0A0F1F',
    font=dict(color="#EAF2FF"),
    title=dict(
        text="<b>Comparativa de capital final</b>",
        x=0.5,
        font=dict(color="#EAF2FF", size=18)
    ),
    xaxis=dict(title="Escenario"),
    yaxis=dict(title="Capital neto (€)")
)

st.plotly_chart(fig_comp, use_container_width=True)

# ============================
# GRÁFICA 2 — BRECHA CUBIERTA VS NO CUBIERTA
# ============================

brecha_cubierta_recom = min(capital_real_final_recom / (anos_jubilacion * 12), brecha)
brecha_cubierta_cliente = min(capital_real_final_cliente / (anos_jubilacion * 12), brecha)

brecha_no_cubierta_recom = brecha - brecha_cubierta_recom
brecha_no_cubierta_cliente = brecha - brecha_cubierta_cliente

fig_brecha = go.Figure()

fig_brecha.add_trace(go.Bar(
    name="Brecha cubierta (Recomendado)",
    x=["Recomendado"],
    y=[brecha_cubierta_recom],
    marker_color="#00FFAA"
))

fig_brecha.add_trace(go.Bar(
    name="Brecha cubierta (Cliente)",
    x=["Cliente"],
    y=[brecha_cubierta_cliente],
    marker_color="#FFD700"
))

fig_brecha.add_trace(go.Bar(
    name="Brecha no cubierta (Recomendado)",
    x=["Recomendado"],
    y=[brecha_no_cubierta_recom],
    marker_color="#003366"
))

fig_brecha.add_trace(go.Bar(
    name="Brecha no cubierta (Cliente)",
    x=["Cliente"],
    y=[brecha_no_cubierta_cliente],
    marker_color="#660022"
))

fig_brecha.update_layout(
    barmode='stack',
    height=420,
    plot_bgcolor='#0A0F1F',
    paper_bgcolor='#0A0F1F',
    font=dict(color="#EAF2FF"),
    title=dict(
        text="<b>Brecha cubierta vs brecha no cubierta</b>",
        x=0.5,
        font=dict(color="#EAF2FF", size=18)
    ),
    xaxis=dict(title="Escenario"),
    yaxis=dict(title="€/mes")
)

st.plotly_chart(fig_brecha, use_container_width=True)

# ============================
# EXPLICACIÓN FINAL SRG
# ============================

with st.expander("📘 Interpretación final SRG"):
    st.markdown(f"""
    <div style="background:#0A1A2F;color:#EAF2FF;padding:18px;border-left:4px solid #00BFFF;border-radius:6px;">
    Las gráficas finales SRG permiten visualizar de forma clara:<br><br>

    <b>1. Capital final acumulado</b><br>
    - La cuota recomendada genera un capital neto de <b>{capital_real_final_recom:,.0f} €</b>.<br>
    - La cuota del cliente genera un capital neto de <b>{capital_real_final_cliente:,.0f} €</b>.<br><br>

    <b>2. Brecha cubierta</b><br>
    - Con la cuota recomendada se cubre <b>{brecha_cubierta_recom:,.0f} €/mes</b> de la brecha.<br>
    - Con la cuota del cliente se cubre <b>{brecha_cubierta_cliente:,.0f} €/mes</b>.<br><br>

    <b>3. Brecha no cubierta</b><br>
    - Recomendado: <b>{brecha_no_cubierta_recom:,.0f} €/mes</b>.<br>
    - Cliente: <b>{brecha_no_cubierta_cliente:,.0f} €/mes</b>.<br><br>

    Estas gráficas permiten tomar decisiones informadas sobre la cuota ideal, la rentabilidad necesaria
    y el horizonte temporal para asegurar un nivel de vida óptimo en la jubilación.
    </div>
    """, unsafe_allow_html=True)

# ============================
# CIERRE DEL SIMULADOR SRG
# ============================

st.markdown("""
<div class="srg-footer">
Simulador SRG © 2026 — Informe, simulaciones y gráficas generadas con precisión profesional.
</div>
""", unsafe_allow_html=True)

