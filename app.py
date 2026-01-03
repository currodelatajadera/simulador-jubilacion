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

/* TITULOS DE SECCIÓN */
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
#   TABLA MENSUAL (RESUMIDA)
# ============================

def tabla_mensual_y_anual_html(evolucion, anos_hasta_jub):
    filas = ""

    # Primeros 12 meses (1-12)
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

    # Después año a año
    for ano in range(2, anos_hasta_jub + 1):
        indice = ano * 12
        if indice < len(evolucion):
            fila = evolucion[indice]
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

# ============================
#   FILA 1 — DATOS PRINCIPALES
# ============================

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

    st.markdown('</div>', unsafe_allow_html=True)

# Ajustes de coherencia en edades
if edad_actual >= edad_prevista_jub:
    st.warning("La edad prevista de jubilación debe ser mayor que la edad actual. Se ajusta automáticamente.")
    edad_prevista_jub = edad_actual + 1

if esperanza_vida <= edad_prevista_jub:
    st.warning("La esperanza de vida debe ser mayor que la edad de jubilación. Se ajusta automáticamente.")
    esperanza_vida = edad_prevista_jub + 1

with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    anos_cotizados_hoy = st.number_input(
        "Años cotizados hoy",
        0, max(1, edad_actual - 16), 10,
        help="Años que ya has cotizado a la Seguridad Social."
    )

    anos_futuros = st.number_input(
        "Años que cotizarás desde hoy",
        0, max(1, edad_prevista_jub - edad_actual), 0,
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

# ============================
#   CÁLCULOS LEGALES
# ============================

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
anos_hasta_jub = max(1, edad_prevista_jub - edad_actual)
anos_jubilacion = max(1, esperanza_vida - edad_prevista_jub)

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

# ============================
#   EXPLICACIÓN DETALLADA
# ============================

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

# ============================
#   FILA 2 — PENSIÓN, OBJETIVO Y BRECHA
# ============================

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

# ============================
#   PLAN DE AHORRO
# ============================

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

# ============================
#   GRÁFICA EVOLUCIÓN CAPITAL
# ============================

with colP2:
    st.markdown('<div class="srg-title">Evolución del capital</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

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

# ============================
#   MODO AGENTE SRG
# ============================

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

# ============================
#   INFORMES HTML (CLIENTE/AGENTE)
# ============================

def informe_cliente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Informe Cliente SRG</title>

<style>
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
        position: relative;
        z-index: 1;
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

    .srg-container {{
        max-width: 900px;
        margin: 40px auto 60px auto;
        background-color: #ffffff;
        padding: 32px 40px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
        border-radius: 12px;
        position: relative;
        z-index: 1;
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

    .srg-highlight-box {{
        border: 1px solid #0055A4;
        border-radius: 10px;
        padding: 12px 16px;
        background-color: #f9fbff;
        margin-top: 8px;
    }}

    .srg-chart-container {{
        margin-top: 10px;
        margin-bottom: 10px;
        padding: 10px 12px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border: 1px solid #e1e6f0;
    }}

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

{marca_agua_srg()}

<div class="srg-cover">
    <div class="srg-cover-title">Informe de Proyección de Jubilación SRG</div>
    <div class="srg-cover-subtitle">Simulación personalizada</div>
    <div class="srg-cover-client">Informe para: <b>{contexto['nombre_cliente'] or "Cliente SRG"}</b></div>
    <div class="srg-cover-date">Fecha de generación: {fecha}</div>
    <div class="srg-cover-footer-line"></div>
    <div class="srg-cover-footer-text">SRG Consultora Financiera · Herramienta de planificación y educación financiera</div>
</div>

<div class="srg-container">

    <h2>1. Resumen ejecutivo</h2>

    <div class="srg-cards">
