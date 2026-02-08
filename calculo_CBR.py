import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Analizador DCP", layout="wide")
st.title("📊 Calificador de Pavimentos (Ensayo DCP)")

# --- 1. ENTRADA DE DATOS ---
st.header("Inserte penetraciones por golpe (mm)")
col1, col2 = st.columns(2)
lecturas = []

for i in range(16):
    contenedor = col1 if i < 8 else col2
    # Usamos value para que coincida con tus datos de prueba si gustas
    valor = contenedor.number_input(f"Golpe {i}:", min_value=0.0, step=0.1, key=f"g{i}")
    lecturas.append(valor)

# --- 2. CÁLCULOS ---
if st.button("CALCULAR RESULTADOS"):
    altura_total = lecturas[15] - lecturas[0]
    
    lista_cbr = []
    tabla_detallada = []

    for n in range(1, 16):
        delta_dn = lecturas[n] - lecturas[n-1]
        delta_nn = 1
        dcpi = delta_dn / delta_nn
        
        # Fórmula CBR = 292 / (DCPI^1.12)
        cbr_i = 292 / (max(dcpi, 0.1) ** 1.12)
        lista_cbr.append(cbr_i)
        
        tabla_detallada.append({
            "Intervalo": f"Golpe {n-1} a {n}",
            "ΔDn (mm)": delta_dn,
            "ΔNn (golpes)": delta_nn,
            "DCPI (mm/golpe)": dcpi,
            "CBR (%)": round(cbr_i, 4)
        })

    # --- CORRECCIÓN ESTADÍSTICA ---
    cbr_promedio = np.mean(lista_cbr)
    # ddof=1 asegura que sea la desviación estándar muestral (7.028...)
    desviacion_std = np.std(lista_cbr, ddof=1)

    # --- 3. MOSTRAR RESULTADOS ---
    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.metric("Altura Total Penetración", f"{altura_total:.2f} mm")
    res2.metric("CBR Promedio", f"{cbr_promedio:.2f} %")
    res3.metric("Desviación Estándar", f"{desviacion_std:.7f}")

    st.subheader("Desglose por Golpe")
    st.table(pd.DataFrame(tabla_detallada))