import streamlit as st
from scipy.stats import norm
import math

st.title("Calculadora de Tamanho de Amostra para Teste A/B")

control_rate = st.number_input("Taxa de conversão do grupo de controle (%)", min_value=0.0, max_value=100.0, value=10.0) / 100
mde = st.number_input("Efeito mínimo detectável (%)", min_value=0.1, max_value=50.0, value=2.0)
effect_type = st.selectbox("Tipo de efeito", ["absoluto", "relativo"])
confidence = st.slider("Intervalo de confiança (%)", 80, 99, 95)
power = st.slider("Poder estatístico (%)", 80, 99, 80)

alpha = 1 - confidence / 100
z_alpha = norm.ppf(1 - alpha / 2)
z_beta = norm.ppf(power / 100)

if effect_type == "absoluto":
    treatment_rate = control_rate + mde / 100
else:
    treatment_rate = control_rate * (1 + mde / 100)

pooled_prob = (control_rate + treatment_rate) / 2
sample_size = ((z_alpha + z_beta) ** 2 * 2 * pooled_prob * (1 - pooled_prob)) / ((treatment_rate - control_rate) ** 2)
sample_size = math.ceil(sample_size)

st.markdown("---")
st.write(f"📊 Tamanho mínimo de amostra por grupo: **{sample_size}** participantes")
