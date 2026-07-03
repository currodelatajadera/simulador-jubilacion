
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Simulador de Jubilación SRG", page_icon="💼", layout="wide")

# ============================
#   CSS GLOBAL PREMIUM SRG
# ============================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&display=swap');

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

.srg-header-inner {
    max-width: 980px;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    text-align: center;
}

/* TÍTULO PRINCIPAL — tipografía intacta */
.srg-header-title-main {
    font-family: 'Dancing Script', cursive !important;
    font-size: 3.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1.1;
}

/* SUBTÍTULO — tipografía intacta */
.srg-header-title-sub {
    font-family: 'Dancing Script', cursive !important;
    font-size: 1.8rem;
    font-weight: 400;
    color: #d0d8e8;
    margin-top: 6px;
}

/* TITULOS DE SECCIÓN — ahora con degradado suave */
.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

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

</style>
""", unsafe_allow_html=True)

# ============================
#   HEADER SIN LOGO
# ============================

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
    lista = []

    for mes in range(meses + 1):
        if mes > 0:
            capital = capital * (1 + r_mensual) + aportacion

        capital_aportado = aportacion * mes
        capital_real = capital / ((1 + inflacion/100) ** (mes/12))
        inflacion_perdida = capital - capital_real

        lista.append({
            "mes": mes,
            "aportada": capital_aportado,
            "total": capital,
            "inflacion": inflacion_perdida,
            "neta": capital_real
        })

    return lista

# ============================
#   MARCA DE AGUA DIAGONAL
# ============================

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
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="srg-title">Datos personales</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    edad_actual = st.number_input(
        "Edad actual",
        18, 70, 40,
        help="Tu edad hoy. Se usa para calcular los años que faltan hasta la jubilación."
    )

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
        60, 75, 67,
        help="La edad a la que deseas jubilarte. Afecta a la pensión y al tiempo de ahorro."
    )

    esperanza_vida = st.number_input(
        "Esperanza de vida",
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
    )

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
        0, edad_prevista_jub - edad_actual, 0,
        help="Años que te quedan por cotizar hasta la jubilación."
    )

    st.markdown('</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
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

    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
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
    )

    reval = st.number_input(
        "Revalorización anual pensión (%)",
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

    modo_brecha = st.radio(
        "¿Qué quieres cubrir?",
        ["Objetivo económico", "Gastos reales"],
        horizontal=True,
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
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


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

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
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

# -------- GENERAR HTML DEL INFORME --------
if tipo_informe == "Cliente":
    html_informe = informe_cliente(contexto_pdf, fig)
else:
    html_informe = informe_agente(contexto_pdf, fig)

bytes_informe = html_informe.encode("utf-8")

# -------- COLUMNA 2: DESCARGAR INFORME --------
with col_desc:
    st.markdown('<div class="srg-title">Descargar informe</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    with st.expander("Resumen del informe"):
        st.write(f"**Pensión futura estimada:** {pension_futura:,.0f} €/mes")
        st.write(f"**Objetivo mensual futuro:** {objetivo_futuro:,.0f} €")
        st.write(f"**Gastos futuros estimados:** {gastos_futuros:,.0f} €")
        st.write(f"**Brecha mensual:** {brecha:,.0f} €")
        st.write(f"**Aportación mensual recomendada:** {aportacion:,.0f} €")

    if nombre_cliente:
        st.write("---")
        st.write("### Datos del cliente")
        st.write(f"**Nombre:** {nombre_cliente}")
        st.write(f"**Email:** {email_cliente}")
        st.write(f"**Teléfono:** {telefono_cliente}")



    st.download_button(
        label="Descargar informe SRG (HTML imprimible)",
        data=bytes_informe,
        file_name="informe_jubilacion_srg.html",
        mime="text/html"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
#   FOOTER PROFESIONAL SRG
# ============================================

footer_html = """
<div class="srg-footer">
    <div><b>Simulador SRG — Samuel Ruiz González </b></div>
    <div>Herramienta educativa y formativa para Agentes.</div>
    <div>© 2025 Samuel Ruiz González · <a href="#">Política de privacidad</a> · <a href="#">Aviso legal</a></div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
