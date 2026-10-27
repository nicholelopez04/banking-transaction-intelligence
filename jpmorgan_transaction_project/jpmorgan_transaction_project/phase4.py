"""Frozen validation protocol and future synthetic robustness assessment."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from main import select_threshold
from phase2 import prior_features

ROOT = Path(__file__).resolve().parent
SEEDS = [11, 22, 33, 44, 55]
SCENARIOS = {'large_spikes': (15.0, 35.0), 'moderate_spikes': (3.0, 6.0),
             'small_amounts': (0.01, 0.08)}
MODELS = ['isolation_forest', 'local_outlier_factor']


def synthetic_period(seed, scenario, n, start, days, id_offset=0):
    """Scenario generator v1: baseline fields, independent period RNGs.

    Labels record deliberate perturbations, even if amounts overlap ordinary data.
    A 1.5% injection rate and 0.5% missing-amount rate are rounded to nearest integer.
    Missing amounts may overlap injections; both raw and usable counts are saved.
    """
    if scenario not in SCENARIOS or n < 1 or days < 1:
        raise ValueError('Unknown scenario or nonpositive period size')
    rng = np.random.default_rng(seed)
    customers = rng.integers(100, 150, n)
    amounts = rng.lognormal(4.0, 0.85, n)
    dates = pd.Timestamp(start) + pd.to_timedelta(rng.integers(0, days, n), unit='D')
    labels = np.zeros(n, dtype=bool)
    indices = rng.choice(n, size=int(round(n * 0.015)), replace=False)
    labels[indices] = True
    amounts[indices] *= rng.uniform(*SCENARIOS[scenario], len(indices))
    amounts = amounts.round(2)
    amounts[rng.choice(n, size=int(round(n * 0.005)), replace=False)] = np.nan
    return pd.DataFrame({'transaction_id': np.arange(id_offset + 1, id_offset + n + 1),
        'customer_id': customers, 'date': dates.strftime('%Y-%m-%d'), 'amount': amounts,
        'merchant_category': rng.choice(['groceries','travel','retail','utilities','restaurants'], n),
        'is_injected_anomaly': labels})


def make_model(name, seed):
    if name == 'isolation_forest':
        return IsolationForest(n_estimators=150, contamination=0.03, random_state=seed)
    if name == 'local_outlier_factor':
        return LocalOutlierFactor(n_neighbors=20, contamination=0.03, novelty=True)
    raise ValueError('Unknown detector')


def metrics_for(labels, scores, threshold):
    actual = np.asarray(labels, dtype=bool)
    predicted = np.asarray(scores) >= threshold
    tn, fp, fn, tp = confusion_matrix(actual, predicted, labels=[False, True]).ravel()
    return {'rows': len(actual), 'injections': int(actual.sum()), 'alerts': int(predicted.sum()),
        'precision': float(precision_score(actual, predicted, zero_division=0)),
        'precision_defined': bool(predicted.any()),
        'recall': float(recall_score(actual, predicted, zero_division=0)),
        'recall_defined': bool(actual.any()),
        'f1': float(f1_score(actual, predicted, zero_division=0)),
        'true_positives': int(tp), 'false_positives': int(fp),
        'false_negatives': int(fn), 'true_negatives': int(tn)}


def choose_validation_threshold(labels, scores):
    if np.asarray(labels, dtype=bool).any():
        table, chosen = select_threshold(labels, scores)
        return table, chosen['threshold'], 'maximum_validation_f1'
    # F1 cannot select a useful operating point without positives. Use a
    # predeclared validation-score quantile; do not drop inconvenient seeds.
    threshold = float(np.quantile(scores, 0.97))
    row = {'threshold': threshold, **metrics_for(labels, scores, threshold)}
    return pd.DataFrame([row]), threshold, 'fallback_validation_97th_percentile_no_positives'


def summarize(results, groups):
    # Sample SD across seeds, including zero_division=0 observations.
    columns = ['precision', 'recall', 'f1', 'alerts']
    summary = results.groupby(groups)[columns].agg(['mean', 'std', 'min', 'max'])
    summary.columns = ['_'.join(column) for column in summary.columns]
    return summary.reset_index()


def select_algorithm(validation):
    means = validation.groupby('model').agg(mean_f1=('f1','mean'), mean_alerts=('alerts','mean')).reset_index()
    return means.sort_values(['mean_f1','mean_alerts','model'], ascending=[False,True,True]).iloc[0]['model']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    # Each run gets its own directory; earlier assessment evidence is preserved.
    output = ROOT/'outputs'/'phase4'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output.mkdir(parents=True, exist_ok=False)
    feature_metadata = json.loads((ROOT/'outputs/phase2/evaluation_metrics.json').read_text())
    columns = feature_metadata['feature_columns']
    config = {'generator_version': 'scenario_period_v1', 'seeds': SEEDS,
        'scenarios': SCENARIOS, 'feature_columns': columns, 'models': MODELS,
        'development_rows': 1000, 'future_rows': 500,
        'train_start': '2026-09-01', 'train_end_exclusive': '2026-09-15',
        'validation_end_exclusive': '2026-09-21', 'future_start': '2026-10-01',
        'future_days': 10, 'future_seed_offset': 1000000,
        'threshold_selection': 'Maximum validation F1; fewer alerts; higher threshold. No positives: validation score quantile 0.97',
        'model_selection': 'Mean validation F1 across all fixed seeds/scenarios; fewer mean alerts; alphabetical model name',
        'history_policy': 'Strictly earlier dates, including earlier observed validation/future amounts, never labels',
        'precision_recall_undefined_convention': 'zero_division=0; defined flags saved',
        'python': platform.python_version(), 'sklearn': sklearn.__version__,
        'numpy': np.__version__, 'pandas': pd.__version__,
        'model_parameters': {name: make_model(name, SEEDS[0]).get_params() for name in MODELS},
        'source_sha256': {name: digest(ROOT/name) for name in ['main.py','phase2.py','phase4.py']}}
    (output/'protocol.json').write_text(json.dumps(config, indent=2), encoding='utf-8')
    validation_rows, experiments = [], []
    for scenario in SCENARIOS:
        for seed in SEEDS:
            case = output/f'{scenario}_{seed}'
            case.mkdir()
            raw = synthetic_period(seed, scenario, 1000, '2026-09-01', 20)
            raw.to_csv(case/'development_raw.csv', index=False)
            development = raw.dropna(subset=['amount']).copy()
            train = development.date < '2026-09-15'
            validation = ~train
            features = prior_features(development)
            scaler = StandardScaler()
            x_train = scaler.fit_transform(features.loc[train, columns])
            x_validation = scaler.transform(features.loc[validation, columns])
            for name in MODELS:
                model = make_model(name, seed)
                model.fit(x_train)
                scores = -model.decision_function(x_validation)
                labels = development.loc[validation, 'is_injected_anomaly']
                table, threshold, rule = choose_validation_threshold(labels, scores)
                table.to_csv(case/f'{name}_thresholds.csv', index=False)
                result = {'scenario': scenario, 'seed': seed, 'model': name,
                    'threshold': threshold, 'threshold_rule': rule,
                    'train_rows': int(train.sum()), **metrics_for(labels, scores, threshold)}
                validation_rows.append(result)
                predictions = development.loc[validation].copy()
                predictions['anomaly_score'] = scores
                predictions['anomaly_flag'] = scores >= threshold
                predictions.to_csv(case/f'{name}_validation.csv', index=False)
                joblib.dump({'model': model, 'scaler': scaler, 'threshold': threshold,
                             'feature_columns': columns}, case/f'{name}_frozen.joblib')
                experiments.append((scenario, seed, name, case, development, model, scaler, threshold))
            print(f'Validation complete: {scenario}, seed {seed}', flush=True)
    validation = pd.DataFrame(validation_rows)
    validation.to_csv(output/'validation_runs.csv', index=False)
    selected_model = select_algorithm(validation)
    frozen_paths = sorted(output.glob('*/*_frozen.joblib'))
    freeze = {'selected_model': selected_model, 'selected_from': 'validation only',
        'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'protocol_sha256': digest(output/'protocol.json'),
        'validation_sha256': digest(output/'validation_runs.csv'),
        'artifacts_sha256': {str(path.relative_to(output)): digest(path) for path in frozen_paths},
        'thresholds': validation[['scenario','seed','model','threshold','threshold_rule']].to_dict('records')}
    (output/'selection_freeze.json').write_text(json.dumps(freeze, indent=2), encoding='utf-8')
    print('FROZEN before future generation. Selected:', selected_model, flush=True)
    future_rows = []
    future_cache = {}
    for scenario, seed, name, case, development, model, scaler, threshold in experiments:
        key = (scenario, seed)
        if key not in future_cache:
            raw = synthetic_period(1000000 + seed, scenario, 500, '2026-10-01', 10, id_offset=1000)
            raw.to_csv(case/'future_raw.csv', index=False)
            future = raw.dropna(subset=['amount']).copy()
            combined = pd.concat([development, future], ignore_index=True)
            features = prior_features(combined)
            future_mask = combined.transaction_id > 1000
            x_future = scaler.transform(features.loc[future_mask, columns])
            future_cache[key] = (combined.loc[future_mask].copy(), x_future, raw)
        future, x_future, raw = future_cache[key]
        scores = -model.decision_function(x_future)
        result = {'scenario': scenario, 'seed': seed, 'future_seed': 1000000+seed,
            'model': name, 'selected_model': name == selected_model, 'threshold': threshold,
            'raw_injections': int(raw.is_injected_anomaly.sum()),
            'missing_rows': int(raw.amount.isna().sum()),
            **metrics_for(future.is_injected_anomaly, scores, threshold)}
        future_rows.append(result)
        predictions = future.copy()
        predictions['anomaly_score'] = scores
        predictions['anomaly_flag'] = scores >= threshold
        predictions.sort_values('anomaly_score', ascending=False).to_csv(case/f'{name}_future.csv', index=False)
    future_results = pd.DataFrame(future_rows)
    future_results.to_csv(output/'future_runs.csv', index=False)
    summary = summarize(future_results, ['scenario','model'])
    summary.to_csv(output/'future_summary.csv', index=False)
    summarize(validation, ['scenario','model']).to_csv(output/'validation_summary.csv', index=False)
    summarize(future_results, ['model']).to_csv(output/'future_overall_summary.csv', index=False)
    assert all(digest(output/path) == value for path, value in freeze['artifacts_sha256'].items())
    report = {'selected_model': selected_model, 'validation_runs': len(validation),
        'future_runs': len(future_results), 'future_generated_after_freeze': True,
        'notes': ['Both fixed candidates assessed once on fresh October synthetic periods.',
                  'No selection or retuning based on future assessment.',
                  'Summaries are sample SD across seeds, not confidence intervals.',
                  'Scenario runs share underlying customers/amounts and are not independent populations.',
                  'Known injection labels do not identify verified fraud; non-injected alerts can still be unusual.',
                  'Small synthetic samples do not establish real-world detection quality.'],
        'future_summary': summary.to_dict('records')}
    (output/'evaluation_metrics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(summary[['scenario','model','precision_mean','precision_std','recall_mean','recall_std','f1_mean','f1_std','alerts_mean','alerts_std']].to_string(index=False))
    print('Saved:', output)
    return output


if __name__ == '__main__':
    run()
