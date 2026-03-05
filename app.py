# BLOQUE 1 — IMPORTS, CSS, FUNCIONES AUXILIARES, DATOS BASE

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
@import url('https://://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&display=swap');

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
    r_mensual = rentabilidad / 12 if rentabilidad is not None else 0

    capital = 0
    lista = []

    for mes in range(meses + 1):
        if mes > 0:
            capital = capital * (1 + r_mensual) + aportacion

        capital_aportado = aportacion * mes
        capital_real = capital / ((1 + inflacion/100) ** (mes/12)) if inflacion is not None else capital
        inflacion_perdida = capital - capital_real

        lista.append({
            "mes": mes,
            "aportada": capital_aportado,
            "total": capital,
            "inflacion": inflacion_perdida,
            "neta": capital_real
        })

    return lista

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
    edad_actual = st.number_input("Edad actual", 18, 70, 40)
    edad_prevista_jub = st.number_input("Edad prevista de jubilación", 60, 75, 67)
    esperanza_vida = st.number_input("Esperanza de vida", 75, 100, 85)
    st.markdown('</div>', unsafe_allow_html=True)

if edad_prevista_jub <= edad_actual:
    edad_prevista_jub = edad_actual + 1
if esperanza_vida <= edad_prevista_jub:
    esperanza_vida = edad_prevista_jub + 1

with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
    anos_cotizados_hoy = st.number_input("Años cotizados hoy", 0, 50, 10)
    anos_futuros = st.number_input("Años que cotizarás desde hoy", 0, 50, 0)
    st.markdown('</div>', unsafe_allow_html=True)

if anos_cotizados_hoy > edad_actual - 16:
    anos_cotizados_hoy = max(0, edad_actual - 16)
if anos_futuros > edad_prevista_jub - edad_actual:
    anos_futuros = max(0, edad_prevista_jub - edad_actual)

with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
    tipo_jubilacion = st.selectbox(
        "Tipo prevista",
        ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"]
    )
    meses_anticipo = st.number_input("Meses anticipo (+) / demora (-)", -120, 60, 0)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
    ingresos = st.number_input("Ingresos mensuales (€)", 0, 20000, 2500)
    gastos = st.number_input("Gastos mensuales (€)", 0, ingresos, 1800)
    capacidad = ingresos - gastos
    st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")
    st.markdown('</div>', unsafe_allow_html=True)

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
# BLOQUE 2 — PENSIÓN, BRECHA Y PLAN DE AHORRO RECOMENDADO + GRÁFICA BASE

colA, colB, colC, colD = st.columns(4)

with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
    base = st.number_input(
        "Base reguladora (€)",
        min_value=0,
        max_value=50000,
        value=1500,
        help="Promedio de tus bases de cotización. Determina tu pensión."
    )
    inflacion = st.number_input(
        "Inflación anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="La inflación reduce el poder adquisitivo del dinero con el tiempo."
    )
    reval = st.number_input(
        "Revalorización anual pensión (%)",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Incremento anual estimado de la pensión pública."
    )
    st.markdown('</div>', unsafe_allow_html=True)

if modo_valido:
    pct = min(1.0, anos_totales / 37)
else:
    pct = 0.0

pension_hoy = base * pct * coef_ajuste
pension_futura = pension_hoy * ((1 + reval/100) ** anos_hasta_jub)

with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
    st.metric("Porcentaje sobre base", f"{pct*100:,.1f} %")
    st.metric("Pensión ajustada hoy", f"{pension_hoy:,.0f} €")
    st.metric("Pensión futura estimada", f"{pension_futura:,.0f} €/mes")
    st.markdown('</div>', unsafe_allow_html=True)

