"""Read saved experiment artifacts; no generation, fitting or scoring."""
import json
import hashlib
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent


def load_independent(root=ROOT):
    """Load the reviewed, portable snapshot and verify every exported byte."""
    folder = Path(root).resolve().parents[1]/'docs/results/stage5'
    manifest = json.loads((folder/'evidence_manifest.json').read_text(encoding='utf-8'))
    for name, info in manifest['files'].items():
        if Path(name).name != name:
            raise ValueError('Evidence filenames must be local basenames')
        if hashlib.sha256((folder/name).read_bytes()).hexdigest() != info['sha256']:
            raise ValueError(f'Evidence checksum mismatch: {name}')
    tables = {Path(name).stem: pd.read_csv(folder/name) for name in manifest['files'] if name.endswith('.csv')}
    documents = {Path(name).stem: json.loads((folder/name).read_text(encoding='utf-8'))
                 for name in manifest['files'] if name.endswith('.json')}
    return dict(manifest=manifest, tables=tables, documents=documents, folder=folder)


def read_csv(path):
    data = pd.read_csv(path)
    if 'date' in data:
        data['date'] = pd.to_datetime(data['date'], errors='raise')
    return data


def load_saved(root=ROOT):
    root = Path(root)
    one, two = root/'outputs/phase1', root/'outputs/phase2'
    phase2_metrics = json.loads((two/'evaluation_metrics.json').read_text())
    selected_name = phase2_metrics['selected_feature_set']
    return {
        'raw': read_csv(one/'synthetic_transactions.csv'),
        'cleaned': read_csv(one/'cleaned_transactions.csv'),
        'phase1_metrics': json.loads((one/'evaluation_metrics.json').read_text()),
        'phase2_metrics': phase2_metrics,
        'historical': read_csv(one/'anomaly_results.csv'),
        'validation': read_csv(two/f'{selected_name}_validation_results.csv'),
        'thresholds': read_csv(two/f'{selected_name}_thresholds.csv'),
        'comparison': read_csv(two/'feature_comparison.csv'),
        'development': read_csv(two/'development_features.csv'),
    }


def filter_transactions(data, categories, customer, start, end, amount_range):
    mask = data.merchant_category.isin(categories)
    if customer != 'All customers':
        mask &= data.customer_id == int(customer)
    mask &= data.date.between(pd.Timestamp(start), pd.Timestamp(end))
    mask &= data.amount.between(*amount_range)
    return data.loc[mask].copy()


def confusion_counts(data):
    actual, predicted = data.is_injected_anomaly.astype(bool), data.anomaly_flag.astype(bool)
    return [[int((~actual & ~predicted).sum()), int((~actual & predicted).sum())],
            [int((actual & ~predicted).sum()), int((actual & predicted).sum())]]


def load_robustness(root=ROOT):
    """Load only completed runs; partial experiments never appear as results."""
    base = Path(root)/'outputs'/'phase4'
    runs = sorted(path.parent for path in base.glob('*/evaluation_metrics.json'))
    if runs:
        latest = runs[-1]
        run_name = latest.name
        source = 'local experiment'
    else:
        # A hosted checkout has the compact recorded evidence, not ignored runs.
        latest = Path(root).resolve().parents[1]/'docs'/'results'
        if not (latest/'evaluation_metrics.json').is_file():
            return None
        run_name = 'recorded portfolio snapshot'
        source = 'committed synthetic evidence'
    return {'run': run_name, 'source': source,
        'metrics': json.loads((latest/'evaluation_metrics.json').read_text()),
        'freeze': json.loads((latest/'selection_freeze.json').read_text()),
        'summary': read_csv(latest/'future_summary.csv'),
        'validation': read_csv(latest/'validation_runs.csv'),
        'future': read_csv(latest/'future_runs.csv')}
