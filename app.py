# ============================================
#   FILA — GENERAR INFORME + DESCARGAR INFORME
# ============================================

col_gen, col_desc = st.columns([1, 1])

with col_gen:
    st.subheader("Generar informe SRG")

    tipo_informe = st.radio(
        "Selecciona el tipo de informe:",
        ["Cliente", "Agente"],
        horizontal=True
    )

    with st.expander("Datos del cliente"):
        nombre_cliente = st.text_input("Nombre del cliente")
        email_cliente = st.text_input("Email del cliente")
        telefono_cliente = st.text_input("Teléfono del cliente")

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

with col_desc:
    st.subheader("Descargar informe SRG")

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

# ============================================
#   VISTA PREVIA DEL INFORME (igual que local)
# ============================================

st.subheader("Vista previa del informe")
st.components.v1.html(html_informe, height=900, scrolling=True)

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