with colC:
    st.markdown('<div class="srg-title">Objetivo económico</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)
    objetivo_hoy = st.number_input(
        "Ingresos deseados hoy (€)",
        min_value=0,
        max_value=20000,
        value=2000,
        help="Ingresos mensuales que te gustaría mantener en jubilación."
    )
    pct_mantener = st.number_input(
        "Gastos que mantendrás en jubilación (%)",
        min_value=50,
        max_value=120,
        value=90,
        help="Porcentaje de tus gastos actuales que mantendrás en jubilación."
    )
    st.markdown('</div>', unsafe_allow_html=True)

objetivo_futuro, gastos_futuros = calcular_objetivo_y_gastos_futuros(
    objetivo_hoy,
    gastos,
    pct_mantener,
    inflacion,
    anos_hasta_jub
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
    if modo_brecha == "Objetivo económico":
        brecha = objetivo_futuro - pension_futura
    else:
        brecha = gastos_futuros - pension_futura
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
#   PLAN DE AHORRO RECOMENDADO
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
        aportacion_recom = 0.0
        capital_necesario = 0.0
        evolucion_recom = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, 0.0)
    else:
        if rentabilidad == 0:
            capital_necesario = brecha * 12 * anos_jubilacion
        else:
            capital_necesario = brecha * 12 * (1 - (1 + rentabilidad)**(-anos_jubilacion)) / rentabilidad

        meses_hasta_jub = anos_hasta_jub * 12
        r_mensual = rentabilidad / 12

        if meses_hasta_jub > 0:
            if rentabilidad == 0:
                aportacion_recom = capital_necesario / meses_hasta_jub
            else:
                aportacion_recom = capital_necesario * r_mensual / ((1 + r_mensual)**meses_hasta_jub - 1)
        else:
            aportacion_recom = 0.0

        st.metric("Capital necesario al jubilarte", f"{capital_necesario:,.0f} €")
        st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €/mes")

        evolucion_recom = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, aportacion_recom)

    capital_total_recom = evolucion_recom[-1]["total"]
    capital_aportado_recom = evolucion_recom[-1]["aportada"]
    capital_real_final_recom = evolucion_recom[-1]["neta"]
    capital_rendimientos_recom = capital_total_recom - capital_aportado_recom

    st.markdown("### Desglose del capital acumulado al jubilarte (escenario recomendado)")
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        st.metric("Capital aportado", f"{capital_aportado_recom:,.0f} €")
        st.metric("Rendimientos obtenidos", f"{capital_rendimientos_recom:,.0f} €")
    with col_cap2:
        st.metric("Capital total acumulado", f"{capital_total_recom:,.0f} €")
        st.metric("Capital neto (ajustado inflación)", f"{capital_real_final_recom:,.0f} €")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================
#   GRÁFICA EVOLUCIÓN CAPITAL (RECOMENDADO + CLIENTE SI EXISTE)
# ============================

# Inicializamos variables de escenarios adicionales (se rellenan en bloque 3)
evolucion_cliente = None
cuota_cliente = 0.0

