import streamlit as st
import numpy as np
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Simulador de Jubilación SRG", page_icon="💼", layout="wide")

# ============================
#   CSS GLOBAL PREMIUM SRG (CORREGIDO PARA NUBE)
# ============================

st.markdown("""
<style>
/* 1. IMPORTAMOS FUENTES (Dancing Script y Montserrat) */
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&family=Montserrat:wght@300;400;600;700&display=swap');

/* 2. FORZAMOS ESTILOS GLOBALES (Evita problemas de Modo Oscuro) */
html, body, [class*="css"], .stApp {
    font-family: 'Montserrat', sans-serif;
    background-color: #ffffff; 
    color: #222222; 
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
    color: #ffffff !important;
    margin: 0;
    line-height: 1.1;
}

.srg-header-title-sub {
    font-family: 'Dancing Script', cursive !important;
    font-size: 1.8rem;
    font-weight: 400;
    color: #d0d8e8 !important;
    margin-top: 6px;
}

/* TÍTULOS DE SECCIÓN */
.srg-title {
    background: linear-gradient(135deg, #003366, #0055A4);
    color: white !important;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

/* ESTILO PARA LOS CONTENEDORES NATIVOS (Sustituye a .srg-box) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(180deg, #ffffff, #f2f6fb);
    border: 1px solid #c7d4e5 !important;
    border-radius: 8px;
    padding: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Ajuste interno para evitar fondos dobles */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background-color: transparent !important;
}

/* FOOTER */
.srg-footer {
    margin-top: 30px;
    padding: 16px 12px;
    background: linear-gradient(135deg, #003366, #0055A4);
    color: #ffffff !important;
    text-align: center;
    font-size: 0.85rem;
    border-radius: 6px 6px 0 0;
}

.srg-footer a {
    color: #ffffff !important;
    text-decoration: underline;
}

/* MÉTRICAS */
[data-testid="stMetricValue"] {
    font-size: 1.1rem;
    color: #003366 !important;
}
[data-testid="stMetricLabel"] {
    color: #444444 !important;
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

def tabla_mensual_y_anual_html(evolucion, anos_hasta_jub):
    filas = ""
    # --- Primeros 12 meses ---
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
    with st.container(border=True):
        edad_actual = st.number_input(
            "Edad actual",
            18, 70, 40,
            help="Tu edad hoy."
        )
        edad_prevista_jub = st.number_input(
            "Edad prevista de jubilación",
            60, 75, 67,
            help="La edad a la que deseas jubilarte."
        )
        esperanza_vida = st.number_input(
            "Esperanza de vida",
            75, 100, 85,
            help="Estimación de vida."
        )

# Correcciones de edad
if edad_actual >= edad_prevista_jub:
    edad_prevista_jub = edad_actual + 1
if esperanza_vida <= edad_prevista_jub:
    esperanza_vida = edad_prevista_jub + 1

with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    with st.container(border=True):
        anos_cotizados_hoy = st.number_input(
            "Años cotizados hoy",
            0, edad_actual - 16, 10
        )
        anos_futuros = st.number_input(
            "Años que cotizarás desde hoy",
            0, edad_prevista_jub - edad_actual, 0
        )

with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    with st.container(border=True):
        tipo_jubilacion = st.selectbox(
            "Tipo prevista",
            ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria", "Demorada"]
        )
        meses_anticipo = st.number_input(
            "Meses anticipo (+) / demora (-)",
            -120, 60, 0
        )

with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
    with st.container(border=True):
        ingresos = st.number_input("Ingresos mensuales (€)", 0, 20000, 2500)
        gastos = st.number_input("Gastos mensuales (€)", 0, 20000, 1800)
        capacidad = ingresos - gastos
        st.metric("Capacidad de ahorro", f"{capacidad:,.0f} €")

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
    st.error("La modalidad seleccionada NO es válida.")

with st.expander("Ver explicación detallada"):
    st.write(f"**Modalidad:** {tipo_jubilacion}")
    st.write(f"**Total años cotizados previstos:** {anos_totales}")
    st.write(f"**Años hasta la jubilación:** {anos_hasta_jub}")
    st.write(f"**Coeficiente aplicado:** {coef_ajuste:.3f}")

# ============================================
#   FILA 2 — PENSIÓN, OBJETIVO Y BRECHA
# ============================================

colA, colB, colC, colD = st.columns(4)

with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    with st.container(border=True):
        base = st.number_input("Base reguladora (€)", 0, 50000, 1500)
        inflacion = st.number_input("Inflación anual (%)", 0.0, 10.0, 2.0, 0.1)
        reval = st.number_input("Revalorización pensión (%)", 0.0, 5.0, 1.5, 0.1)

# Cálculo pensión
pct = min(1, anos_totales / 37) if modo_valido else 0
pension_hoy = base * pct * coef_ajuste
pension_futura = pension_hoy * ((1 + reval/100) ** anos_hasta_jub)

with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write(f"**Porcentaje base:** {pct*100:,.1f} %")
        st.write(f"**Pensión hoy:** {pension_hoy:,.0f} €")
        st.write(f"**Pensión futura:** {pension_futura:,.0f} €/mes")

with colC:
    st.markdown('<div class="srg-title">Objetivo económico</div>', unsafe_allow_html=True)
    with st.container(border=True):
        objetivo_hoy = st.number_input("Ingresos deseados hoy (€)", 0, 20000, 2000)
        pct_mantener = st.number_input("Gastos a mantener (%)", 50, 120, 90)

objetivo_futuro, gastos_futuros = calcular_objetivo_y_gastos_futuros(
    objetivo_hoy, gastos, pct_mantener, inflacion, anos_hasta_jub
)

with colC:
    with st.container(border=False): # Visual extra
        st.metric("Objetivo futuro", f"{objetivo_futuro:,.0f} €")

with colD:
    st.markdown('<div class="srg-title">Brecha</div>', unsafe_allow_html=True)
    with st.container(border=True):
        modo_brecha = st.radio("¿Qué cubrir?", ["Objetivo económico", "Gastos reales"], horizontal=True)
        brecha = objetivo_futuro - pension_futura if modo_brecha == "Objetivo económico" else gastos_futuros - pension_futura
        st.metric("Brecha mensual", f"{brecha:,.0f} €")

# ============================================
#   PLAN DE AHORRO
# ============================================

colP1, colP2 = st.columns([1, 2])

with colP1:
    st.markdown('<div class="srg-title">Plan de ahorro</div>', unsafe_allow_html=True)
    with st.container(border=True):
        rentabilidad = st.number_input("Rentabilidad anual (%)", 0.0, 15.0, 4.0, 0.1) / 100

        if brecha <= 0:
            aportacion = 0
            capital_necesario = 0
            evolucion = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, 0)
            st.success("Sin brecha estimada.")
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

            st.metric("Capital necesario", f"{capital_necesario:,.0f} €")
            st.metric("Aportación mensual", f"{aportacion:,.0f} €/mes")

            evolucion = calcular_evolucion_mensual(anos_hasta_jub, rentabilidad, inflacion, aportacion)

        # Resumen capital
        capital_total = evolucion[-1]["total"]
        st.write("---")
        st.metric("Capital total acumulado", f"{capital_total:,.0f} €")

with colP2:
    st.markdown('<div class="srg-title">Evolución del capital</div>', unsafe_allow_html=True)
    with st.container(border=True):
        evolucion_sin_mes0 = evolucion[1:]
        anos_evol = [fila["mes"]/12 for fila in evolucion_sin_mes0]
        total = [fila["total"] for fila in evolucion_sin_mes0]
        aportada = [fila["aportada"] for fila in evolucion_sin_mes0]
        neta = [fila["neta"] for fila in evolucion_sin_mes0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=anos_evol, y=total, mode='lines', name='Total', line=dict(color='#003366', width=3)))
        fig.add_trace(go.Scatter(x=anos_evol, y=aportada, mode='lines', name='Aportado', line=dict(color='#66a3ff', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=anos_evol, y=neta, mode='lines', name='Real (Neto)', line=dict(color='#009999', width=2)))

        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_title="Años",
            yaxis_title="€"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
#   MODO AGENTE SRG
# ============================================

st.markdown('<div class="srg-title">Modo Agente SRG</div>', unsafe_allow_html=True)
with st.container(border=True):
    with st.expander("Guion comercial"):
        modo_agente = st.checkbox("Activar Modo Agente")
        if modo_agente:
            st.markdown(f"""
            - **Situación:** {anos_cotizados_hoy} años cotizados. Jubilación a los {edad_prevista_jub}.
            - **Brecha:** {brecha:,.0f} €/mes.
            - **Solución:** Aportar {aportacion:,.0f} €/mes al {rentabilidad*100:.1f}%.
            """)

# ============================================
#   RESUMEN EJECUTIVO
# ============================================
st.markdown('<div class="srg-title">Resumen ejecutivo</div>', unsafe_allow_html=True)
with st.container(border=True):
    colR1, colR2, colR3, colR4 = st.columns(4)
    colR1.metric("Pensión futura", f"{pension_futura:,.0f} €")
    colR2.metric("Objetivo", f"{objetivo_futuro:,.0f} €")
    colR3.metric("Brecha", f"{brecha:,.0f} €")
    colR4.metric("Aportación", f"{aportacion:,.0f} €")

# ============================================
#   GENERACIÓN DE INFORMES (HTML)
# ============================================

def informe_cliente(contexto, fig):
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Informe Cliente SRG</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
        body {{ font-family: 'Montserrat', sans-serif; color: #222; padding: 20px; }}
        .srg-header {{ background: #003366; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }}
        h2 {{ color: #003366; border-left: 4px solid #0055A4; padding-left: 10px; }}
        .metric-box {{ border: 1px solid #ddd; padding: 10px; margin: 5px; background: #f9f9f9; display: inline-block; width: 45%; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th {{ background: #003366; color: white; padding: 8px; }}
        td {{ border-bottom: 1px solid #ddd; padding: 8px; }}
    </style>
    </head>
    <body>
    <div class="srg-header">
        <h1>Informe de Jubilación</h1>
        <p>Cliente: {contexto['nombre_cliente']} - {fecha}</p>
    </div>
    <h2>Resumen</h2>
    <div class="metric-box"><b>Pensión Estimada:</b> {contexto['pension_futura']:,.0f} €</div>
    <div class="metric-box"><b>Brecha Mensual:</b> {contexto['brecha']:,.0f} €</div>
    <div class="metric-box"><b>Objetivo:</b> {contexto['objetivo_futuro']:,.0f} €</div>
    <div class="metric-box"><b>Aportación Recomendada:</b> {contexto['aportacion']:,.0f} €</div>

    <h2>Evolución</h2>
    <p>Gráfica adjunta en la aplicación.</p>
    <table>
        <tr><th>Mes/Año</th><th>Aportado</th><th>Total</th><th>Neto Real</th></tr>
        {tabla_mensual_y_anual_html(contexto['evolucion'], contexto['anos_hasta_jub'])}
    </table>
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
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
        body {{ font-family: 'Montserrat', sans-serif; color: #333; padding: 20px; }}
        h2 {{ color: #003366; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #444; color: white; padding: 5px; }}
        td {{ border: 1px solid #ccc; padding: 5px; }}
    </style>
    </head>
    <body>
    <h1>Informe Técnico (Agente)</h1>
    <p>Cliente: {contexto['nombre_cliente']} | Fecha: {fecha}</p>
    
    <h2>Datos Técnicos</h2>
    <ul>
        <li><b>Coeficiente Ajuste:</b> {contexto['coef_ajuste']:.3f}</li>
        <li><b>Rentabilidad Asumida:</b> {contexto['rentabilidad']*100:.1f}%</li>
        <li><b>Inflación Asumida:</b> {contexto['inflacion']:.1f}%</li>
        <li><b>Capital Necesario Total:</b> {contexto['capital_necesario']:,.0f} €</li>
    </ul>

    <h2>Tabla de Amortización/Ahorro</h2>
    <table>
        <tr><th>Periodo</th><th>Aportación</th><th>Total</th><th>Inflación</th><th>Neto</th></tr>
        {tabla_mensual_y_anual_html(contexto['evolucion'], contexto['anos_hasta_jub'])}
    </table>
    </body>
    </html>
    """
    return html

# ============================================
#   FILA — GENERAR + DESCARGAR (SOLUCIÓN COLUMNAS)
# ============================================

col_gen, col_desc = st.columns([1, 1], gap="medium")

# --- COLUMNA IZQUIERDA: DATOS ---
with col_gen:
    st.markdown('<div class="srg-title">Generar informe</div>', unsafe_allow_html=True)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            tipo_informe = st.radio("Tipo", ["Cliente", "Agente"])
        with c2:
            nombre_cliente = st.text_input("Nombre", "Cliente SRG")
            email_cliente = st.text_input("Email", "")
            telefono_cliente = st.text_input("Teléfono", "")

# PREPARAR CONTEXTO
contexto_pdf = {
    "edad_actual": edad_actual, "edad_prevista_jub": edad_prevista_jub,
    "anos_cotizados_hoy": anos_cotizados_hoy, "anos_futuros": anos_futuros,
    "tipo_jubilacion": tipo_jubilacion, "pension_futura": pension_futura,
    "coef_ajuste": coef_ajuste, "objetivo_futuro": objetivo_futuro,
    "gastos_futuros": gastos_futuros, "brecha": brecha,
    "capital_necesario": capital_necesario, "aportacion": aportacion,
    "rentabilidad": rentabilidad, "inflacion": inflacion,
    "anos_hasta_jub": anos_hasta_jub, "anos_jubilacion": anos_jubilacion,
    "evolucion": evolucion, "nombre_cliente": nombre_cliente,
    "email_cliente": email_cliente, "telefono_cliente": telefono_cliente
}

if tipo_informe == "Cliente":
    html_out = informe_cliente(contexto_pdf, fig)
else:
    html_out = informe_agente(contexto_pdf, fig)
bytes_informe = html_out.encode("utf-8")

# --- COLUMNA DERECHA: DESCARGA ---
with col_desc:
    st.markdown('<div class="srg-title">Descargar informe</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("### Resultados clave")
        cd1, cd2 = st.columns(2)
        with cd1:
            st.caption("Pensión")
            st.write(f"**{pension_futura:,.0f} €**")
        with cd2:
            st.caption("Aportación")
            st.write(f"**{aportacion:,.0f} €**")
        
        st.divider()
        st.download_button(
            label="📄 Descargar Informe HTML",
            data=bytes_informe,
            file_name=f"Informe_{tipo_informe}.html",
            mime="text/html",
            use_container_width=True
        )

# ============================
#   FOOTER
# ============================
footer_html = """
<div class="srg-footer">
    <div><b>Simulador SRG — Samuel Ruiz González </b></div>
    <div>Herramienta educativa y formativa.</div>
    <div>© 2025 Samuel Ruiz González</div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
