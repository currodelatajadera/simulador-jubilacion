# ============================================
#   BLOQUE 1 — IMPORTS, CSS, FUNCIONES BASE
# ============================================

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
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
#   CSS GLOBAL PREMIUM SRG
# ============================================

st.markdown("""
<style>
@import url('https://://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&display=swap');

body, html {
    font-family: 'Montserrat', sans-serif;
}

/* HEADER SRG */
.srg-header {
    padding: 14px 24px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #003366, #0055A4);
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
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

/* CAJAS */
.srg-box {
    background: linear-gradient(180deg, #ffffff, #f2f6fb);
    padding: 14px;
    border-radius: 6px;
    border: 1px solid #c7d4e5;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* FOOTER */
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

/* MÉTRICAS */
[data-testid="stMetricValue"] {
    font-size: 1.1rem;
}

/* BOTÓN EXPLICACIÓN */
#btn_explicacion button {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: #ffffff !important;
    border: 1px solid #c7d4e5;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 600;
    font-size: 0.9rem;
}
#btn_explicacion button:hover {
    background: linear-gradient(135deg, #0055A4, #0070CC);
}
</style>
""", unsafe_allow_html=True)

# ============================================
#   ESTILOS PERSONALIZADOS SRG  (AÑADIDOS)
# ============================================

