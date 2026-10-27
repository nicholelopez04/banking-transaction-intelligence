"""Prior-day behavioral features and validation-only feature comparison."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from main import generate_data, select_threshold, write_threshold_plot

FEATURE_SETS = {
    'prior_ratio': ['log_amount', 'amount_vs_prior_avg'],
    'enhanced': ['log_amount', 'amount_vs_prior_avg', 'log_prior_avg',
                 'log_prior_count', 'cold_start'],
}


def prior_features(data):
    """Use strictly earlier calendar dates; never assume intra-day ordering.

    New customers use the earlier global average. Before any global history
    exists, use a fixed $1 neutral denominator. Cold-start ratios are fixed
    to 1 because no customer-relative comparison is available yet.
    """
    required = ['transaction_id', 'customer_id', 'date', 'amount']
    frame = data[required].copy()
    frame['date'] = pd.to_datetime(frame['date'], errors='raise').dt.normalize()
    if frame[required].isna().any().any() or frame.transaction_id.duplicated().any():
        raise ValueError('Require complete records and unique transaction IDs')
    if not np.isfinite(frame.amount).all() or (frame.amount < 0).any():
        raise ValueError('Require finite nonnegative amounts')
    daily = frame.groupby(['customer_id', 'date'], as_index=False).agg(
        daily_sum=('amount', 'sum'), daily_count=('amount', 'size'))
    daily = daily.sort_values(['customer_id', 'date'])
    daily['prior_sum'] = daily.groupby('customer_id').daily_sum.cumsum() - daily.daily_sum
    daily['prior_count'] = daily.groupby('customer_id').daily_count.cumsum() - daily.daily_count
    global_daily = frame.groupby('date').amount.agg(['sum', 'count']).sort_index()
    sums = global_daily['sum'].cumsum().shift(1, fill_value=0)
    counts = global_daily['count'].cumsum().shift(1, fill_value=0)
    global_average = sums.div(counts.replace(0, np.nan)).fillna(1.0)
    daily['prior_avg'] = daily.prior_sum.div(daily.prior_count.replace(0, np.nan))
    daily['prior_avg'] = daily.prior_avg.fillna(daily.date.map(global_average))
    joined = frame.merge(daily[['customer_id', 'date', 'prior_count', 'prior_avg']],
                         on=['customer_id', 'date'], how='left', validate='many_to_one')
    joined.index = data.index
    features = joined[['transaction_id', 'prior_count', 'prior_avg']].copy()
    features['cold_start'] = (features.prior_count == 0).astype(int)
    features['log_amount'] = np.log1p(joined.amount)
    features['amount_vs_prior_avg'] = joined.amount.div(features.prior_avg.clip(lower=0.01))
    features.loc[features.cold_start == 1, 'amount_vs_prior_avg'] = 1.0
    features['log_prior_avg'] = np.log1p(features.prior_avg)
    features['log_prior_count'] = np.log1p(features.prior_count)
    return features


def run():
    output = Path(__file__).resolve().parent / 'outputs' / 'phase2'
    output.mkdir(parents=True, exist_ok=True)
    # Historical test rows never enter this feature-selection experiment.
    raw = generate_data()
    development = raw.loc[raw.date < '2026-09-21'].copy()
    data = development.dropna(subset=['amount']).copy()
    train_mask = data.date < '2026-09-15'
    validation_mask = ~train_mask
    features = prior_features(data)
    exported = data.join(features.drop(columns='transaction_id'))
    exported['split'] = np.where(train_mask, 'train', 'validation')
    exported.to_csv(output/'development_features.csv', index=False)
    # The old two-feature recipe is a reference only: its training means
    # contain future training rows. It is ineligible for selection.
    reference = features.copy()
    average = data.loc[train_mask].groupby('customer_id').amount.mean()
    reference['amount_vs_customer_avg'] = data.amount / data.customer_id.map(average).fillna(
        data.loc[train_mask, 'amount'].mean()).clip(lower=0.01)
    experiments = {'phase1_reference': (reference, ['log_amount', 'amount_vs_customer_avg'])}
    experiments.update({name: (features, columns) for name, columns in FEATURE_SETS.items()})
    results = []
    for name, (values, columns) in experiments.items():
        scaler = StandardScaler()
        x_train = scaler.fit_transform(values.loc[train_mask, columns])
        x_validation = scaler.transform(values.loc[validation_mask, columns])
        model = IsolationForest(n_estimators=150, contamination=0.03, random_state=42)
        model.fit(x_train)
        scores = -model.decision_function(x_validation)
        table, selected = select_threshold(data.loc[validation_mask, 'is_injected_anomaly'], scores)
        table.to_csv(output/f'{name}_thresholds.csv', index=False)
        write_threshold_plot(table, output/f'{name}_thresholds.svg')
        predictions = exported.loc[validation_mask].copy()
        predictions['anomaly_score'] = scores
        predictions['anomaly_flag'] = scores >= selected['threshold']
        predictions.to_csv(output/f'{name}_validation_results.csv', index=False)
        results.append({'feature_set': name, **selected, 'feature_count': len(columns),
                        'eligible': name != 'phase1_reference'})
    comparison = pd.DataFrame(results)
    comparison.to_csv(output/'feature_comparison.csv', index=False)
    # Prefer fewer features when validation F1 ties; then fewer alerts.
    selected = comparison.loc[comparison.eligible].sort_values(
        ['f1', 'feature_count', 'alerts', 'feature_set'], ascending=[False, True, True, True]).iloc[0]
    report = {
        'selected_feature_set': selected.feature_set,
        'feature_columns': FEATURE_SETS[selected.feature_set],
        'selection_rule': 'Validation F1 descending; feature count ascending; alerts ascending; name ascending',
        'train_rows': int(train_mask.sum()), 'validation_rows': int(validation_mask.sum()),
        'validation_injections': int(data.loc[validation_mask, 'is_injected_anomaly'].sum()),
        'missing_amount_rows_excluded': int(development.amount.isna().sum()),
        'cold_start_rows': int(features.cold_start.sum()),
        'evaluation_scope': 'Development data only; historical test not scored; fresh final period pending model freeze',
        'history_policy': 'Strictly earlier dates; validation history updates with earlier observed validation amounts, never labels',
        'generator_changed': False,
        'results': results,
    }
    (output/'evaluation_metrics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(comparison.to_string(index=False))
    print('Selected:', selected.feature_set)
    print('Historical test not scored. All metrics refer to synthetic injections.')
    print('Saved:', output)


if __name__ == '__main__':
    run()