with colP2:
    st.markdown('<div class="srg-title">Evolución del capital</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    evolucion_sin_mes0 = evolucion_recom[1:]
    anos_evol = [fila["mes"]/12 for fila in evolucion_sin_mes0]
    total_recom = [fila["total"] for fila in evolucion_sin_mes0]
    aportada_recom = [fila["aportada"] for fila in evolucion_sin_mes0]
    neta_recom = [fila["neta"] for fila in evolucion_sin_mes0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=anos_evol, y=total_recom,
        mode='lines',
        name='Escenario recomendado: aportado + rendimientos',
        line=dict(color='#003366', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=anos_evol, y=aportada_recom,
        mode='lines',
        name='Escenario recomendado: cantidad aportada',
        line=dict(color='#66a3ff', width=2, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=anos_evol, y=neta_recom,
        mode='lines',
        name='Escenario recomendado: cantidad neta (ajustada inflación)',
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
# BLOQUE 3 — SIMULACIONES DE AHORRO (CUOTA CLIENTE + COMPARATIVA)

st.markdown('<div class="srg-title">Simulaciones de ahorro</div>', unsafe_allow_html=True)
st.markdown('<div class="srg-box">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Cuota recomendada", "Simular mi cuota", "Comparativa de cuotas"])

# Variables para informes
cuota_cliente = 0.0
capital_total_cliente = 0.0
porc_cobertura_cliente = 0.0
brecha_restante_cliente = brecha
comparativa_cuotas = []

with tab1:
    st.markdown("### Escenario recomendado")
    st.write(
        "Este escenario utiliza la aportación mensual recomendada para cubrir la brecha calculada "
        "en función de tus datos y de la rentabilidad asumida."
    )
    st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €/mes")
    st.metric("Capital total al jubilarte", f"{capital_total_recom:,.0f} €")
    st.metric("Capital neto (ajustado por inflación)", f"{capital_real_final_recom:,.0f} €")

with tab2:
    st.markdown("### Simular mi cuota")
    cuota_cliente = st.number_input(
        "Cuota mensual que quieres aportar (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(round(aportacion_recom, 0)) if aportacion_recom > 0 else 100.0,
        step=10.0,
        help="Introduce la cuota mensual que el cliente está dispuesto a aportar. "
             "El sistema calculará el capital final y el porcentaje de brecha cubierta."
    )

    if cuota_cliente > 0:
        evolucion_cliente = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, cuota_cliente)
        capital_total_cliente = evolucion_cliente[-1]["total"]
        # % de cobertura respecto al capital necesario
        if capital_necesario > 0:
            porc_cobertura_cliente = min(capital_total_cliente / capital_necesario, 1.0) * 100
        else:
            porc_cobertura_cliente = 100.0
        brecha_restante_cliente = brecha * (1 - porc_cobertura_cliente / 100.0)

        st.metric("Capital total con tu cuota", f"{capital_total_cliente:,.0f} €")
        st.metric("Cobertura de la brecha", f"{porc_cobertura_cliente:,.1f} %")
        st.metric("Brecha mensual restante", f"{brecha_restante_cliente:,.0f} €")

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
                name='Tu cuota: aportado + rendimientos',
                line=dict(color='#AA0000', width=3)
            ))
            fig_cli.add_trace(go.Scatter(
                x=anos_cli, y=aportada_cli,
                mode='lines',
                name='Tu cuota: cantidad aportada',
                line=dict(color='#FF6666', width=2, dash='dash')
            ))
            fig_cli.add_trace(go.Scatter(
                x=anos_cli, y=neta_cli,
                mode='lines',
                name='Tu cuota: cantidad neta (ajustada inflación)',
                line=dict(color='#CC6600', width=2)
            ))
            fig_cli.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="Años hasta jubilación",
                yaxis_title="Capital (€)"
            )
            st.plotly_chart(fig_cli, use_container_width=True)

    else:
        st.info("Introduce una cuota mensual mayor que 0 para simular tu propio escenario.")

with tab3:
    st.markdown("### Comparativa de cuotas")
    st.write(
        "Esta tabla compara distintos niveles de aportación y su impacto en el capital final y en la cobertura de la brecha."
    )
    cuota_base = st.number_input(
        "Cuota base para la comparativa (€)",
        min_value=0.0,
        max_value=50000.0,
        value=float(round(aportacion_recom, 0)) if aportacion_recom > 0 else 200.0,
        step=10.0,
        help="Cuota de referencia a partir de la cual se generarán escenarios de comparación."
    )
    rango = st.number_input(
        "Rango de variación por escenario (€)",
        min_value=10.0,
        max_value=1000.0,
        value=50.0,
        step=10.0,
        help="Diferencia en euros entre cada escenario de cuota."
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

# Actualizamos la gráfica principal para mostrar también la cuota del cliente si existe
if evolucion_cliente is not None and cuota_cliente > 0:
    evolucion_sin_mes0_cli = evolucion_cliente[1:]
    anos_cli = [fila["mes"]/12 for fila in evolucion_sin_mes0_cli]
    total_cli = [fila["total"] for fila in evolucion_sin_mes0_cli]

    fig.add_trace(go.Scatter(
        x=anos_cli, y=total_cli,
        mode='lines',
        name='Escenario cliente: aportado + rendimientos',
        line=dict(color='#AA0000', width=2, dash='dot')
    ))
# BLOQUE 4 — MODO AGENTE SRG E INFORME CLIENTE

# ============================
#   MODO AGENTE SRG
# ============================

st.markdown('<div class="srg-title">Modo Agente SRG</div>', unsafe_allow_html=True)
with st.expander("Guion comercial para explicar al cliente"):
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
"Actualmente tienes **{anos_cotizados_hoy} años cotizados** y planeas cotizar **{anos_futuros} años más**, con una jubilación a los **{edad_prevista_jub} años**."

**2. Pensión pública estimada**  
"Con la modalidad **{tipo_jubilacion}**, tu pensión futura estimada sería de **{pension_futura:,.0f} €/mes**."

**3. Objetivo y brecha**  
"Tu objetivo de ingresos futuros es de **{objetivo_futuro:,.0f} €/mes**, y tus gastos futuros se estiman en **{gastos_futuros:,.0f} €/mes**.  
La brecha a cubrir es de **{brecha:,.0f} €/mes**."

**4. Plan de ahorro recomendado**  
"Para cubrir esta brecha, estimamos que necesitas acumular **{capital_necesario:,.0f} €** al jubilarte, con una aportación mensual aproximada de **{aportacion_recom:,.0f} €/mes**, asumiendo una rentabilidad anual del **{rentabilidad*100:.1f}%** y una inflación del **{inflacion:.1f}%**."

**5. Escenario con la cuota del cliente**  
{texto_cuota_cliente if texto_cuota_cliente else "En caso de que el cliente proponga una cuota distinta, podemos comparar cuánto de la brecha se cubriría con su aportación."}

**6. Comparativa de escenarios**  
"Además, hemos analizado distintos niveles de aportación para que puedas ver cómo cambia la cobertura de la brecha según la cuota mensual que decidas."

**7. Cierre**  
"A partir de aquí, podemos diseñar juntos la combinación de productos de ahorro e inversión que mejor se adapte a tu perfil."
        """)

# ============================
#   INFORME CLIENTE (HTML)
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
            <div class="srg-card-value">{contexto['aportacion_recom']:,.0f} €/mes</div>
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

    <h2>3. Evolución del ahorro (escenario recomendado)</h2>
    <table class="srg-table">
        <tr>
            <th>Mes/Año</th>
            <th>Aportación acumulada</th>
            <th>Capital total</th>
            <th>Impacto de la inflación</th>
            <th>Capital neto real</th>
        </tr>
        {tabla_mensual_y_anual_html(contexto['evolucion_recom'], contexto['anos_hasta_jub'])}
    </table>

    <h2>4. Escenario con tu propia cuota</h2>
    <div class="srg-highlight-box">
        <p>Has indicado que podrías aportar <b>{contexto['cuota_cliente']:,.0f} €/mes</b>.</p>
        <p>Con esta cuota, el capital total estimado al llegar a la jubilación sería de
        <b>{contexto['capital_total_cliente']:,.0f} €</b>, lo que te permitiría cubrir aproximadamente
        el <b>{contexto['porc_cobertura_cliente']:,.1f}%</b> de la brecha.</p>
        <p>La brecha mensual restante sería de <b>{contexto['brecha_restante_cliente']:,.0f} €</b>.</p>
    </div>

    <h2>5. Comparativa de cuotas</h2>
    <table class="srg-table">
        <tr>
            <th>Cuota mensual</th>
            <th>Capital final</th>
            <th>Cobertura brecha</th>
            <th>Brecha restante</th>
        </tr>
"""
    for esc in contexto["comparativa_cuotas"]:
        html += f"""
        <tr>
            <td>{esc['cuota']:,.0f} €/mes</td>
            <td>{esc['capital']:,.0f} €</td>
            <td>{esc['porc_cobertura']:,.1f} %</td>
            <td>{esc['brecha_restante']:,.0f} €</td>
        </tr>
"""
    html += f"""
    </table>

    <h2>6. Gráfica de evolución</h2>
    <div class="srg-chart-container">
        {fig.to_html(include_plotlyjs='cdn', full_html=False)}
    </div>

    <h2>7. Explicación de tus resultados</h2>
    <div class="srg-highlight-box">
        <p>Según los datos que nos has proporcionado, tu pensión pública futura estimada sería de
        <b>{contexto['pension_futura']:,.0f} € al mes</b>.</p>

        <p>Para mantener tu nivel de vida, tu objetivo económico futuro se sitúa en
        <b>{contexto['objetivo_futuro']:,.0f} € mensuales</b>. La diferencia entre lo que necesitarás
        y lo que recibirás —la <b>brecha</b>— es de
        <b>{contexto['brecha']:,.0f} € al mes</b>.</p>

        <p>Con la aportación recomendada de <b>{contexto['aportacion_recom']:,.0f} €/mes</b> podrías cubrir
        prácticamente el 100% de esa brecha, mientras que con tu cuota actual de
        <b>{contexto['cuota_cliente']:,.0f} €/mes</b> cubrirías aproximadamente el
        <b>{contexto['porc_cobertura_cliente']:,.1f}%</b>.</p>
    </div>

    <h2>8. Conclusión personalizada</h2>
    <p><b>Tu situación financiera actual demuestra que estás dando pasos sólidos hacia una jubilación estable y bien planificada.</b></p>

    <p>Este plan te permite avanzar con seguridad hacia una jubilación tranquila, con ingresos suficientes para
    mantener tu estilo de vida y afrontar imprevistos.</p>

    <p><b>Estás tomando decisiones inteligentes hoy que tendrán un impacto directo en tu bienestar futuro.</b></p>

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
# BLOQUE 5 — INFORME AGENTE, RESUMEN EJECUTIVO

def informe_agente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")

    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Informe Agente SRG</title>

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
        max-width: 950px;
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
    <div class="srg-cover-title">Informe Técnico SRG</div>
    <div class="srg-cover-subtitle">Uso interno para agente</div>
    <div class="srg-cover-client">Cliente: <b>{contexto['nombre_cliente'] or "Cliente SRG"}</b></div>
    <div class="srg-cover-date">Fecha de generación: {fecha}</div>
    <div class="srg-cover-footer-line"></div>
    <div class="srg-cover-footer-text">SRG Consultora Financiera · Soporte técnico para el análisis de jubilación</div>
</div>

<div class="srg-container">

    <h2>1. Resumen técnico</h2>
    <div class="srg-highlight-box">
        <p><b>Pensión futura estimada:</b> {contexto['pension_futura']:,.0f} €/mes</p>
        <p><b>Brecha mensual estimada:</b> {contexto['brecha']:,.0f} €</p>
        <p><b>Aportación mensual recomendada:</b> {contexto['aportacion_recom']:,.0f} €/mes</p>
        <p><b>Cuota propuesta por el cliente:</b> {contexto['cuota_cliente']:,.0f} €/mes</p>
        <p><b>Cobertura de la brecha con la cuota del cliente:</b> {contexto['porc_cobertura_cliente']:,.1f}%</p>
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

    <h2>4. Escenarios de aportación</h2>
    <table class="srg-table">
        <tr>
            <th>Escenario</th>
            <th>Cuota mensual</th>
            <th>Capital final</th>
            <th>Cobertura brecha</th>
            <th>Brecha restante</th>
        </tr>
        <tr>
            <td>Recomendado</td>
            <td>{contexto['aportacion_recom']:,.0f} €/mes</td>
            <td>{contexto['capital_total_recom']:,.0f} €</td>
            <td>≈ 100 %</td>
            <td>≈ 0 €</td>
        </tr>
        <tr>
            <td>Cliente</td>
            <td>{contexto['cuota_cliente']:,.0f} €/mes</td>
            <td>{contexto['capital_total_cliente']:,.0f} €</td>
            <td>{contexto['porc_cobertura_cliente']:,.1f} %</td>
            <td>{contexto['brecha_restante_cliente']:,.0f} €</td>
        </tr>
"""
    for esc in contexto["comparativa_cuotas"]:
        html += f"""
        <tr>
            <td>Comparativa</td>
            <td>{esc['cuota']:,.0f} €/mes</td>
            <td>{esc['capital']:,.0f} €</td>
            <td>{esc['porc_cobertura']:,.1f} %</td>
            <td>{esc['brecha_restante']:,.0f} €</td>
        </tr>
"""
    html += f"""
    </table>

    <h2>5. Evolución del ahorro (escenario recomendado)</h2>
    <table class="srg-table">
        <tr>
            <th>Mes/Año</th>
            <th>Aportación acumulada</th>
            <th>Capital total</th>
            <th>Impacto de la inflación</th>
            <th>Capital neto real</th>
        </tr>
        {tabla_mensual_y_anual_html(contexto['evolucion_recom'], contexto['anos_hasta_jub'])}
    </table>

    <h2>6. Gráfica de evolución</h2>
    <div class="srg-chart-container">
        {fig.to_html(include_plotlyjs='cdn', full_html=False)}
    </div>

    <h2>7. Comentario técnico</h2>
    <p>Este caso ilustra la importancia de complementar la pensión pública con ahorro privado, especialmente en escenarios donde la inflación y la esperanza de vida prolongada amplifican la brecha entre la pensión y el nivel de ingresos deseado.</p>

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

# ============================
#   RESUMEN EJECUTIVO SRG
# ============================

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
    st.metric("Aportación mensual recomendada", f"{aportacion_recom:,.0f} €")

st.markdown('</div>', unsafe_allow_html=True)
# BLOQUE 6 — GENERAR INFORME, DESCARGA Y FOOTER

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
    "nombre_cliente": nombre_cliente,
    "email_cliente": email_cliente,
    "telefono_cliente": telefono_cliente,
    "cuota_cliente": cuota_cliente,
    "capital_total_cliente": capital_total_cliente,
    "porc_cobertura_cliente": porc_cobertura_cliente,
    "brecha_restante_cliente": brecha_restante_cliente,
    "comparativa_cuotas": comparativa_cuotas,
    "capital_total_recom": capital_total_recom
}

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
        st.write(f"**Aportación mensual recomendada:** {aportacion_recom:,.0f} €/mes")
        if cuota_cliente > 0:
            st.write(f"**Cuota del cliente:** {cuota_cliente:,.0f} €/mes")
            st.write(f"**Cobertura brecha con cuota cliente:** {porc_cobertura_cliente:,.1f} %")
        if nombre_cliente:
            st.write("---")
            st.write("### Datos del cliente")
            st.write(f"**Nombre:** {nombre_cliente}")
            st.write(f"**Email:** {email_cliente}")
            st.write(f"**Teléfono:** {telefono_cliente}")

    with st.expander("Vista previa del informe (HTML)"):
        components.html(html_informe, height=700, scrolling=True)

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
