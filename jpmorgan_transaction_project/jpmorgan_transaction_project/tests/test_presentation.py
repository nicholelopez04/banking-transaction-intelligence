"""Regression checks for evidence fidelity and preserved explorer interactions."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest
from dashboard_data import ROOT, load_independent
from dashboard_evaluation import display_table


class IndependentEvidenceTests(unittest.TestCase):
    def test_undefined_gates_display_as_na_without_changing_source(self):
        source = pd.DataFrame({'gate': [True, False, None], 'precision': [0.1, 0., None]})
        result = display_table(source, ['precision'], ['gate'])
        self.assertEqual(result.gate.tolist(), ['Pass', 'Fail', 'N/A'])
        self.assertEqual(result.precision.tolist(), ['10.000%', '0.000%', 'N/A'])
        self.assertTrue(pd.isna(source.gate.iloc[-1]))

    def test_portable_snapshot_and_metric_reconciliation(self):
        evidence = load_independent()
        cases = evidence['tables']['all_case_metrics']
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases[['scenario', 'seed']].drop_duplicates().shape[0], 40)
        self.assertEqual(set(cases.scenario), {f'S{i}' for i in range(1, 9)})
        for row in evidence['tables']['pooled_metrics'].itertuples():
            subset = cases[(cases.model == row.model) & (cases.policy == row.policy)]
            for key in ['TP', 'FP', 'FN', 'TN']:
                self.assertEqual(int(subset[key].sum()), getattr(row, key))
            self.assertEqual(row.reviews, row.TP + row.FP)
            self.assertAlmostEqual(row.precision, row.TP / row.reviews)
            self.assertAlmostEqual(row.recall, row.TP / (row.TP + row.FN))
            self.assertAlmostEqual(row.f1, 2*row.TP / (2*row.TP + row.FP + row.FN))
            if row.policy == 'equal_budget':
                self.assertEqual(row.reviews, 8000)
        controls = cases[(cases.scenario == 'S8') & (cases.policy == 'native')]
        self.assertTrue(controls.recall.isna().all())
        self.assertEqual(controls[controls.model == 'phase6_v1'].alerts.tolist(), [159,150,141,149,140])
        types = evidence['tables']['pooled_type_metrics'].query("model == 'phase6_v1' and policy == 'native'")
        self.assertEqual(types.TP.sum(), 462)
        self.assertEqual(types.loc[types.injection_type == 'inactivity_return', 'TP'].item(), 452)

    def test_hosted_snapshot_loads_without_full_research_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout = Path(folder)/'checkout'
            app = checkout/'project/app'
            app.mkdir(parents=True)
            target = checkout/'docs/results/stage5'
            shutil.copytree(load_independent()['folder'], target)
            self.assertEqual(load_independent(app)['manifest']['cases'], 40)
            with (target/'pooled_metrics.csv').open('a') as f:
                f.write('tampered')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                load_independent(app)


class PresentationInteractionTests(unittest.TestCase):
    def app(self):
        app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=45).run()
        self.assertFalse(app.exception)
        return app

    def test_landing_and_all_policies_remain_fixed_under_explorer_filters(self):
        app = self.app()
        self.assertEqual(app.tabs[0].label, 'Independent evaluation')
        self.assertTrue(any('Neither model met' in x.value for x in app.error))
        self.assertTrue(any('452 of 462' in x.value for x in app.warning))
        self.assertTrue(any('Model Selection Only — Two Injected Anomalies' in x.value for x in app.markdown))
        reviews = [m.value for m in app.tabs[0].metric if m.label == 'Reviews']
        self.assertEqual(reviews, ['83', '5,184', '8,000', '8,000'])
        app.sidebar.multiselect[0].set_value([]).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.tabs[0].metric if m.label == 'Reviews'], reviews)
        app.selectbox(key='independent_policy').select('equal_budget').run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.tabs[0].metric if m.label == 'Reviews'], reviews)

    def test_customer_rankings_and_historical_chart_controls(self):
        app = self.app()
        app.sidebar.selectbox[0].select('100').run()
        self.assertFalse(app.exception)
        self.assertEqual(next(m.value for m in app.metric if m.label == 'Transactions'), '18')
        app.checkbox[0].check().run()
        self.assertFalse(app.exception)
        app.selectbox(key='robustness_metric').select('f1').run()
        self.assertFalse(app.exception)
        app.select_slider[0].set_value(0).run()
        self.assertFalse(app.exception)


if __name__ == '__main__':
    unittest.main()
