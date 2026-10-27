import unittest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from phase2 import prior_features

class HistoryTests(unittest.TestCase):
    def data(self):
        return pd.DataFrame({'transaction_id': [1, 2, 3, 4, 5],
            'customer_id': [100, 100, 100, 100, 200],
            'date': ['2026-09-01', '2026-09-01', '2026-09-02', '2026-09-03', '2026-09-02'],
            'amount': [10., 30., 60., 100., 50.],
            'is_injected_anomaly': [False, True, False, False, True]})

    def test_exact_history_and_same_day_exclusion(self):
        features = prior_features(self.data())
        self.assertEqual(features.prior_count.tolist(), [0, 0, 2, 3, 0])
        self.assertAlmostEqual(features.loc[2, 'prior_avg'], 20.)
        self.assertAlmostEqual(features.loc[3, 'prior_avg'], 100/3)
        self.assertEqual(features.loc[2, 'amount_vs_prior_avg'], 3.)

    def test_future_and_same_day_changes_cannot_change_history(self):
        data = self.data()
        original = prior_features(data)
        data.loc[3, 'amount'] = 1e9
        changed = prior_features(data)
        assert_frame_equal(original.iloc[:3], changed.iloc[:3])
        data = self.data()
        data.loc[1, 'amount'] = 1e9
        changed = prior_features(data)
        assert_frame_equal(original.iloc[[0]], changed.iloc[[0]])

    def test_cold_start_uses_prior_global_only(self):
        features = prior_features(self.data())
        self.assertEqual(features.loc[0, 'prior_avg'], 1.)
        self.assertEqual(features.loc[4, 'prior_avg'], 20.)
        self.assertEqual(features.loc[4, 'amount_vs_prior_avg'], 1.)
        self.assertTrue(np.isfinite(features.to_numpy()).all())

    def test_labels_and_input_order_do_not_affect_features(self):
        data = self.data()
        original = prior_features(data).sort_values('transaction_id').reset_index(drop=True)
        data.is_injected_anomaly = ~data.is_injected_anomaly
        shuffled = prior_features(data.sample(frac=1, random_state=4)).sort_values('transaction_id').reset_index(drop=True)
        assert_frame_equal(original, shuffled)

    def test_future_append_invariance(self):
        data = self.data()
        original = prior_features(data)
        future = pd.DataFrame({'transaction_id': [6], 'customer_id': [100],
            'date': ['2026-10-01'], 'amount': [1e8], 'is_injected_anomaly': [True]})
        assert_frame_equal(original, prior_features(pd.concat([data, future], ignore_index=True)).iloc[:len(data)])

if __name__ == '__main__':
    unittest.main()
