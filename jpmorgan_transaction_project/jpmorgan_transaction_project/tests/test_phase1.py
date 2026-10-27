import unittest
import numpy as np
from main import select_threshold, generate_data

class ThresholdTests(unittest.TestCase):
    def test_known_optimum(self):
        table, chosen = select_threshold([False, True, False, True], [0.1, 0.9, 0.3, 0.8])
        self.assertEqual(chosen['threshold'], 0.8)
        self.assertEqual(chosen['f1'], 1.0)
        self.assertEqual(chosen['alerts'], 2)
        self.assertEqual(table.iloc[-1]['alerts'], 0)

    def test_equal_scores_are_not_split(self):
        _, chosen = select_threshold([True, False], [0.5, 0.5])
        self.assertEqual(chosen['alerts'], 2)
        self.assertAlmostEqual(chosen['precision'], 0.5)

    def test_missing_validation_positives(self):
        with self.assertRaises(ValueError):
            select_threshold([False], [0.5])

    def test_nonfinite_scores(self):
        with self.assertRaises(ValueError):
            select_threshold([True], [np.nan])

    def test_chronological_periods(self):
        data = generate_data().dropna(subset=['amount'])
        train = data[data.date < '2026-09-15']
        validation = data[(data.date >= '2026-09-15') & (data.date < '2026-09-21')]
        test = data[data.date >= '2026-09-21']
        self.assertLess(train.date.max(), validation.date.min())
        self.assertLess(validation.date.max(), test.date.min())
        self.assertEqual(len(train) + len(validation) + len(test), len(data))
        self.assertGreater(validation.is_injected_anomaly.sum(), 0)

if __name__ == '__main__':
    unittest.main()
