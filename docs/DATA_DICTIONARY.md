# Data dictionary

All records describe synthetic transactions. IDs have no real-world identity.

## Transaction records

| Column | CSV / SQLite representation | Meaning |
|---|---|---|
| transaction_id | Integer / INTEGER | Unique transaction identifier within a dataset; Phase 4 future IDs start after development IDs |
| customer_id | Integer / INTEGER | Synthetic customer ID, 100 through 149 |
| date | YYYY-MM-DD / TIMESTAMP | Calendar date; SQLite export may include midnight, which does not supply actual transaction time |
| amount | Floating point / REAL | Synthetic amount in dollars; missing in some raw rows; usable values finite and nonnegative |
| merchant_category | Text / TEXT | groceries, travel, retail, utilities or restaurants |
| is_injected_anomaly | Boolean / INTEGER | Evaluation-only indicator of deliberate amount perturbation; not a fraud label |
| anomaly_score | Floating point, prediction outputs | Negative decision_function; larger means more unusual; scales differ across models/runs |
| anomaly_flag | Boolean, prediction outputs | Saved score >= selected threshold; review suggestion only |

Raw CSVs retain missing amounts. Cleaned CSVs and SQLite transactions exclude them.
Injection counts can change during cleaning when a missing amount overlaps an
injected row. Always distinguish raw from usable labels. Floating-point amounts
are appropriate to this numerical demo; production ledgers typically require
explicit currency, precision and reconciliation rules.

## Prior-day customer features

| Column | Definition |
|---|---|
| prior_count | Number of customer's usable transactions on strictly earlier dates |
| prior_avg | Mean of customer's usable amounts on strictly earlier dates |
| cold_start | 1 if prior_count is zero; otherwise 0 |
| log_amount | log(1 + current amount) |
| amount_vs_prior_avg | Current amount / max(prior_avg, 0.01), or 1 for a cold start |
| log_prior_avg | log(1 + prior_avg) |
| log_prior_count | log(1 + prior_count) |
| split | train or validation in saved Phase 2 development_features.csv |

A new customer's prior_avg falls back to the earlier global mean. With no earlier
global observations, the fixed fallback is $1. The ratio is neutralized to 1 for
cold starts because no personal comparison is available. A one-observation
customer uses that observation; this can be noisy. No later training rows, same-day
peers, labels or future dates enter prior history. Earlier validation/future
amounts update later-day history but never refit the model or scaler.

Selected features are log_amount and amount_vs_prior_avg. Prior average/count and
cold_start were available in the enhanced candidate but showed no validation gain.
No hour-of-day feature exists because the source has no transaction time.

## Metrics and evidence

Precision = TP / (TP + FP); recall = TP / (TP + FN); F1 is their harmonic mean.
TP/FP/FN/TN compare saved alerts with known injection labels only. Precision@10
measures injection share among the top ten scores across a complete period; it is
not daily precision and is independent of the alert threshold.

Phase 4 per-run CSVs include scenario, seed, model, threshold, rows, injections,
alerts, confusion counts and metric values. precision_defined and recall_defined
identify zero-denominator cases; numeric summaries follow zero_division=0.
Summary suffixes _mean, _std, _min, _max describe repeated seeds; _std is sample SD.
The selected_model field marks the validation-selected detector, not a detector
chosen from future outcomes. See [methodology](EVALUATION.md).
