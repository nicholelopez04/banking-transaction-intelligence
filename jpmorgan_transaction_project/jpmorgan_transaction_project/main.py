"""Synthetic banking transaction analysis and anomaly detection demo."""
from pathlib import Path
import json
import sqlite3
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent / 'outputs' / 'phase1'


def generate_data(n=1000, seed=42):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    # A local generator makes repeated calls reproducible, not just fresh runs.
    RNG = np.random.default_rng(seed)
    customer_id = RNG.integers(100, 150, n)
    amounts = np.round(RNG.lognormal(mean=4.0, sigma=0.85, size=n), 2)
    injected = RNG.choice(n, size=min(15, n), replace=False)
    amounts[injected] *= RNG.uniform(15, 35, len(injected))
    dates = pd.Timestamp('2026-09-01') + pd.to_timedelta(RNG.integers(0, 30, n), unit='D')
    df = pd.DataFrame({
        'transaction_id': np.arange(1, n + 1),
        'customer_id': customer_id,
        'date': dates.strftime('%Y-%m-%d'),
        'amount': amounts.round(2),
        'merchant_category': RNG.choice(['groceries', 'travel', 'retail', 'utilities', 'restaurants'], n),
    })
    # Synthetic evaluation label only; never used as a model feature.
    df['is_injected_anomaly'] = False
    df.loc[injected, 'is_injected_anomaly'] = True
    df.loc[RNG.choice(n, min(5, n), replace=False), 'amount'] = np.nan
    return df


def select_threshold(labels, scores):
    """Tune on validation injections only; larger scores mean more unusual."""
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=bool)
    if not len(scores) or len(scores) != len(labels) or not np.isfinite(scores).all():
        raise ValueError('Expected matching nonempty labels and finite scores')
    if not labels.any():
        raise ValueError('Validation must contain injected positives for F1 selection')
    thresholds = np.unique(np.append(scores, [0.0, np.nextafter(scores.max(), np.inf)]))
    rows = []
    for threshold in thresholds:
        predicted = scores >= threshold
        rows.append({'threshold': float(threshold), 'precision': float(precision_score(labels, predicted, zero_division=0)),
                     'recall': float(recall_score(labels, predicted, zero_division=0)),
                     'f1': float(f1_score(labels, predicted, zero_division=0)), 'alerts': int(predicted.sum())})
    table = pd.DataFrame(rows)
    selected = table.sort_values(['f1', 'alerts', 'threshold'], ascending=[False, True, False]).iloc[0].to_dict()
    selected['alerts'] = int(selected['alerts'])
    return table, selected


def write_threshold_plot(table, path):
    """Dependency-free SVG of validation metrics versus alert volume."""
    ordered = table.sort_values('alerts')
    maximum = max(int(ordered['alerts'].max()), 1)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="460" viewBox="0 0 900 460">',
             '<rect width="900" height="460" fill="white"/>',
             '<text x="60" y="28" font-size="20">Validation threshold comparison - synthetic injections</text>',
             '<path d="M60 60 V380 H840" fill="none" stroke="black"/>',
             '<text x="330" y="435">Alert count (threshold decreases to the right)</text>',
             '<text x="10" y="65">1.0</text><text x="10" y="385">0.0</text>']
    for i, (metric, color) in enumerate([('precision', '#2563eb'), ('recall', '#059669'), ('f1', '#d97706')]):
        points = ' '.join(f"{60 + 780 * row.alerts / maximum:.2f},{380 - 320 * getattr(row, metric):.2f}" for row in ordered.itertuples())
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        parts.append(f'<text x="{90 + 180*i}" y="55" fill="{color}">{metric}</text>')
    parts.append(f'<text x="60" y="405">0</text><text x="820" y="405">{maximum}</text></svg>')
    path.write_text(''.join(parts), encoding='utf-8')


