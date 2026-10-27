import tempfile
import unittest
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from sklearn.preprocessing import StandardScaler
from phase2 import prior_features
from phase4 import (synthetic_period, make_model, metrics_for,
                    choose_validation_threshold, select_algorithm, summarize)

class RobustnessTests(unittest.TestCase):
    def test_dashboard_ignores_incomplete_experiment(self):
        from dashboard_data import load_robustness
        with tempfile.TemporaryDirectory() as folder:
            incomplete = Path(folder)/'outputs'/'phase4'/'incomplete'
            incomplete.mkdir(parents=True)
            (incomplete/'protocol.json').write_text('{}')
            self.assertIsNone(load_robustness(folder))

    def test_generator_reproducible_and_periods_disjoint(self):
        development = synthetic_period(123, 'large_spikes', 200, '2026-09-01', 20)
        assert_frame_equal(development, synthetic_period(123, 'large_spikes', 200, '2026-09-01', 20))
        future = synthetic_period(999, 'large_spikes', 100, '2026-10-01', 10, 200)
        self.assertLess(development.date.max(), future.date.min())
        self.assertTrue(set(development.transaction_id).isdisjoint(future.transaction_id))
        self.assertEqual(int(development.is_injected_anomaly.sum()), 3)
        self.assertEqual(int(development.amount.isna().sum()), 1)

    def test_scenarios_change_only_injected_amounts(self):
        a = synthetic_period(123, 'large_spikes', 200, '2026-09-01', 20)
        b = synthetic_period(123, 'small_amounts', 200, '2026-09-01', 20)
        assert_frame_equal(a.loc[~a.is_injected_anomaly], b.loc[~b.is_injected_anomaly])
        self.assertTrue((a.loc[a.is_injected_anomaly, 'amount'] > b.loc[b.is_injected_anomaly, 'amount']).all())

    def test_no_positive_fallback_is_predeclared_quantile(self):
        scores = np.array([0.1, 0.2, 0.4])
        _, threshold, rule = choose_validation_threshold([False]*3, scores)
        self.assertAlmostEqual(threshold, np.quantile(scores, 0.97))
        self.assertIn('no_positives', rule)

    def test_undefined_metrics_and_confusion_accounting(self):
        metrics = metrics_for([False, True, False], [0.1, 0.3, 0.2], 0.5)
        self.assertFalse(metrics['precision_defined'])
        self.assertTrue(metrics['recall_defined'])
        self.assertEqual(metrics['false_negatives'], 1)
        self.assertEqual(metrics['true_negatives'], 2)
        self.assertEqual(metrics['alerts'], 0)

    def test_validation_selection_and_sample_variation(self):
        results = pd.DataFrame({'model': ['a','a','b','b'], 'f1': [0.8,1.,0.7,0.9],
            'precision': [0.8,1.,0.7,0.9], 'recall':[0.8,1.,0.7,0.9], 'alerts':[2,4,2,2]})
        self.assertEqual(select_algorithm(results), 'a')
        summary = summarize(results, ['model']).set_index('model')
        self.assertAlmostEqual(summary.loc['a', 'f1_mean'], 0.9)
        self.assertAlmostEqual(summary.loc['a', 'alerts_std'], np.sqrt(2))

    def test_training_only_scaling_and_frozen_model_roundtrip(self):
        data = synthetic_period(321, 'moderate_spikes', 200, '2026-09-01', 20).dropna(subset=['amount'])
        features = prior_features(data)
        columns = ['log_amount','amount_vs_prior_avg']
        train = data.date < '2026-09-15'
        scaler = StandardScaler().fit(features.loc[train, columns])
        np.testing.assert_allclose(scaler.mean_, features.loc[train, columns].mean())
        self.assertEqual(scaler.n_samples_seen_, int(train.sum()))
        x_train = scaler.transform(features.loc[train, columns])
        x_validation = scaler.transform(features.loc[~train, columns])
        for name in ['isolation_forest', 'local_outlier_factor']:
            model = make_model(name, 321).fit(x_train)
            scores = model.decision_function(x_validation)
            self.assertTrue(np.isfinite(scores).all())
            if name == 'local_outlier_factor':
                self.assertTrue(model.novelty)
            with tempfile.TemporaryDirectory() as folder:
                target = Path(folder)/'trusted_test.joblib'
                joblib.dump({'model':model, 'scaler':scaler}, target)
                restored = joblib.load(target)
                np.testing.assert_allclose(scores, restored['model'].decision_function(x_validation))

if __name__ == '__main__':
    unittest.main()
