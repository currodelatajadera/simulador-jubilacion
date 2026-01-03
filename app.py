
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
