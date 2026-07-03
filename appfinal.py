import streamlit as st
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="Simulador Jubilación SRG", layout="wide")

# ============================================
#   ESTILOS SRG
# ============================================

st.markdown("""
<style>
    body, .stMarkdown {
        font-family: 'Montserrat', sans-serif;
    }
    .srg-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #003366;
        margin-bottom: 0.25rem;
    }
    .srg-box {
        border: 1px solid #d9d9d9;
        border-radius: 8px;
        padding: 0.75rem;
        background-color: #f9f9fb;
        margin-bottom: 0.5rem;
    }
    .srg-footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
        font-size: 0.8rem;
        color: #555;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
#   FUNCIONES AUXILIARES
# ============================================

def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


def tabla_mensual_y_anual_html(evolucion, inflacion_val):
    html = ""
    inflacion_mensual = inflacion_val / 100 / 12 if inflacion_val else 0
    aporte_prev = 0.0

    for i, total in enumerate(evolucion):
        mes = i + 1
        ano = (mes - 1) // 12 + 1
        if i == 0:
            aporte = total
        else:
            aporte = max(0.0, total - evolucion[i-1])
        aporte_prev += aporte
        factor_inflacion = (1 + inflacion_mensual) ** mes if inflacion_mensual > 0 else 1
        neto_real = total / factor_inflacion if factor_inflacion > 0 else total
        perdida = total - neto_real
        html += (
            f"<tr>"
            f"<td>{mes} / Año {ano}</td>"
            f"<td>{aporte:,.0f} €</td>"
            f"<td>{total:,.0f} €</td>"
            f"<td>{neto_real:,.0f} €</td>"
            f"<td>{perdida:,.0f} €</td>"
            f"</tr>"
        )
    return html


# ============================================
#   FILA 1 — DATOS PERSONALES Y ECONÓMICOS
# ============================================

st.markdown("## Datos personales y económicos")

col1, col2, col3, col4 = st.columns(4)

# -------- COLUMNA 1 — DATOS PERSONALES --------
with col1:
    st.markdown('<div class="srg-title">Datos personales</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    edad_actual = st.number_input(
        "Edad actual",
        min_value=0,
        max_value=100,
        value=None,
        placeholder="Ej: 45"
    )

    edad_prevista_jub = st.number_input(
        "Edad prevista de jubilación",
        min_value=0,
        max_value=100,
        value=None,
        placeholder="Ej: 67"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# -------- COLUMNA 2 — COTIZACIÓN --------
with col2:
    st.markdown('<div class="srg-title">Cotización</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    anos_totales = st.number_input(
        "Años cotizados",
        min_value=0.0,
        max_value=50.0,
        value=None,
        placeholder="Ej: 25"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# -------- COLUMNA 3 — TIPO DE JUBILACIÓN --------
with col3:
    st.markdown('<div class="srg-title">Tipo de jubilación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    modalidad = st.selectbox(
        "Modalidad",
        ["Ordinaria", "Anticipada", "Demorada"],
        index=None,
        placeholder="Elige una opción"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# -------- COLUMNA 4 — INGRESOS Y GASTOS --------
with col4:
    st.markdown('<div class="srg-title">Ingresos y gastos</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    ingresos_deseados = st.number_input(
        "Ingresos deseados hoy (€)",
        min_value=0.0,
        value=None,
        placeholder="Ej: 2000"
    )

    gastos_pct = st.slider(
        "Gastos que mantendrás en jubilación (%)",
        50, 100, 90
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ---- Cálculos base ----
try:
    anos_hasta_jub = int(edad_prevista_jub) - int(edad_actual)
    if anos_hasta_jub < 0:
        anos_hasta_jub = 0
except:
    anos_hasta_jub = 0

try:
    modo_valido = (
        modalidad == "Ordinaria" or
        (modalidad == "Anticipada" and anos_totales is not None and anos_totales >= 35) or
        (modalidad == "Demorada" and anos_totales is not None and anos_totales >= 15)
    )
except:
    modo_valido = False

# Coeficiente de ajuste según modalidad (B)
try:
    if modalidad == "Ordinaria":
        coef_ajuste = 1.0
    elif modalidad == "Anticipada":
        coef_ajuste = 0.9
    elif modalidad == "Demorada":
        coef_ajuste = 1.1
    else:
        coef_ajuste = 1.0
except:
    coef_ajuste = 1.0


# ============================================
#   FILA 2 — EXPLICACIÓN DETALLADA MODALIDAD
# ============================================

st.markdown("## Situación de jubilación")

with st.container():
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    if modalidad is None or edad_actual is None or edad_prevista_jub is None or anos_totales is None:
        st.info("Introduce tus datos para evaluar si cumples los requisitos de jubilación.")
        mensaje_modalidad = "A la espera de datos."
    else:
        if modo_valido:
            if modalidad == "Ordinaria":
                mensaje_modalidad = "Cumples los requisitos para la jubilación ordinaria."
            elif modalidad == "Anticipada":
                mensaje_modalidad = "Cumples los requisitos para la jubilación anticipada."
            else:
                mensaje_modalidad = "Cumples los requisitos para la jubilación demorada."
            st.success(mensaje_modalidad)
        else:
            mensaje_modalidad = "La modalidad seleccionada NO es válida según los años cotizados o la edad."
            st.warning(mensaje_modalidad)

    with st.expander("Explicación detallada"):
        st.markdown("""
- La **jubilación ordinaria** exige una edad mínima y un mínimo de años cotizados.
- La **jubilación anticipada** requiere más años de cotización y aplica coeficientes reductores.
- La **jubilación demorada** puede incrementar la pensión mediante coeficientes bonificados.

Esta simulación es orientativa y no sustituye al criterio oficial de la Seguridad Social.
""")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
#   FILA 3 — PENSIÓN, OBJETIVO Y BRECHA
# ============================================

st.markdown("## Pensión, objetivo y brecha")

colA, colB, colC, colD = st.columns(4)

# -------- COLUMNA A — PENSIÓN E INFLACIÓN --------
with colA:
    st.markdown('<div class="srg-title">Pensión e inflación</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    base = st.number_input(
        "Base reguladora (€)",
        min_value=0.0,
        max_value=50000.0,
        value=None,
        placeholder="Ej: 1500"
    )

    inflacion = st.number_input(
        "Inflación anual (%)",
        min_value=0.0,
        max_value=10.0,
        value=None,
        placeholder="Ej: 2.0"
    )

    reval = st.number_input(
        "Revalorización anual pensión (%)",
        min_value=0.0,
        max_value=5.0,
        value=None,
        placeholder="Ej: 1.5"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ---- Cálculo pensión ----
base_val = safe_float(base)
inflacion_val = safe_float(inflacion)
reval_val = safe_float(reval)

try:
    pct = min(1, anos_totales / 37) if modo_valido and anos_totales is not None else 0
except:
    pct = 0

pension_hoy = base_val * pct * coef_ajuste
pension_futura = pension_hoy * ((1 + reval_val/100) ** anos_hasta_jub)

# -------- COLUMNA B — RESUMEN PENSIÓN --------
with colB:
    st.markdown('<div class="srg-title">Resumen pensión</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    st.write(f"**Porcentaje sobre base:** {pct*100:,.1f} %")
    st.write(f"**Pensión ajustada hoy:** {pension_hoy:,.0f} €")
    st.write(f"**Pensión futura estimada:** {pension_futura:,.0f} €/mes")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- COLUMNA C — OBJETIVO ECONÓMICO --------
with colC:
    st.markdown('<div class="srg-title">Objetivo económico</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    try:
        objetivo_futuro = safe_float(ingresos_deseados) * ((1 + inflacion_val/100) ** anos_hasta_jub)
        gastos_futuros = safe_float(ingresos_deseados) * gastos_pct/100 * ((1 + inflacion_val/100) ** anos_hasta_jub)
    except:
        objetivo_futuro = 0.0
        gastos_futuros = 0.0

    st.metric("Objetivo mensual futuro", f"{objetivo_futuro:,.0f} €")
    st.metric("Gastos futuros estimados", f"{gastos_futuros:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- COLUMNA D — BRECHA (CON TOGGLE DENTRO) --------
with colD:
    st.markdown('<div class="srg-title">Brecha</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    modo_brecha = st.radio(
        "¿Qué quieres cubrir?",
        ["Objetivo económico", "Gastos reales"],
        horizontal=True
    )

    try:
        if modo_brecha == "Objetivo económico":
            brecha = objetivo_futuro - pension_futura
        else:
            brecha = gastos_futuros - pension_futura

        brecha = max(0, float(brecha))
    except:
        brecha = 0.0

    st.metric("Brecha mensual a cubrir", f"{brecha:,.0f} €")

    with st.expander("¿Qué es la brecha?"):
        st.markdown("""
La **brecha** es la diferencia entre lo que necesitarás cada mes en jubilación y la pensión pública futura estimada.

Representa **cuánto dinero faltaría cada mes** para mantener tu nivel de vida.
""")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
#   FILA 4 — PLAN DE AHORRO Y EVOLUCIÓN
# ============================================

st.markdown("## Plan de ahorro recomendado y evolución del capital")

colP1, colP2 = st.columns(2)

# -------- COLUMNA 1 — PLAN DE AHORRO --------
with colP1:
    st.markdown('<div class="srg-title">Plan de ahorro recomendado</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    rendimiento = st.number_input(
        "Rentabilidad anual esperada (%)",
        min_value=0.0,
        max_value=15.0,
        value=None,
        placeholder="Ej: 4.0"
    )

    incremento_aporte = st.number_input(
        "Incremento anual de aportaciones (%)",
        min_value=0.0,
        max_value=10.0,
        value=None,
        placeholder="Ej: 1.0"
    )

    r = safe_float(rendimiento) / 100 / 12
    inc = safe_float(incremento_aporte) / 100 / 12

    anos_jubilacion = 25
    meses_jub = anos_jubilacion * 12
    meses_hasta_jub = max(1, anos_hasta_jub * 12)

    brecha_val = safe_float(brecha)

    if r > 0:
        capital_necesario = brecha_val * (1 - (1 + r)**(-meses_jub)) / r
    else:
        capital_necesario = brecha_val * meses_jub

    try:
        if r > inc:
            aporte_mensual = capital_necesario * (r - inc) / ((1 + r)**meses_hasta_jub - (1 + inc)**meses_hasta_jub)
        else:
            aporte_mensual = capital_necesario / meses_hasta_jub
    except:
        aporte_mensual = 0.0

    aporte_mensual = max(0, aporte_mensual)

    st.metric("Aportación mensual necesaria", f"{aporte_mensual:,.0f} €")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- COLUMNA 2 — EVOLUCIÓN DEL CAPITAL --------
with colP2:
    st.markdown('<div class="srg-title">Evolución del capital</div>', unsafe_allow_html=True)
    st.markdown('<div class="srg-box">', unsafe_allow_html=True)

    evolucion = []
    if aporte_mensual == 0 or anos_hasta_jub <= 0:
        st.info("Introduce tus datos y calcula la brecha para ver la evolución del capital.")
    else:
        meses = anos_hasta_jub * 12
        total = 0.0
        aporte = aporte_mensual

        for m in range(meses):
            total = total * (1 + r) + aporte
            evolucion.append(total)
            if (m + 1) % 12 == 0:
                aporte *= (1 + inc)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(evolucion, color="#1f77b4", linewidth=2)
        ax.set_title("Evolución del capital acumulado", fontsize=14)
        ax.set_xlabel("Meses hasta la jubilación")
        ax.set_ylabel("Capital acumulado (€)")
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
#   FILA 5 — MODO AGENTE SRG
# ============================================

st.markdown("## Modo Agente SRG")

st.markdown('<div class="srg-title">Modo Agente SRG</div>', unsafe_allow_html=True)
with st.container(border=True):
    with st.expander("Guion comercial para explicar al cliente"):
        modo_agente = st.checkbox("Activar Modo Agente")
        if modo_agente:
            st.markdown(f"""
- **Situación actual:** {anos_totales if anos_totales is not None else 0} años cotizados. Jubilación prevista a los {edad_prevista_jub if edad_prevista_jub is not None else '-'} años.
- **Brecha detectada:** {brecha:,.0f} €/mes que no cubre la pensión pública.
- **Estrategia:** Crear un plan de ahorro que complete esa brecha en el tiempo.
- **Propuesta SRG:** Aportar **{aporte_mensual:,.0f} €/mes** con una rentabilidad objetivo del **{safe_float(rendimiento):.1f}% anual**.
""")

# ============================================
#   FILA 6 — RESUMEN EJECUTIVO
# ============================================

st.markdown("## Resumen ejecutivo")

st.markdown('<div class="srg-title">Resumen ejecutivo</div>', unsafe_allow_html=True)
with st.container(border=True):
    colR1, colR2, colR3, colR4 = st.columns(4)
    colR1.metric("Pensión futura", f"{pension_futura:,.0f} €")
    colR2.metric("Objetivo", f"{objetivo_futuro:,.0f} €")
    colR3.metric("Brecha", f"{brecha:,.0f} €")
    colR4.metric("Aportación mensual", f"{aporte_mensual:,.0f} €")


# ============================================
#   FILA 7 — GENERAR INFORME / DESCARGAR INFORME
# ============================================

def informe_cliente(contexto):
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
    <div class="metric-box"><b>Aportación Recomendada:</b> {contexto['aporte_mensual']:,.0f} €</div>

    <h2>Evolución del capital</h2>
    <table>
        <tr><th>Mes/Año</th><th>Aportación</th><th>Total</th><th>Neto Real</th><th>Pérdida por inflación</th></tr>
        {tabla_mensual_y_anual_html(contexto['evolucion'], contexto['inflacion_val'])}
    </table>
    </body>
    </html>
    """
    return html


def informe_agente(contexto):
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
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th {{ background: #444; color: white; padding: 5px; }}
        td {{ border: 1px solid #ccc; padding: 5px; }}
    </style>
    </head>
    <body>
    <h1>Informe Técnico (Agente)</h1>
    <p>Cliente: {contexto['nombre_cliente']} | Fecha: {fecha}</p>

    <h2>Datos Técnicos</h2>
    <ul>
        <li><b>Modalidad:</b> {contexto['modalidad']}</li>
        <li><b>Coeficiente Ajuste:</b> {contexto['coef_ajuste']:.3f}</li>
        <li><b>Rentabilidad Asumida:</b> {contexto['rendimiento']:.1f}%</li>
        <li><b>Inflación Asumida:</b> {contexto['inflacion']:,.1f}%</li>
        <li><b>Capital Necesario Total:</b> {contexto['capital_necesario']:,.0f} €</li>
    </ul>

    <h2>Tabla de ahorro</h2>
    <table>
        <tr><th>Periodo</th><th>Aportación</th><th>Total</th><th>Neto Real</th><th>Pérdida por inflación</th></tr>
        {tabla_mensual_y_anual_html(contexto['evolucion'], contexto['inflacion_val'])}
    </table>
    </body>
    </html>
    """
    return html


st.markdown("## Generar y descargar informe")

col_gen, col_desc = st.columns([1, 1], gap="medium")

# --- COLUMNA IZQUIERDA: GENERAR INFORME ---
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

if 'evolucion' not in locals() or evolucion is None:
    evolucion = []

contexto_pdf = {
    "edad_actual": edad_actual,
    "edad_prevista_jub": edad_prevista_jub,
    "anos_totales": anos_totales,
    "anos_hasta_jub": anos_hasta_jub,
    "modalidad": modalidad,
    "pension_futura": pension_futura,
    "coef_ajuste": coef_ajuste,
    "objetivo_futuro": objetivo_futuro,
    "gastos_futuros": gastos_futuros,
    "brecha": brecha,
    "capital_necesario": capital_necesario,
    "aporte_mensual": aporte_mensual,
    "rendimiento": safe_float(rendimiento),
    "inflacion": inflacion_val,
    "inflacion_val": inflacion_val,
    "evolucion": evolucion,
    "nombre_cliente": nombre_cliente,
    "email_cliente": email_cliente,
    "telefono_cliente": telefono_cliente
}

if tipo_informe == "Cliente":
    html_out = informe_cliente(contexto_pdf)
else:
    html_out = informe_agente(contexto_pdf)

bytes_informe = html_out.encode("utf-8")

# --- COLUMNA DERECHA: DESCARGAR INFORME ---
with col_desc:
    st.markdown('<div class="srg-title">Descargar informe</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("### Resultados clave")
        cd1, cd2 = st.columns(2)
        with cd1:
            st.caption("Pensión futura")
            st.write(f"**{pension_futura:,.0f} €**")
        with cd2:
            st.caption("Aportación mensual")
            st.write(f"**{aporte_mensual:,.0f} €**")

        st.divider()
        st.download_button(
            label="📄 Descargar Informe HTML",
            data=bytes_informe,
            file_name=f"Informe_{tipo_informe}.html",
            mime="text/html",
            use_container_width=True
        )


# ============================================
#   FOOTER SRG
# ============================================

footer_html = """
<div class="srg-footer">
    <div><b>Simulador SRG — Samuel Ruiz González</b></div>
    <div>Herramienta educativa y formativa.</div>
    <div>© 2025 Samuel Ruiz González</div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
