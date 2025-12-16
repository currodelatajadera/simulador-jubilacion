import streamlit as st

st.set_page_config(page_title="Simulador de Jubilación", layout="wide")

st.title("Simulador de Jubilación – Uso Profesional")
st.markdown("Introduce los datos del cliente y pulsa **Simular**")

col1, col2 = st.columns(2)

with col1:
    st.header("Datos del cliente")
    anio_nacimiento = st.number_input("Año de nacimiento", min_value=1940, max_value=2007, value=1978)
    edad_jubilacion = st.number_input("Edad de jubilación", min_value=60, max_value=70, value=67)
    anios_cotizados = st.number_input("Años cotizados", min_value=0, max_value=45, value=15)
    base_media = st.number_input("Base media mensual (€)", min_value=500, max_value=6000, value=3000)
    tipo = st.selectbox("Tipo de jubilación", ["Ordinaria", "Anticipada"])

    simular = st.button("SIMULAR JUBILACIÓN")

with col2:
    st.header("Resultado estimado")
    if simular:
        base_reguladora = base_media * 12

        if anios_cotizados < 15:
            porcentaje = 0
        elif anios_cotizados < 36:
            porcentaje = 0.5
        else:
            porcentaje = 1

        pension_anual = base_reguladora * porcentaje
        pension_mensual = pension_anual / 14

        st.metric("Base reguladora anual (€)", f"{base_reguladora:,.0f}")
        st.metric("Porcentaje aplicado", f"{porcentaje*100:.0f} %")
        st.metric("Pensión mensual estimada (€)", f"{pension_mensual:,.0f}")

        brecha = base_media - pension_mensual
        st.metric("Brecha mensual (€)", f"{brecha:,.0f}")
    else:
        st.info("Introduce los datos y pulsa SIMULAR")

