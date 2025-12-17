import streamlit as st

st.set_page_config(page_title="Simulador de Jubilación", layout="centered")

st.title("📊 Simulador de Jubilación")
st.caption("Herramienta orientativa para análisis de previsión social")

# -----------------------
# ENTRADA DE DATOS
# -----------------------
st.sidebar.header("Datos del cliente")

anio_nacimiento = st.sidebar.number_input(
    "Año de nacimiento", min_value=1940, max_value=2005, value=1978
)

edad_jubilacion = st.sidebar.slider(
    "Edad de jubilación prevista", min_value=63, max_value=67, value=67
)

anos_cotizados = st.sidebar.slider(
    "Años cotizados", min_value=0.0, max_value=45.0, value=15.0, step=0.5
)

base_media = st.sidebar.number_input(
    "Base media de cotización (€)", min_value=800, max_value=6000, value=3000
)

tipo_jubilacion = st.sidebar.selectbox(
    "Tipo de jubilación",
    ["Ordinaria", "Anticipada voluntaria", "Anticipada involuntaria"]
)

# -----------------------
# CÁLCULOS
# -----------------------
# Base reguladora
base_reguladora = (base_media * 300) / 350

# Porcentaje por años cotizados
if anos_cotizados < 15:
    porcentaje = 0
elif anos_cotizados >= 36.5:
    porcentaje = 1
else:
    porcentaje = 0.5 + (anos_cotizados - 15) * (0.5 / 21.5)

pension_teorica = base_reguladora * porcentaje

# Penalización si es anticipada (simplificada)
penalizacion = 0
if tipo_jubilacion != "Ordinaria":
    if anos_cotizados < 38:
        penalizacion = 0.15
    else:
        penalizacion = 0.10

pension_final = pension_teorica * (1 - penalizacion)

# -----------------------
# RESULTADOS
# -----------------------
st.subheader("📌 Resultados estimados")

col1, col2 = st.columns(2)

col1.metric("Base reguladora", f"{base_reguladora:,.2f} €")
col2.metric("Porcentaje aplicable", f"{porcentaje*100:.2f} %")

st.metric("Pensión mensual estimada", f"{pension_final:,.2f} €")
st.metric("Pensión anual (14 pagas)", f"{pension_final*14:,.2f} €")

if penalizacion > 0:
    st.warning(f"⚠️ Se aplica una penalización aproximada del {penalizacion*100:.0f}% por jubilación anticipada")

# -----------------------
# SIMULACIÓN COMERCIAL
# -----------------------
st.subheader("📈 Simulación de mejora")

anos_extra = st.slider(
    "¿Y si cotizara algunos años más?",
    min_value=0.0, max_value=10.0, value=5.0, step=0.5
)

nuevos_anos = min(anos_cotizados + anos_extra, 36.5)

if nuevos_anos >= 36.5:
    nuevo_porcentaje = 1
else:
    nuevo_porcentaje = 0.5 + (nuevos_anos - 15) * (0.5 / 21.5)

nueva_pension = base_reguladora * nuevo_porcentaje

incremento = nueva_pension - pension_final

st.success(f"💶 Pensión con {nuevos_anos} años cotizados: {nueva_pension:,.2f} € / mes")
st.info(f"📊 Mejora mensual: +{incremento:,.2f} €")
st.info(f"📊 Mejora anual: +{incremento*14:,.2f} €")

# -----------------------
# AVISO LEGAL
# -----------------------
st.caption(
    "⚠️ Simulación orientativa. No constituye cálculo oficial de la Seguridad Social."
)

