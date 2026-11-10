# A/B test sample size calculator

A small Streamlit app that estimates the minimum sample size for a two-sided A/B test with two independent groups and 1:1 allocation. It supports binary metrics (e.g. conversion) and continuous metrics (e.g. revenue per user). The interface is in Portuguese.

## Run

```bash
pip install -r requirements.txt
streamlit run ab_test_app.py
```

The calculations live in `sample_size.py` and are tested without Streamlit:

```bash
python -m unittest -v
```

## Example

At 95% confidence and 80% power:

| Metric | Inputs | Per group | Total |
| --- | --- | --- | --- |
| Continuous | standard deviation 5, MDE 1 (absolute) | 393 | 786 |
| Binary | baseline 10%, MDE 2 percentage points (same as 20% relative, so 12% in treatment) | 3,843 | 7,686 |

## Statistical assumptions

- Two-sided test, two independent groups of equal size; α = 1 − confidence level, power = 1 − β.
- Normal approximation: z_α = Φ⁻¹(1 − α/2), z_β = Φ⁻¹(power).
- Continuous metrics assume the same standard deviation σ in both groups: n per group = ⌈2 · ((z_α + z_β) · σ / δ)²⌉, where δ is the absolute MDE in the metric's unit.
- Binary metrics use an approximate formula with the average rate p̄ = (p₁ + p₂) / 2: n per group = ⌈(z_α + z_β)² · 2p̄(1 − p̄) / (p₂ − p₁)²⌉. An absolute MDE is in percentage points (p₂ = p₁ + MDE); a relative MDE is a percentage of the baseline (p₂ = p₁ · (1 + MDE)). Other textbook formulas can differ by a few units.
- Both rates must be strictly between 0% and 100%, and the MDE must be positive.
- No adjustment for multiple variants, multiple metrics, sequential peeking or clustered units.
