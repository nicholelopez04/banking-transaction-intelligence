import tempfile
import unittest
from streamlit.testing.v1 import AppTest
from dashboard_data import ROOT, load_saved, filter_transactions, confusion_counts, load_robustness

class SavedDataTests(unittest.TestCase):
    def test_confusion_agrees_with_saved_metrics(self):
        saved = load_saved()
        m = saved['phase1_metrics']
        self.assertEqual(confusion_counts(saved['historical']),
            [[m['true_negatives'], m['false_positives']], [m['false_negatives'], m['true_positives']]])
        selected = next(x for x in saved['phase2_metrics']['results'] if x['feature_set'] == saved['phase2_metrics']['selected_feature_set'])
        self.assertEqual(int(saved['validation'].anomaly_flag.sum()), selected['alerts'])

    def test_empty_category_selection(self):
        data = load_saved()['cleaned']
        self.assertTrue(filter_transactions(data, [], 'All customers', data.date.min(), data.date.max(), (0, data.amount.max())).empty)

    def test_hosted_checkout_uses_recorded_robustness_without_local_runs(self):
        import shutil
        with tempfile.TemporaryDirectory() as folder:
            from pathlib import Path
            checkout = Path(folder)/'checkout'
            app = checkout/'project'/'application'
            app.mkdir(parents=True)
            evidence = checkout/'docs'/'results'
            evidence.mkdir(parents=True)
            original = ROOT.parents[1]/'docs'/'results'
            for name in ['evaluation_metrics.json','selection_freeze.json',
                         'future_summary.csv','validation_runs.csv','future_runs.csv']:
                shutil.copy2(original/name, evidence/name)
            result = load_robustness(app)
            self.assertEqual(result['source'], 'committed synthetic evidence')
            self.assertEqual(result['run'], 'recorded portfolio snapshot')
            self.assertEqual(len(result['future']), 30)
            self.assertEqual(result['freeze']['selected_model'], 'isolation_forest')

    def test_missing_artifact_raises(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                load_saved(folder)

class DashboardTests(unittest.TestCase):
    def app(self):
        app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=30).run()
        self.assertFalse(app.exception)
        return app

    def test_default_loads_saved_results(self):
        app = self.app()
        self.assertEqual(app.title[0].value, 'Transaction Intelligence')
        self.assertTrue(any('SYNTHETIC DATA ONLY' in x.value for x in app.warning))
        self.assertEqual(app.metric[0].value, f"{len(load_saved()['cleaned']):,}")

    def test_filters_empty_and_evaluation_stays_full_split(self):
        app = self.app()
        before = [m.value for m in app.metric][-4:]
        app.sidebar.multiselect[0].set_value([]).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, '0')
        self.assertEqual([m.value for m in app.metric][-4:], before)

    def test_historical_evaluation_and_alert_only_ranking(self):
        app = self.app()
        app.selectbox(key='evaluation_experiment').select_index(1).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric][-4:], ['N/A', '0.0%', '0.0%', '0'])
        app.selectbox(key='ranking_experiment').select_index(1).run()
        app.checkbox[0].check().run()
        self.assertFalse(app.exception)
        self.assertTrue(any('No scored transactions' in x.value for x in app.info))

    def test_threshold_exploration_keeps_saved_alert_count(self):
        app = self.app()
        before = [m.value for m in app.metric][-4:]
        app.select_slider[0].set_value(0).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric][-4:], before)

if __name__ == '__main__':
    unittest.main()
