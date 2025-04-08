import streamlit as st
from scipy.stats import norm
import math

st.title("Calculadora de Tamanho de Amostra para Testes A/B")

# Tipo de métrica
metric_type = st.selectbox("Tipo de métrica a ser medida", ["Binária (ex: conversão)", "Contínua (ex: receita por usuário)"])

if metric_type == "Binária (ex: conversão)":
    control_rate = st.number_input("Taxa de conversão do grupo de controle (%)", min_value=0.0, max_value=100.0, value=10.0) / 100
    mde_input = st.number_input("Efeito mínimo detectável (%)", min_value=0.0, value=2.0)
    effect_type = st.selectbox("Tipo de efeito mínimo detectável", ["absoluto", "relativo"])
else:
    mean = st.number_input("Média esperada da métrica (ex: R$ por usuário)", min_value=0.0, value=10.0)
    stddev = st.number_input("Desvio padrão estimado da métrica", min_value=0.01, value=5.0)
    mde_input = st.number_input("Diferença mínima detectável (valor absoluto)", min_value=0.01, value=1.0)

confidence_level = st.slider("Intervalo de confiança (%)", min_value=80, max_value=99, value=95)
power = st.slider("Poder estatístico (%)", min_value=80, max_value=99, value=80)

# Cálculo dos parâmetros z
alpha = 1 - confidence_level / 100
z_alpha = norm.ppf(1 - alpha / 2)
z_beta = norm.ppf(power / 100)

st.markdown("---")
st.subheader("Resultado")

if metric_type == "Binária (ex: conversão)":
    if effect_type == "absoluto":
        treatment_rate = control_rate + mde_input / 100
    else:  # relativo
        treatment_rate = control_rate * (1 + mde_input / 100)

    pooled_prob = (control_rate + treatment_rate) / 2
    sample_size = ((z_alpha + z_beta) ** 2 * (pooled_prob * (1 - pooled_prob) * 2)) / ((treatment_rate - control_rate) ** 2)
    sample_size = math.ceil(sample_size)

    st.write(f"Tamanho mínimo de amostra por grupo: **{sample_size}** participantes")

else:
    delta = mde_input  # diferença mínima detectável (absoluta)
    sample_size = ((z_alpha + z_beta) * stddev / delta) ** 2
    sample_size = math.ceil(sample_size)

    st.write(f"Tamanho mínimo de amostra por grupo: **{sample_size}** participantes")
