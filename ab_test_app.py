import streamlit as st

from sample_size import (
    ABSOLUTE,
    RELATIVE,
    binary_sample_size,
    continuous_sample_size,
    treatment_rate,
)

BINARY = "Binária (ex: conversão)"
CONTINUOUS = "Contínua (ex: receita por usuário)"
EFFECT_LABELS = {
    ABSOLUTE: "Absoluto (pontos percentuais)",
    RELATIVE: "Relativo (% da taxa de controle)",
}


def format_int(value):
    return f"{value:,}".replace(",", ".")


st.title("Calculadora de Tamanho de Amostra para Testes A/B")
st.caption("Teste bilateral com dois grupos independentes e alocação 1:1.")

# Tipo de métrica
metric_type = st.selectbox("Tipo de métrica a ser medida", [BINARY, CONTINUOUS])

if metric_type == BINARY:
    control_rate = st.number_input("Taxa de conversão do grupo de controle (%)", value=10.0)
    effect_type = st.selectbox(
        "Tipo de efeito mínimo detectável", [ABSOLUTE, RELATIVE], format_func=EFFECT_LABELS.get
    )
    if effect_type == ABSOLUTE:
        mde = st.number_input("Efeito mínimo detectável (pontos percentuais)", value=2.0)
    else:
        mde = st.number_input("Efeito mínimo detectável relativo (%)", value=20.0)
else:
    std_dev = st.number_input("Desvio padrão estimado da métrica", value=5.0)
    mde = st.number_input("Diferença mínima detectável (valor absoluto, na unidade da métrica)", value=1.0)

confidence_level = st.slider("Nível de confiança (%)", min_value=80, max_value=99, value=95)
power = st.slider("Poder estatístico (%)", min_value=80, max_value=99, value=80)

st.markdown("---")
st.subheader("Resultado")

try:
    if metric_type == BINARY:
        expected_rate = treatment_rate(control_rate, mde, effect_type)
        per_group = binary_sample_size(control_rate, mde, effect_type, confidence_level, power)
    else:
        per_group = continuous_sample_size(std_dev, mde, confidence_level, power)
except ValueError as error:
    st.error(str(error))
    st.stop()

if metric_type == BINARY:
    st.write(f"Taxa esperada no grupo de tratamento: **{expected_rate:.2f}%**".replace(".", ","))

col_group, col_total = st.columns(2)
col_group.metric("Amostra por grupo", format_int(per_group))
col_total.metric("Amostra total (2 grupos)", format_int(2 * per_group))
