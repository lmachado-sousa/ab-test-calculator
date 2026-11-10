"""Cálculo de tamanho de amostra para testes A/B, sem dependência do Streamlit.

Premissas: teste bilateral, dois grupos independentes, alocação 1:1 e
aproximação normal. Taxas, efeitos, confiança e poder são informados em
porcentagem (10 significa 10%).
"""
import math

from scipy.stats import norm

ABSOLUTE = "absoluto"  # MDE em pontos percentuais
RELATIVE = "relativo"  # MDE em % da taxa de controle


def _format_pct(value):
    return f"{value:.2f}".replace(".", ",") + "%"


def _check_open_percent(value, name):
    # A comparação encadeada também rejeita NaN.
    if not 0 < value < 100:
        raise ValueError(f"{name} deve estar entre 0% e 100%, sem incluir os extremos.")


def _check_mde(mde):
    if not (math.isfinite(mde) and mde > 0):
        raise ValueError("O efeito mínimo detectável deve ser maior que zero.")


def z_scores(confidence_level, power):
    """Retorna (z_alpha, z_beta) para um teste bilateral."""
    _check_open_percent(confidence_level, "O nível de confiança")
    _check_open_percent(power, "O poder estatístico")
    alpha = 1 - confidence_level / 100
    return norm.ppf(1 - alpha / 2), norm.ppf(power / 100)


def treatment_rate(control_rate, mde, effect_type):
    """Taxa esperada no grupo de tratamento, em %."""
    _check_open_percent(control_rate, "A taxa de controle")
    _check_mde(mde)
    if effect_type == ABSOLUTE:
        rate = control_rate + mde
    elif effect_type == RELATIVE:
        rate = control_rate * (1 + mde / 100)
    else:
        raise ValueError(f"Tipo de efeito desconhecido: {effect_type!r}.")
    if not 0 < rate < 100:
        raise ValueError(
            f"A taxa esperada no tratamento ({_format_pct(rate)}) deve estar entre 0% e 100%, "
            "sem incluir os extremos. Reduza o efeito mínimo detectável."
        )
    return rate


def binary_sample_size(control_rate, mde, effect_type, confidence_level=95, power=80):
    """Amostra por grupo para métrica binária (aproximação com a taxa média dos grupos)."""
    p1 = control_rate / 100
    p2 = treatment_rate(control_rate, mde, effect_type) / 100
    z_alpha, z_beta = z_scores(confidence_level, power)
    pooled = (p1 + p2) / 2
    return math.ceil((z_alpha + z_beta) ** 2 * 2 * pooled * (1 - pooled) / (p2 - p1) ** 2)


def continuous_sample_size(std_dev, mde, confidence_level=95, power=80):
    """Amostra por grupo para métrica contínua, com desvio padrão comum aos dois grupos.

    `mde` é a diferença absoluta entre as médias, na unidade da métrica.
    """
    if not (math.isfinite(std_dev) and std_dev > 0):
        raise ValueError("O desvio padrão deve ser maior que zero.")
    _check_mde(mde)
    z_alpha, z_beta = z_scores(confidence_level, power)
    return math.ceil(2 * ((z_alpha + z_beta) * std_dev / mde) ** 2)