def phase1_main():
    BASE.mkdir(parents=True, exist_ok=True)
    raw = generate_data()
    raw.to_csv(BASE / 'synthetic_transactions.csv', index=False)
    print('Raw rows:', len(raw), '| Missing amounts:', raw['amount'].isna().sum())

    # Preserve original records; exclude unknown amounts only from numeric analysis.
    cleaned = raw.dropna(subset=['amount']).copy()
    cleaned['date'] = pd.to_datetime(cleaned['date'], errors='raise')
    if cleaned['transaction_id'].duplicated().any():
        raise ValueError('Transaction IDs must be unique')
    if not np.isfinite(cleaned['amount']).all() or (cleaned['amount'] < 0).any():
        raise ValueError('This synthetic demo requires finite, nonnegative amounts')
    cleaned.to_csv(BASE / 'cleaned_transactions.csv', index=False)
    print('Cleaned rows:', len(cleaned), '| Total volume: $' + f"{cleaned['amount'].sum():,.2f}")

    # Prepare a chronological split for evaluating future transactions.
    cutoff = pd.Timestamp('2026-09-21')
    train = cleaned.loc[cleaned['date'] < pd.Timestamp('2026-09-15')].copy()
    validation = cleaned.loc[(cleaned['date'] >= pd.Timestamp('2026-09-15')) & (cleaned['date'] < cutoff)].copy()
    test = cleaned.loc[cleaned['date'] >= cutoff].copy()
    print('Training rows:', len(train), '| Validation rows:', len(validation), '| Historical test rows:', len(test))
    if train.empty or validation.empty or test.empty:
        raise ValueError('All chronological periods must contain usable transactions')

    from contextlib import closing
    with closing(sqlite3.connect(BASE / 'banking.db')) as con:
        cleaned.to_sql('transactions', con, if_exists='replace', index=False)
        query = '''
        SELECT customer_id, COUNT(*) AS transaction_count,
               ROUND(SUM(amount), 2) AS total_spent
        FROM transactions
        GROUP BY customer_id
        HAVING SUM(amount) > 2000
        ORDER BY total_spent DESC
        LIMIT 5
        '''
        top_customers = pd.read_sql_query(query, con)
    print('\nTop customers by transaction amount:')
    print(top_customers.to_string(index=False))
    top_customers.to_csv(BASE / 'top_customers.csv', index=False)

    # Unsupervised model: no fraud labels are available.
    features = cleaned[['amount']].copy()
    features['log_amount'] = np.log1p(features['amount'])
    # Use historical customer means, with a training-only fallback for new customers.
    customer_averages = train.groupby('customer_id')['amount'].mean()
    fallback_average = train['amount'].mean()
    features['customer_avg'] = cleaned['customer_id'].map(customer_averages).fillna(fallback_average)
    features['amount_vs_customer_avg'] = features['amount'] / features['customer_avg'].clip(lower=0.01)
    feature_columns = ['log_amount', 'amount_vs_customer_avg']
    scaler = StandardScaler()
    x_train = scaler.fit_transform(features.loc[train.index, feature_columns])
    x_validation = scaler.transform(features.loc[validation.index, feature_columns])
    model = IsolationForest(n_estimators=150, contamination=0.03, random_state=42)
    model.fit(x_train)
    validation_scores = -model.decision_function(x_validation)
    comparisons, selected = select_threshold(validation['is_injected_anomaly'], validation_scores)
    comparisons.to_csv(BASE / 'threshold_comparison.csv', index=False)
    write_threshold_plot(comparisons, BASE / 'threshold_comparison.svg')
    validation['anomaly_score'] = validation_scores
    validation['anomaly_flag'] = validation_scores >= selected['threshold']
    validation.to_csv(BASE / 'validation_results.csv', index=False)
    print('Validation-selected threshold:', selected['threshold'])
    print('Validation precision / recall / F1:', selected['precision'], selected['recall'], selected['f1'])
    # Only after threshold selection: score the historical test period once.
    x_test = scaler.transform(features.loc[test.index, feature_columns])
    test['anomaly_score'] = -model.decision_function(x_test)
    test['anomaly_flag'] = test['anomaly_score'] >= selected['threshold']
    ranked = test.sort_values('anomaly_score', ascending=False)
    ranked.to_csv(BASE / 'anomaly_results.csv', index=False)
    print('\nTest transactions flagged for review:', int(test['anomaly_flag'].sum()))
    # Evaluate later transactions that were excluded from fitting.
    actual = test['is_injected_anomaly']
    predicted = test['anomaly_flag']
    print('Injected anomalies in test data:', int(actual.sum()))
    print('Precision on synthetic injections:', f'{precision_score(actual, predicted, zero_division=0):.1%}')
    print('Recall on synthetic injections:', f'{recall_score(actual, predicted, zero_division=0):.1%}')
    tn, fp, fn, tp = confusion_matrix(actual, predicted, labels=[False, True]).ravel()
    metrics = {
        'train_rows': len(train), 'validation_rows': len(validation), 'test_rows': len(test),
        'selected_threshold': selected,
        'selection_rule': 'Maximum validation F1; ties: fewer alerts, then higher threshold',
        'feature_columns': feature_columns,
        'train_end_exclusive': '2026-09-15', 'validation_end_exclusive': '2026-09-21',
        'f1': float(f1_score(actual, predicted, zero_division=0)),
        'test_injected_anomalies': int(actual.sum()),
        'flagged': int(predicted.sum()),
        'true_positives': int(tp), 'false_positives': int(fp),
        'false_negatives': int(fn), 'true_negatives': int(tn),
        'precision': float(precision_score(actual, predicted, zero_division=0)),
        'recall': float(recall_score(actual, predicted, zero_division=0)),
        'precision_at_10': float(ranked.head(10)['is_injected_anomaly'].mean()),
        'evaluation': 'Validation-selected threshold on historical synthetic test period whose baseline results were previously inspected; reserve a fresh final period after feature/model selection' ,
    }
    (BASE / 'evaluation_metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print(f'TP: {tp} | FP: {fp} | FN: {fn} | TN: {tn}')
    print('Precision at 10 (entire test period):', f"{metrics['precision_at_10']:.1%}")
    print(ranked.loc[ranked['anomaly_flag'], ['transaction_id', 'customer_id', 'amount', 'anomaly_score']].head(10).to_string(index=False))
    print('\nOutputs saved in:', BASE)
    print('NOTE: Metrics evaluate held-out synthetic injections, not verified fraud or real-world performance.')


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['1', '2', '4'], default='2')
    args = parser.parse_args()
    if args.phase == '1':
        phase1_main()
    elif args.phase == '4':
        from phase4 import run
        run()
    else:
        from phase2 import run
        run()


if __name__ == '__main__':
    main()
