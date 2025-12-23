import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# CONFIGURACIÓN GENERAL
# -----------------------
st.set_page_config(
    page_title="Simulador Profesional de Jubilación",
    layout="wide"
)

# -----------------------
# TÍTULO
# -----------------------
st.markdown(
    """
    <h1 style='text-align:center;'>Simulador Profesional de Jubilación</h1>
    <p style='text-align:center; color:gray;'>Planificación financiera clara y realista</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -----------------------
# INPUTS PRINCIPALES
# -----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Datos personales")
    edad_actual = st.number_input("Edad actual", 18, 67, 45)
    edad_jubilacion = st.number_input("Edad de jubilación", 60, 70, 67)
    esperanza_vida = st.number_input("Esperanza de vida", 70, 100, 85)

with col2:
    st.subheader("Déficit en jubilación")
    deficit_mensual = st.number_input("Déficit mensual estimado (€)", 0, 5000, 600)
    inflacion = st.number_input("Inflación media anual (%)", 0.0, 5.0, 2.0, step=0.1)

with col3:
    st.subheader("Ahorro e inversión")
    aportacion_inicial = st.number_input("Aportación inicial (€)", 0, 500000, 20000)
    aportacion_mensual = st.number_input("Aportación mensual (€)", 0, 5000, 300)
    rentabilidad = st.number_input("Rentabilidad anual (%)", 0.0, 10.0, 5.0, step=0.1)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------
# BOTÓN CALCULAR
# -----------------------
calcular = st.button("Calcular simulación")

# -----------------------
# CÁLCULOS
# -----------------------
if calcular:
    años_ahorro = edad_jubilacion - edad_actual
    meses_ahorro = años_ahorro * 12
    años_cobro = esperanza_vida - edad_jubilacion
    meses_cobro = años_cobro * 12

    r_mensual = rentabilidad / 100 / 12

    capital = aportacion_inicial
    capitales = []

    for mes in range(meses_ahorro):
        capital = capital * (1 + r_mensual) + aportacion_mensual
        capitales.append(capital)

    # Consumo del capital en jubilación
    capital_jubilacion = capital
    capitales_post = []

    for mes in range(meses_cobro):
        capital_jubilacion = capital_jubilacion - deficit_mensual
        capitales_post.append(max(capital_jubilacion, 0))

    # -----------------------
    # GRÁFICA
    # -----------------------
    st.subheader("Evolución del capital")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(capitales, label="Fase de ahorro")
    ax.plot(
        range(len(capitales), len(capitales) + len(capitales_post)),
        capitales_post,
        label="Fase de jubilación"
    )

    ax.set_ylabel("€")
    ax.set_xlabel("Meses")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # -----------------------
    # TABLA RESUMEN
    # -----------------------
    st.subheader("Resumen numérico")

    resumen = pd.DataFrame({
        "Concepto": [
            "Edad actual",
            "Edad jubilación",
            "Esperanza de vida",
            "Capital acumulado al jubilarse",
            "Déficit mensual",
            "Años cubiertos con el capital"
        ],
        "Valor": [
            edad_actual,
            edad_jubilacion,
            esperanza_vida,
            f"{capital:,.0f} €",
            f"{deficit_mensual} €",
            round(capital / (deficit_mensual * 12), 1) if deficit_mensual > 0 else "∞"
        ]
    })

    st.table(resumen)
