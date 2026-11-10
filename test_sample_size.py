import math
import unittest

from sample_size import (
    ABSOLUTE,
    RELATIVE,
    binary_sample_size,
    continuous_sample_size,
    treatment_rate,
)


class ContinuousMetricTest(unittest.TestCase):
    def test_reference_example(self):
        # 2 * ((1.95996 + 0.84162) * 5 / 1) ** 2 = 392.44 -> 393
        self.assertEqual(continuous_sample_size(std_dev=5, mde=1, confidence_level=95, power=80), 393)


class BinaryMetricTest(unittest.TestCase):
    def test_absolute_and_relative_mde_give_same_treatment_rate(self):
        self.assertAlmostEqual(treatment_rate(10, 2, ABSOLUTE), 12)
        self.assertAlmostEqual(treatment_rate(10, 20, RELATIVE), 12)

    def test_absolute_and_relative_mde_give_same_sample_size(self):
        absolute = binary_sample_size(10, 2, ABSOLUTE, confidence_level=95, power=80)
        relative = binary_sample_size(10, 20, RELATIVE, confidence_level=95, power=80)
        self.assertEqual(absolute, relative)
        # Valor da fórmula aproximada já existente, fixado contra regressões.
        self.assertEqual(absolute, 3843)


class InvalidInputTest(unittest.TestCase):
    def test_non_positive_mde(self):
        for mde in (0, -1, math.nan):
            with self.subTest(mde=mde):
                with self.assertRaisesRegex(ValueError, "efeito mínimo detectável deve ser maior que zero"):
                    continuous_sample_size(std_dev=5, mde=mde)
                for effect_type in (ABSOLUTE, RELATIVE):
                    with self.assertRaisesRegex(ValueError, "efeito mínimo detectável deve ser maior que zero"):
                        binary_sample_size(10, mde, effect_type)

    def test_invalid_std_dev(self):
        for std_dev in (0, -5, math.nan, math.inf):
            with self.subTest(std_dev=std_dev):
                with self.assertRaisesRegex(ValueError, "desvio padrão deve ser maior que zero"):
                    continuous_sample_size(std_dev=std_dev, mde=1)

    def test_control_rate_outside_open_interval(self):
        for control_rate in (0, 100, -1, 150, math.nan):
            with self.subTest(control_rate=control_rate):
                with self.assertRaisesRegex(ValueError, "taxa de controle deve estar entre 0% e 100%"):
                    binary_sample_size(control_rate, 2, ABSOLUTE)

    def test_treatment_rate_outside_open_interval(self):
        cases = [
            (95, 10, ABSOLUTE),  # 105%
            (90, 10, ABSOLUTE),  # exatamente 100%
            (90, 20, RELATIVE),  # 108%
        ]
        for control_rate, mde, effect_type in cases:
            with self.subTest(control_rate=control_rate, mde=mde, effect_type=effect_type):
                with self.assertRaisesRegex(ValueError, "taxa esperada no tratamento .* deve estar entre 0% e 100%"):
                    binary_sample_size(control_rate, mde, effect_type)

    def test_unknown_effect_type(self):
        with self.assertRaisesRegex(ValueError, "Tipo de efeito desconhecido"):
            binary_sample_size(10, 2, "outro")

    def test_confidence_and_power_outside_open_interval(self):
        with self.assertRaisesRegex(ValueError, "nível de confiança"):
            continuous_sample_size(5, 1, confidence_level=100)
        with self.assertRaisesRegex(ValueError, "poder estatístico"):
            continuous_sample_size(5, 1, power=0)


if __name__ == "__main__":
    unittest.main()