st.markdown("""
<style>

/* Título pequeño y coherente con la tipografía general */
h5 {
    font-family: 'Inter', 'Montserrat', sans-serif;
    font-weight: 600;
    font-size: 1.05rem;
    color: #2E2E2E;
    margin-top: 0.8rem;
    margin-bottom: 0.6rem;
}

/* Caja de resultado verde suave */
div[data-testid="stSuccess"] {
    background-color: #E9F6EC !important;
    border-radius: 8px;
    padding: 10px 14px;
    font-weight: 600;
    color: #2E7D32;
}

/* Ajuste visual para inputs */
div[data-testid="stNumberInput"] label {
    font-weight: 500;
    color: #3A3A3A;
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
#   FUNCIONES UNIFICADAS
# ============================================

def calcular_objetivo_y_gastos_futuros(ingresos_hoy, gastos_hoy, pct, inflacion, anos):
    factor = (1 + inflacion/100) ** anos
    return ingresos_hoy * factor, gastos_hoy * (pct/100) * factor

def calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, aportacion):
    meses = anos_hasta_jub * 12
    r_mensual = rentabilidad / 12
    infl_mensual = inflacion / 12

    capital = 0
    lista = []

    for mes in range(meses + 1):
        if mes > 0:
            capital = capital * (1 + r_mensual) + aportacion

        capital_aportado = aportacion * mes
        capital_real = capital / ((1 + infl_mensual) ** mes)
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
    filas = ""
    max_mes = min(12, len(evolucion) - 1)

    for mes in range(1, max_mes + 1):
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

    for ano in range(2, anos_hasta_jub + 1):
        idx = ano * 12
        if idx < len(evolucion):
            fila = evolucion[idx]
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
#   BLOQUE 2 — PENSIÓN, OBJETIVO, BRECHA
# ============================================

# ============================
#   FILA 1 — DATOS PRINCIPALES
# ============================

col1, col2, col3, col4 = st.columns(4)

# ---------------------------
#   DATOS PERSONALES
# ---------------------------
with col1:
    st.markdown('<div class="srg-title">Datos personales</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Información básica necesaria para calcular tu horizonte de jubilación.")

    edad_actual = st.number_input(
        "Edad actual",
        18, 70, 47,
        help="Tu edad hoy. Se usa para calcular cuántos años faltan hasta la jubilación."
    )

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
        60, 75, 67,
        help="Edad a la que deseas jubilarte. La edad mínima depende de la modalidad elegida."
    )

    esperanza_vida = st.number_input(
        "Esperanza de vida",
        75, 100, 85,
        help="Estimación de años que vivirás según estadísticas. Afecta a los años que estarás jubilado."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# Correcciones automáticas
if edad_prevista_jub <= edad_actual:
    edad_prevista_jub = edad_actual + 1
if esperanza_vida <= edad_prevista_jub:
    esperanza_vida = edad_prevista_jub + 1

# ---------------------------
# ---------------------------
#   COTIZACIÓN
# ---------------------------
with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Tus años cotizados determinan si puedes acceder a modalidades anticipadas.")

    # Máximo lógico: no puedes haber cotizado más años de los que has podido trabajar
    max_cotizables_hoy = max(0, edad_actual - 16)

    anos_cotizados_hoy = st.number_input(
        "Años cotizados hoy",
        min_value=0,
        max_value=max_cotizables_hoy,
        value=min(15, max_cotizables_hoy),
        help="Años cotizados a la Seguridad Social. No incluye lagunas ni convenios especiales."
    )

    # Máximo lógico: no puedes cotizar más años futuros de los que hay hasta la jubilación
    max_anos_futuros = max(0, edad_prevista_jub - edad_actual)

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
        min_value=0,
        max_value=max_anos_futuros,
        value=min(20, max_anos_futuros),
        help="Años adicionales que seguirás cotizando hasta la edad prevista de jubilación."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# Derivados coherentes
anos_totales = anos_cotizados_hoy + anos_futuros
anos_hasta_jub = max(1, edad_prevista_jub - edad_actual)
anos_jubilacion = max(1, esperanza_vida - edad_prevista_jub)



# ---------------------------
#   TIPO DE JUBILACIÓN (INTELIGENTE)
# ---------------------------
with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Selecciona la modalidad. Te mostraremos requisitos y límites automáticamente.")

    tipo_jubilacion = st.selectbox(
        "Tipo prevista",
        ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"],
        help="""
**Ordinaria:** edad legal sin anticipos.
**Anticipada voluntaria:** hasta 24 meses antes, requiere 35 años cotizados.
**Anticipada involuntaria:** hasta 48 meses antes, requiere 33 años cotizados.
**Demorada:** retrasar la jubilación, genera bonificaciones.
"""
    )

    # Explicación dinámica según modalidad
    if tipo_jubilacion == "Ordinaria":
        st.info("La jubilación ordinaria no permite anticipos. Solo puedes jubilarte a la edad legal.")
        meses_anticipo = st.number_input("Meses anticipo (+) / demora (-)", 0, 0, 0)

    elif tipo_jubilacion == "Anticipada voluntaria":
        st.info("Requiere **35 años cotizados** y permite anticipar entre **1 y 24 meses**.")
        meses_anticipo = st.number_input("Meses de anticipo", 1, 24, 1)

    elif tipo_jubilacion == "Anticipada involuntaria":
        st.info("Requiere **33 años cotizados** y permite anticipar entre **1 y 48 meses**.")
        meses_anticipo = st.number_input("Meses de anticipo", 1, 48, 48)

    elif tipo_jubilacion == "Demorada":
        st.info("Retrasar la jubilación genera bonificaciones. Introduce meses negativos.")
        meses_anticipo = st.number_input("Meses de demora (negativos)", -120, -1, -1)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
#   INGRESOS Y GASTOS
# ---------------------------
with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Tus ingresos y gastos actuales nos permiten estimar tu objetivo económico futuro.")

    ingresos = st.number_input(
        "Ingresos mensuales (€)",
        min_value=0,
        max_value=20000,
        value=2500,
        help="Tus ingresos netos actuales."
    )

    # El valor por defecto de gastos nunca puede ser mayor que los ingresos actuales
    valor_defecto_gastos = min(1800, ingresos)

    gastos = st.number_input(
        "Gastos mensuales (€)",
        min_value=0,
        max_value=20000,
        value=valor_defecto_gastos,
        help="Tus gastos mensuales actuales."
    )

    # Corrección lógica: si los gastos superan los ingresos, ajustamos y avisamos
    if gastos > ingresos:
        st.warning("Has indicado más gastos que ingresos. Ajustamos los gastos al máximo igual a tus ingresos.")
        gastos = ingresos

    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
#   VALIDACIONES LEGALES 2026
# ---------------------------

anos_totales = anos_cotizados_hoy + anos_futuros
anos_hasta_jub = max(1, edad_prevista_jub - edad_actual)
anos_jubilacion = max(1, esperanza_vida - edad_prevista_jub)

modo_valido = True
motivo_error = ""

if tipo_jubilacion == "Ordinaria":
    if meses_anticipo != 0:
        modo_valido = False
        motivo_error = "La jubilación ordinaria no permite anticipos."

elif tipo_jubilacion == "Anticipada voluntaria":
    if anos_totales < 35:
        modo_valido = False
        motivo_error = "La anticipada voluntaria requiere al menos 35 años cotizados."

elif tipo_jubilacion == "Anticipada involuntaria":
    if anos_totales < 33:
        modo_valido = False
        motivo_error = "La anticipada involuntaria requiere al menos 33 años cotizados."

elif tipo_jubilacion == "Demorada":
    if meses_anticipo >= 0:
        modo_valido = False
        motivo_error = "La jubilación demorada solo permite meses negativos."

# Coeficiente
coef_ajuste = 1.0
if modo_valido:
    if "Anticipada" in tipo_jubilacion:
        coef_ajuste -= 0.005 * meses_anticipo
    elif tipo_jubilacion == "Demorada":
        coef_ajuste -= 0.004 * meses_anticipo
coef_ajuste = max(0, coef_ajuste)

# ---------------------------
#   EXPLICACIÓN DETALLADA
# ---------------------------
st.markdown('<div class="srg-title">Explicación detallada</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

if modo_valido:
    st.success("La modalidad seleccionada es válida.")
else:
    st.error(f"La modalidad seleccionada NO es válida. Motivo: {motivo_error}")

if st.button("Ver explicación" if not st.session_state.mostrar_explicacion else "Ocultar explicación"):
    st.session_state.mostrar_explicacion = not st.session_state.mostrar_explicacion

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.mostrar_explicacion:
    with st.expander("Explicación detallada", expanded=True):
        st.write(f"**Modalidad:** {tipo_jubilacion}")
        st.write(f"**Años cotizados hoy:** {anos_cotizados_hoy}")
        st.write(f"**Años futuros:** {anos_futuros}")
        st.write(f"**Total cotizados:** {anos_totales}")
        st.write(f"**Meses anticipo/demora:** {meses_anticipo}")
        st.write(f"**Coeficiente aplicado:** {coef_ajuste:.3f}")

# ============================================
#   PENSIÓN E INFLACIÓN  (COLUMNA SIGUIENTE)
# ============================================

PENSION_MAX_2026 = 3359.60
EXTRA_REVAL = 0.00115
BASE_MAX_ESPANA_2026 = 4720

colA, colB, colC, colD = st.columns(4)

# ---------------------------
# ---------------------------
#   PENSIÓN E INFLACIÓN
# ---------------------------
with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Estos valores determinan tu pensión futura ajustada a la inflación.")

    # ---------------------------------------
    #   BASE REGULADORA — MODO MANUAL / SRG
    # ---------------------------------------
    modo_br = st.radio(
        "Modo de cálculo de Base Reguladora",
        ["Introducir base reguladora manualmente", "Calcular base reguladora SRG"],
        help="La Base Reguladora se calcula con las bases de cotización de los últimos 29 años (348 meses), actualizadas por IPC y eliminando los 24 peores meses."
    )

    if modo_br == "Introducir base reguladora manualmente":
        base = st.number_input(
            "Base reguladora (€)",
            min_value=0,
            max_value=BASE_MAX_ESPANA_2026,
            value=1500,
            help="Introduce directamente tu base reguladora estimada. La Seguridad Social aplica un límite máximo de cotización anual."
        )

    else:
        st.markdown("#### Calcular base reguladora SRG")
        # Línea informativa bajo el título
        st.caption(
    "Los cálculos respetan los límites legales de cotización y pensión establecidos por la Seguridad Social. "
    "Si tu base o pensión supera el máximo permitido, el sistema la ajusta automáticamente según la normativa vigente."
    )

        

        salario_actual = st.number_input(
            "Salario mensual actual (€)",
            min_value=0,
            max_value=20000,
            value=2000,
            help="Salario bruto mensual aproximado."
        )

        crecimiento_salarial = st.number_input(
            "Crecimiento salarial anual (%)",
            min_value=0.0,
            max_value=10.0,
            value=1.5,
            step=0.1,
            help="Incremento medio anual de tu salario."
        )

        ipc_actualizacion = st.number_input(
            "Actualización IPC anual (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            help="Factor de actualización de bases antiguas."
        )

        anos_con_salario = st.number_input(
            "Años cotizados con salario conocido",
            min_value=1,
            max_value=29,
            value=10,
            help="Años recientes con salario aproximado."
        )
        

        # ---------------------------------------
        #   CÁLCULO REAL DE BASE REGULADORA SRG
        # ---------------------------------------
        meses_totales = 29 * 12  # 348 meses

        bases = []
        for i in range(meses_totales):
            anos_pasados = (meses_totales - 1 - i) / 12
            salario_estimado = salario_actual / ((1 + crecimiento_salarial/100) ** anos_pasados)
            bases.append(salario_estimado)

        # Actualizar por IPC
        bases_actualizadas = []
        for i, base_i in enumerate(bases):
            anos_pasados = (meses_totales - 1 - i) / 12
            factor_ipc = (1 + ipc_actualizacion/100) ** anos_pasados
            bases_actualizadas.append(base_i * factor_ipc)

        # Ordenar y eliminar los 24 peores meses
        bases_ordenadas = sorted(bases_actualizadas)
        mejores_322 = bases_ordenadas[24:]

        # Base reguladora final
        base = sum(mejores_322) / 322

        # Aplicar límite legal de cotización
        if base > BASE_MAX_ESPANA_2026:
            base = BASE_MAX_ESPANA_2026
            st.warning(f"La base reguladora supera el límite legal de cotización ({BASE_MAX_ESPANA_2026:,.0f} €). Se ha ajustado automáticamente.")

        st.success(f"Base reguladora calculada: **{base:,.0f} €**")

    # ---------------------------------------
    #   INFLACIÓN Y REVALORIZACIÓN
    # ---------------------------------------
    inflacion = st.number_input(
        "Inflación anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="La inflación reduce el poder adquisitivo. Se usa para proyectar valores futuros."
    )

    reval = st.number_input(
        "Revalorización anual pensión (%)",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Incremento anual previsto de la pensión según normativa."
    )

    st.info("En España existe una base máxima de cotización. Aunque ganes más, solo se computa hasta ese límite.")

    st.markdown('</div>', unsafe_allow_html=True)

# Función necesaria
def pension_maxima_proyectada(anos, inflacion):
    return PENSION_MAX_2026 * ((1 + inflacion/100 + EXTRA_REVAL) ** anos)

# ============================================
#   CÁLCULO DE PENSIÓN
# ============================================

if modo_valido:
    pct = min(1.0, anos_totales / 37)
else:
    pct = 0.0

pension_hoy = base * pct * coef_ajuste
pension_futura_sin_tope = pension_hoy * ((1 + reval/100) ** anos_hasta_jub)
pension_max_futura = pension_maxima_proyectada(anos_hasta_jub, inflacion)
pension_futura = min(pension_futura_sin_tope, pension_max_futura)

# ---------------------------
#   RESUMEN PENSIÓN
# ---------------------------
with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Tu pensión estimada según tus años cotizados y tu base reguladora.")

    st.metric("Porcentaje sobre base", f"{pct*100:,.1f} %")
    st.caption("Este porcentaje representa cuánto de tu base reguladora te corresponde según tus años cotizados.")

    st.metric("Pensión ajustada hoy", f"{pension_hoy:,.0f} €")
    st.caption("Pensión que te correspondería hoy, antes de aplicar revalorizaciones futuras.")

    st.metric("Pensión futura estimada", f"{pension_futura:,.0f} €/mes")
    st.caption("Pensión proyectada a tu edad de jubilación, aplicando revalorización anual.")

    # ---------------------------------------
    #   AVISO DE LÍMITE LEGAL DE PENSIÓN
    # ---------------------------------------
    if pension_futura == pension_max_futura:
        st.warning(
            f"La pensión futura calculada supera el límite legal permitido. "
            f"Se ha aplicado el tope máximo proyectado de {pension_max_futura:,.0f} €/mes según la normativa vigente."
        )
        st.caption("La pensión pública tiene un límite legal. Si tu cálculo lo supera, se aplica automáticamente el máximo permitido por ley.")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
#   OBJETIVO ECONÓMICO
# ============================================

with colC:
    st.markdown('<div class="srg-title">Objetivo económico</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Define el nivel de vida que deseas mantener en tu jubilación.")

    objetivo_hoy = st.number_input(
        "Ingresos deseados hoy (€)",
        0, 20000, 2000,
        help="Cantidad mensual que te gustaría mantener en jubilación, expresada en euros actuales."
    )

    pct_mantener = st.number_input(
        "Gastos que mantendrás en jubilación (%)",
        50, 120, 90,
        help="Porcentaje de tus gastos actuales que esperas mantener cuando te jubiles."
    )

    st.markdown('</div>', unsafe_allow_html=True)

objetivo_futuro, gastos_futuros = calcular_objetivo_y_gastos_futuros(
    objetivo_hoy, gastos, pct_mantener, inflacion, anos_hasta_jub
)

with colC:
    st.metric("Objetivo mensual futuro", f"{objetivo_futuro:,.0f} €")
    st.caption("Tu objetivo económico ajustado a la inflación futura.")

    st.metric("Gastos futuros estimados", f"{gastos_futuros:,.0f} €")
    st.caption("Proyección de tus gastos actuales ajustados a la inflación.")

# ============================================
#   BRECHA
# ============================================

with colD:
    st.markdown('<div class="srg-title">Brecha</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.caption("Diferencia entre tu pensión futura y el nivel de vida que deseas mantener.")

    modo_brecha = st.radio(
        "¿Qué quieres cubrir?",
        ["Objetivo económico", "Gastos reales"],
        horizontal=True,
        help="Elige si quieres cubrir tu objetivo deseado o tus gastos reales proyectados."
    )

    if modo_brecha == "Objetivo económico":
        brecha = objetivo_futuro - pension_futura
    else:
        brecha = gastos_futuros - pension_futura

    st.metric("Brecha mensual a cubrir", f"{brecha:,.0f} €")

    with st.expander("¿Qué significa esta brecha?"):
        st.write("""
- **Objetivo económico:** diferencia entre tu pensión futura y los ingresos que deseas mantener.
- **Gastos reales:** diferencia entre tu pensión futura y tus gastos estimados.

La brecha es la **cantidad mensual** que debes generar con ahorro e inversión para mantener tu nivel de vida.
        """)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
#   PLAN DE AHORRO + GRÁFICA A LA DERECHA
# ============================================

st.markdown('<div class="srg-title">Plan de ahorro recomendado</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

col_left, col_right = st.columns([0.55, 0.45])  # <-- GRÁFICA A LA DERECHA

with col_left:

    rentabilidad_pct = st.number_input(
        "Rentabilidad anual esperada (%)",
        0.0, 15.0, 4.0, 0.1
    )
    rentabilidad = rentabilidad_pct / 100

    capital_necesario = max(0, brecha * 12 * anos_jubilacion)

    if capital_necesario > 0 and rentabilidad > 0:
        r_m = rentabilidad / 12
        n_meses = anos_hasta_jub * 12
        aportacion_recom = capital_necesario * r_m / ((1 + r_m)**n_meses - 1)
    else:
        aportacion_recom = 0

    evolucion_recom = calcular_evolucion_mensual(
        anos_hasta_jub, rentabilidad, inflacion, aportacion_recom
    )

    capital_total_recom = evolucion_recom[-1]["total"]
    capital_real_final_recom = evolucion_recom[-1]["neta"]

    st.metric("Capital necesario", f"{capital_necesario:,.0f} €")
    st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €")
    st.metric("Capital total recomendado", f"{capital_total_recom:,.0f} €")
    st.metric("Capital neto recomendado", f"{capital_real_final_recom:,.0f} €")


with col_right:

    evo_sin0 = evolucion_recom[1:]
    anos_evo = [fila["mes"]/12 for fila in evo_sin0]
    total_evo = [fila["total"] for fila in evo_sin0]
    aportada_evo = [fila["aportada"] for fila in evo_sin0]
    neta_evo = [fila["neta"] for fila in evo_sin0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=anos_evo, y=total_evo,
        mode='lines',
        name='Total',
        line=dict(color='#003366', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=anos_evo, y=aportada_evo,
        mode='lines',
        name='Aportado',
        line=dict(color='#66A3FF', width=2, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=anos_evo, y=neta_evo,
        mode='lines',
        name='Neto',
        line=dict(color='#009966', width=2)
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Años",
        yaxis_title="Capital (€)"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
#   MODO EXPERTO SRG
# ============================================

st.markdown('<div class="srg-title">Modo Experto SRG</div>', unsafe_allow_html=True)
with st.expander("Mostrar detalles avanzados de cálculo"):

    st.write("### 🔍 Cálculos internos de la pensión")
    st.write(f"- Base reguladora: {base:,.0f} €")
    st.write(f"- % sobre base: {pct*100:.2f} %")
    st.write(f"- Coeficiente: {coef_ajuste:.3f}")
    st.write(f"- Pensión hoy: {pension_hoy:,.0f} €")
    st.write(f"- Pensión futura sin tope: {pension_futura_sin_tope:,.0f} €")
    st.write(f"- Tope legal proyectado: {pension_max_futura:,.0f} €")
    st.write(f"- Pensión futura final: {pension_futura:,.0f} €")

    st.write("---")
    st.write("### 📈 Fórmulas utilizadas")
    st.code("""
Pensión hoy = Base × % × coeficiente
Pensión futura sin tope = Pensión hoy × (1 + reval) ^ años
Pensión futura final = min(Pensión futura sin tope, Tope legal)
Tope legal = Pensión máxima 2026 × (1 + inflación + extra_reval) ^ años
    """)

    st.write("---")
    st.write("### 🧮 Cálculo del plan recomendado")
    st.write(f"- Brecha mensual: {brecha:,.0f} €")
    st.write(f"- Años en jubilación: {anos_jubilacion}")
    st.write(f"- Capital necesario: {capital_necesario:,.0f} €")
    st.write(f"- Rentabilidad anual: {rentabilidad*100:.2f} %")
    st.write(f"- Rentabilidad mensual: {(rentabilidad/12)*100:.4f} %")

    st.code("""
Cuota recomendada =
    Capital necesario × r_mensual
    -----------------------------------------
    (1 + r_mensual)^(meses hasta jub) - 1
    """)

    st.success("Modo Experto activado.")
# ============================================
#   BLOQUE 3 — SIMULACIONES DE AHORRO
# ============================================

st.markdown('<div class="srg-title">Simulaciones de ahorro</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Cuota recomendada", "Simular mi cuota", "Comparativa de cuotas"])

cuota_cliente = 0.0
capital_total_cliente = 0.0
porc_cobertura_cliente = 0.0
brecha_restante_cliente = brecha
comparativa_cuotas = []
evolucion_cliente = None

# ============================================
#   TAB 1 — ESCENARIO RECOMENDADO
# ============================================

with tab1:
    st.markdown("### Escenario recomendado")
    st.write(
        "Este escenario utiliza la aportación mensual recomendada para cubrir la brecha "
        "calculada en función de tus datos y de la rentabilidad asumida."
    )
    st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €/mes")
    st.metric("Capital total al jubilarte", f"{capital_total_recom:,.0f} €")
    st.metric("Capital neto (ajustado por inflación)", f"{capital_real_final_recom:,.0f} €")

# ============================================
#   TAB 2 — SIMULAR CUOTA DEL CLIENTE
# ============================================

with tab2:
    st.markdown("### Simular mi cuota")

    cuota_cliente = st.number_input(
        "Cuota mensual que quieres aportar (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(round(aportacion_recom, 0)) if aportacion_recom > 0 else 100.0,
        step=10.0,
        help="Introduce la cuota mensual que deseas aportar."
    )

    if cuota_cliente > 0:
        evolucion_cliente = calcular_evolucion_mensual(
            anos_hasta_jub, rentabilidad, inflacion, cuota_cliente
        )

        capital_total_cliente = evolucion_cliente[-1]["total"]

        if capital_necesario > 0:
            porc_cobertura_cliente = min(capital_total_cliente / capital_necesario, 1.0) * 100
        else:
            porc_cobertura_cliente = 100.0

        brecha_restante_cliente = brecha * (1 - porc_cobertura_cliente / 100.0)

        st.metric("Capital total con tu cuota", f"{capital_total_cliente:,.0f} €")
        st.metric("Cobertura de la brecha", f"{porc_cobertura_cliente:,.1f} %")
        st.metric("Brecha mensual restante", f"{brecha_restante_cliente:,.0f} €")

        st.write("#### Resumen de tu cuota")
        st.table({
            "Concepto": [
                "Cuota mensual elegida",
                "Capital total estimado",
                "Cobertura de la brecha",
                "Brecha mensual restante"
            ],
            "Valor": [
                f"{cuota_cliente:,.0f} €",
                f"{capital_total_cliente:,.0f} €",
                f"{porc_cobertura_cliente:,.1f} %",
                f"{brecha_restante_cliente:,.0f} €"
            ]
        })

        # Gráfica de evolución del cliente
        with st.expander("Detalle de la evolución con tu cuota"):
            evo_cli_sin0 = evolucion_cliente[1:]
            anos_cli = [fila["mes"]/12 for fila in evo_cli_sin0]
            total_cli = [fila["total"] for fila in evo_cli_sin0]
            aportada_cli = [fila["aportada"] for fila in evo_cli_sin0]
            neta_cli = [fila["neta"] for fila in evo_cli_sin0]

            fig_cli = go.Figure()
            fig_cli.add_trace(go.Scatter(
                x=anos_cli, y=total_cli,
                mode='lines',
                name='Total acumulado',
                line=dict(color='#AA0000', width=3)
            ))
            fig_cli.add_trace(go.Scatter(
                x=anos_cli, y=aportada_cli,
                mode='lines',
                name='Aportado',
                line=dict(color='#FF6666', width=2, dash='dash')
            ))
            fig_cli.add_trace(go.Scatter(
                x=anos_cli, y=neta_cli,
                mode='lines',
                name='Neto ajustado inflación',
                line=dict(color='#CC6600', width=2)
            ))

            fig_cli.update_layout(
                height=380,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Años hasta jubilación",
                yaxis_title="Capital (€)"
            )

            st.plotly_chart(fig_cli, use_container_width=True)

    else:
        st.info("Introduce una cuota mensual mayor que 0 para simular tu propio escenario.")

# ============================================
#   TAB 3 — COMPARATIVA DE CUOTAS
# ============================================

with tab3:
    st.markdown("### Comparativa de cuotas")
    st.write(
        "Esta tabla compara distintos niveles de aportación y su impacto en el capital final "
        "y en la cobertura de la brecha."
    )

    cuota_base = st.number_input(
        "Cuota base para la comparativa (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(round(aportacion_recom, 0)),
        step=10.0
    )

    rango = st.number_input(
        "Rango de variación por escenario (€)",
        min_value=10.0,
        max_value=1000.0,
        value=50.0,
        step=10.0
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

        evo = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, c)
        cap_tot = evo[-1]["total"]

        if capital_necesario > 0:
            porc_cov = min(cap_tot / capital_necesario, 1.0) * 100
        else:
            porc_cov = 100.0

        brecha_rest = brecha * (1 - porc_cov / 100.0)

        comparativa_cuotas.append({
            "cuota": c,
            "capital": cap_tot,
            "porc_cobertura": porc_cov,
            "brecha_restante": brecha_rest
        })

    if comparativa_cuotas:
        st.write("#### Tabla comparativa de escenarios")
        st.table({
            "Cuota mensual (€)": [f"{x['cuota']:,.0f}" for x in comparativa_cuotas],
            "Capital final (€)": [f"{x['capital']:,.0f}" for x in comparativa_cuotas],
            "Cobertura brecha (%)": [f"{x['porc_cobertura']:,.1f}" for x in comparativa_cuotas],
            "Brecha restante (€)": [f"{x['brecha_restante']:,.0f}" for x in comparativa_cuotas],
        })

        mejor = max(comparativa_cuotas, key=lambda x: x["porc_cobertura"])

        st.markdown("#### Resumen automático")
        st.markdown(
            f"- Con una cuota de **{mejor['cuota']:,.0f} €/mes** cubrirías aproximadamente "
            f"**{mejor['porc_cobertura']:,.1f}%** de la brecha.\n"
            f"- La brecha mensual restante sería de **{mejor['brecha_restante']:,.0f} €**."
        )
    else:
        st.info("Ajusta la cuota base y el rango para generar escenarios válidos.")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
#   MODO AGENTE SRG + INFORMES + DESCARGA
# ============================================

# ============================================
#   CONTEXTO PARA INFORMES
# ============================================

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
    "aportacion_recom": aportacion_recom,
    "rentabilidad": rentabilidad,
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
    "capital_total_recom": capital_total_recom
}

# ============================================
#   INFORME CLIENTE (HTML)
# ============================================

def informe_cliente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Informe Cliente SRG</title>

<style>
    body {{
        font-family: 'Montserrat', sans-serif;
        background-color: #f4f6fb;
        margin: 0;
        padding: 0;
    }}
    .srg-cover {{
        height: 260px;
        background: linear-gradient(135deg, #003366, #0055A4);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px 20px;
    }}
    .srg-container {{
        max-width: 950px;
        margin: 40px auto;
        background: white;
        padding: 32px 40px;
        border-radius: 12px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    }}
    h2 {{
        color: #003366;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
        padding-left: 14px;
        position: relative;
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
    .srg-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 0.86rem;
    }}
    .srg-table th {{
        background-color: #0055A4;
        color: white;
        padding: 7px;
        text-align: left;
    }}
    .srg-table td {{
        border-bottom: 1px solid #e1e6f0;
        padding: 6px 7px;
    }}
    .srg-highlight-box {{
        border: 1px solid #0055A4;
        background: #f9fbff;
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 8px;
    }}
</style>
</head>

<body>

{marca_agua_srg()}

<div class="srg-cover">
    <h1>Informe de Proyección de Jubilación SRG</h1>
    <p>Versión para el cliente</p>
    <p>Cliente: <b>{contexto['nombre_cliente'] or "Cliente SRG"}</b></p>
    <p>Fecha: {fecha}</p>
</div>

<div class="srg-container">

    <h2>1. Resumen ejecutivo</h2>
    <div class="srg-highlight-box">
        <p><b>Pensión futura estimada:</b> {contexto['pension_futura']:,.0f} €/mes</p>
        <p><b>Objetivo mensual futuro:</b> {contexto['objetivo_futuro']:,.0f} €</p>
        <p><b>Brecha mensual:</b> {contexto['brecha']:,.0f} €</p>
        <p><b>Aportación recomendada:</b> {contexto['aportacion_recom']:,.0f} €/mes</p>
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

    <h2>3. Escenario recomendado</h2>
    <div class="srg-highlight-box">
        <p>Con una aportación de <b>{contexto['aportacion_recom']:,.0f} €/mes</b> cubrirías prácticamente el 100% de tu brecha futura.</p>
    </div>

    <h2>4. Escenario con tu propia cuota</h2>
    <div class="srg-highlight-box">
        <p>Tu cuota actual es de <b>{contexto['cuota_cliente']:,.0f} €/mes</b>.</p>
        <p>Capital final: <b>{contexto['capital_total_cliente']:,.0f} €</b></p>
        <p>Cobertura: <b>{contexto['porc_cobertura_cliente']:,.1f}%</b></p>
    </div>

    <h2>5. Comparativa de cuotas</h2>
    <table class="srg-table">
        <tr>
            <th>Cuota</th>
            <th>Capital final</th>
            <th>Cobertura</th>
            <th>Brecha restante</th>
        </tr>
"""

    for esc in contexto["comparativa_cuotas"]:
        html += f"""
        <tr>
            <td>{esc['cuota']:,.0f} €</td>
            <td>{esc['capital']:,.0f} €</td>
            <td>{esc['porc_cobertura']:,.1f}%</td>
            <td>{esc['brecha_restante']:,.0f} €</td>
        </tr>
"""

    html += f"""
    </table>

    <h2>6. Evolución del ahorro</h2>
    <table class="srg-table">
        <tr>
            <th>Mes/Año</th>
            <th>Aportado</th>
            <th>Total</th>
            <th>Inflación</th>
            <th>Neto</th>
        </tr>
        {tabla_mensual_y_anual_html(contexto['evolucion_recom'], contexto['anos_hasta_jub'])}
    </table>

    <h2>7. Gráfica</h2>
    {fig.to_html(include_plotlyjs='cdn', full_html=False)}

</div>

</body>
</html>
"""
    return html
# ============================================
#   INFORME AGENTE (HTML)
# ============================================

def informe_agente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Informe Técnico SRG</title>

<style>
    body {{
        font-family: 'Montserrat', sans-serif;
        background-color: #f4f6fb;
        margin: 0;
        padding: 0;
    }}
    .srg-cover {{
        height: 260px;
        background: linear-gradient(135deg, #003366, #0055A4);
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px 20px;
    }}
    .srg-container {{
        max-width: 950px;
        margin: 40px auto;
        background: white;
        padding: 32px 40px;
        border-radius: 12px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    }}
    h2 {{
        color: #003366;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
        padding-left: 14px;
        position: relative;
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
    .srg-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 0.86rem;
    }}
    .srg-table th {{
        background-color: #0055A4;
        color: white;
        padding: 7px;
        text-align: left;
    }}
    .srg-table td {{
        border-bottom: 1px solid #e1e6f0;
        padding: 6px 7px;
    }}
    .srg-highlight-box {{
        border: 1px solid #0055A4;
        background: #f9fbff;
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 8px;
    }}
</style>
</head>

<body>

{marca_agua_srg()}

<div class="srg-cover">
    <h1>Informe Técnico SRG</h1>
    <p>Uso interno para agentes</p>
    <p>Cliente: <b>{contexto['nombre_cliente'] or "Cliente SRG"}</b></p>
    <p>Fecha: {fecha}</p>
</div>

<div class="srg-container">

    <h2>1. Resumen técnico</h2>
    <div class="srg-highlight-box">
        <p><b>Pensión futura:</b> {contexto['pension_futura']:,.0f} €/mes</p>
        <p><b>Brecha mensual:</b> {contexto['brecha']:,.0f} €</p>
        <p><b>Aportación recomendada:</b> {contexto['aportacion_recom']:,.0f} €/mes</p>
        <p><b>Cuota cliente:</b> {contexto['cuota_cliente']:,.0f} €/mes</p>
        <p><b>Cobertura cliente:</b> {contexto['porc_cobertura_cliente']:,.1f}%</p>
    </div>

    <h2>2. Datos del cliente</h2>
    <table class="srg-table">
        <tr><th>Campo</th><th>Valor</th></tr>
        <tr><td>Nombre</td><td>{contexto['nombre_cliente']}</td></tr>
        <tr><td>Email</td><td>{contexto['email_cliente']}</td></tr>
        <tr><td>Teléfono</td><td>{contexto['telefono_cliente']}</td></tr>
        <tr><td>Edad actual</td><td>{contexto['edad_actual']} años</td></tr>
        <tr><td>Edad prevista de jubilación</td><td>{contexto['edad_prevista_jub']} años</td></tr>
        <tr><td>Años cotizados</td><td>{contexto['anos_cotizados_hoy']} años</td></tr>
        <tr><td>Años futuros</td><td>{contexto['anos_futuros']} años</td></tr>
    </table>

    <h2>3. Parámetros y supuestos</h2>
    <div class="srg-highlight-box">
        <p><b>Tipo de jubilación:</b> {contexto['tipo_jubilacion']}</p>
        <p><b>Coeficiente:</b> {contexto['coef_ajuste']:.3f}</p>
        <p><b>Rentabilidad anual:</b> {contexto['rentabilidad']*100:.1f}%</p>
        <p><b>Inflación anual:</b> {contexto['inflacion']:.1f}%</p>
        <p><b>Años hasta jubilación:</b> {contexto['anos_hasta_jub']}</p>
        <p><b>Años en jubilación:</b> {contexto['anos_jubilacion']}</p>
    </div>

    <h2>4. Escenarios de aportación</h2>
    <table class="srg-table">
        <tr>
            <th>Escenario</th>
            <th>Cuota</th>
            <th>Capital final</th>
            <th>Cobertura</th>
            <th>Brecha restante</th>
        </tr>
        <tr>
            <td>Recomendado</td>
            <td>{contexto['aportacion_recom']:,.0f} €</td>
            <td>{contexto['capital_total_recom']:,.0f} €</td>
            <td>≈ 100%</td>
            <td>≈ 0 €</td>
        </tr>
        <tr>
            <td>Cliente</td>
            <td>{contexto['cuota_cliente']:,.0f} €</td>
            <td>{contexto['capital_total_cliente']:,.0f} €</td>
            <td>{contexto['porc_cobertura_cliente']:,.1f}%</td>
            <td>{contexto['brecha_restante_cliente']:,.0f} €</td>
        </tr>
"""

    for esc in contexto["comparativa_cuotas"]:
        html += f"""
        <tr>
            <td>Comparativa</td>
            <td>{esc['cuota']:,.0f} €</td>
            <td>{esc['capital']:,.0f} €</td>
            <td>{esc['porc_cobertura']:,.1f}%</td>
            <td>{esc['brecha_restante']:,.0f} €</td>
        </tr>
"""

    html += f"""
    </table>

    <h2>5. Evolución del ahorro</h2>
    <table class="srg-table">
        <tr>
            <th>Mes/Año</th>
            <th>Aportado</th>
            <th>Total</th>
            <th>Inflación</th>
            <th>Neto</th>
        </tr>
        {tabla_mensual_y_anual_html(contexto['evolucion_recom'], contexto['anos_hasta_jub'])}
    </table>

    <h2>6. Gráfica</h2>
    {fig.to_html(include_plotlyjs='cdn', full_html=False)}

</div>

</body>
</html>
"""
    return html
# ============================================
#   GENERAR HTML + PANEL 2 COLUMNAS
# ============================================

html_cliente = informe_cliente(contexto_pdf, fig)
html_agente = informe_agente(contexto_pdf, fig)

bytes_cliente = html_cliente.encode("utf-8")
bytes_agente = html_agente.encode("utf-8")

st.markdown('<div class="srg-title">Panel de herramientas SRG</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

col_left, col_right = st.columns([0.55, 0.45])

# ============================================================
#   COLUMNA IZQUIERDA — MODO AGENTE + GENERAR INFORME
# ============================================================
with col_left:

    st.markdown('<div class="srg-title">Modo Agente SRG</div>', unsafe_allow_html=True)


    modo_agente = st.checkbox("Activar Modo Agente SRG", value=False)

    if modo_agente:

        texto_cuota_cliente = ""
        if cuota_cliente > 0:
            texto_cuota_cliente = (
                f"Con la cuota que propones de **{cuota_cliente:,.0f} €/mes**, "
                f"estarías cubriendo aproximadamente el **{porc_cobertura_cliente:,.1f}%** de la brecha, "
                f"quedando una brecha mensual restante de **{brecha_restante_cliente:,.0f} €**.\n\n"
            )

        st.markdown(f"""
**1. Situación actual**  
"Tienes **{anos_cotizados_hoy} años cotizados** y planeas cotizar **{anos_futuros} años más**, con una jubilación a los **{edad_prevista_jub} años**."

**2. Pensión pública estimada**  
"Con la modalidad **{tipo_jubilacion}**, tu pensión futura estimada sería de **{pension_futura:,.0f} €/mes**."

**3. Objetivo y brecha**  
"Tu objetivo mensual futuro es de **{objetivo_futuro:,.0f} €**, y tus gastos futuros se estiman en **{gastos_futuros:,.0f} €**.  
La brecha a cubrir es de **{brecha:,.0f} €/mes**."

**4. Plan recomendado**  
"Para cubrir esta brecha, necesitas acumular **{capital_necesario:,.0f} €**, con una aportación mensual recomendada de **{aportacion_recom:,.0f} €/mes**."

**5. Escenario del cliente**  
{texto_cuota_cliente if texto_cuota_cliente else "Si el cliente propone una cuota distinta, podemos comparar su impacto."}

**6. Comparativa**  
"Hemos analizado distintos niveles de aportación para que puedas ver cómo cambia la cobertura según la cuota mensual."

**7. Cierre**  
"Podemos diseñar juntos la estrategia de ahorro e inversión que mejor se adapte a tu perfil."
        """)



    # -------------------------
    #   GENERAR INFORMES
    # -------------------------
    st.markdown('<div class="srg-title">Generar informes</div>', unsafe_allow_html=True)


    with st.expander("Datos del cliente"):
        contexto_pdf["nombre_cliente"] = st.text_input("Nombre del cliente")
        contexto_pdf["email_cliente"] = st.text_input("Email del cliente")
        contexto_pdf["telefono_cliente"] = st.text_input("Teléfono del cliente")


# ============================================================
#   COLUMNA DERECHA — VISTA PREVIA Y DESCARGA
# ============================================================
with col_right:

    st.markdown('<div class="srg-title">Vista previa y descarga</div>', unsafe_allow_html=True)


    # Vista previa Cliente
    with st.expander("Vista previa informe Cliente"):
        components.html(html_cliente, height=350, scrolling=True)

    st.download_button(
        label="Descargar Informe Cliente (HTML)",
        data=bytes_cliente,
        file_name="informe_cliente_srg.html",
        mime="text/html"
    )


    # Vista previa Agente
    with st.expander("Vista previa informe Agente"):
        components.html(html_agente, height=350, scrolling=True)

    st.download_button(
        label="Descargar Informe Agente (HTML)",
        data=bytes_agente,
        file_name="informe_agente_srg.html",
        mime="text/html"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
#   FOOTER SRG — FINAL
# ============================================

footer_html = """
<div class="srg-footer">
    Simulador SRG — Samuel Ruiz González<br>
    Herramienta educativa y formativa para Agentes.<br>
    © 2025 Samuel Ruiz González · Política de privacidad · Aviso legal
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

