import streamlit as st

st.title("Test Reactividad SRG")

edad_actual = st.number_input("Edad actual", 18, 70, 40)
edad_jub = st.number_input("Edad jubilación", 60, 75, 67)

anos_hasta_jub = edad_jub - edad_actual
st.write(f"Años hasta jubilación: {anos_hasta_jub}")

base = st.number_input("Base reguladora (€)", 0, 50000, 2000)
cotizados = st.number_input("Años cotizados", 0, 50, 20)

pct = min(1.0, cotizados / 37)
pension = base * pct

st.metric("Porcentaje", f"{pct*100:.1f} %")
st.metric("Pensión estimada", f"{pension:,.0f} €")
