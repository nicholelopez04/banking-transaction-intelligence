# Architecture

The application stays in its existing nested directory to preserve the Windows
virtual environment. The root README is the current entry point. Tests are under
the application's tests/ directory; docs and SQL examples live at repository root.

| Module | Responsibility |
|---|---|
| main.py | CLI, original deterministic generator, threshold selection, Phase 1 pipeline |
| phase2.py | Prior-day features and validation-only feature comparison |
| phase4.py | Scenario generation, fixed model comparison, freeze and future assessment |
| dashboard_data.py | Read saved CSV/JSON artifacts, filter transactions, count confusion outcomes |
| app.py | Streamlit controls, charts and scope explanations |

## Data flow

1. Generate synthetic records using a local NumPy Generator and explicit seed.
2. Exclude missing amounts from numerical analysis. The original pipeline also
   validates IDs, dates, finite amounts and nonnegative amounts.
3. Construct customer-day sums/counts. Cumulative sums minus the current day's
   contribution supply strictly earlier-day history. Join history back to rows.
4. Split by date. Fit StandardScaler and detector on training rows only.
5. Score validation rows, use injection labels only for threshold/model selection.
6. Phase 4 saves model/scaler/threshold bundles, parameters and hashes before
   generating the future assessment data. Future scores do not change selection.
7. Save CSV/JSON evidence. The dashboard reads files on each rerun and never fits
   a model, changes thresholds on disk or rewrites experiment outputs.

## Boundaries

The original root-level CSVs/database are preserved local baseline artifacts.
Phase 1/2 write only their own output directories. Phase 4 writes a new timestamped
folder per invocation. Small Phase 1/2 fixtures accompany source for immediate
viewing/testing; databases and fitted models are regenerated locally and ignored.
Compact Phase 4 evidence is copied to docs/results for review without bulky models.

The dashboard's robustness loader identifies only runs with a completion metrics
file. Partially generated runs are not displayed. Its overview comes from Phase 1
saved transactions; Phase 2 supplies validation ranking/evaluation. Robustness uses
separate future scenario data, so sidebar filters do not apply to that evidence.

The CLI is deliberately small: importing main does not run a pipeline because of
the __name__ guard. Functions receive data frames or return values where practical.
Pandas performs grouped calculations; SQLite illustrates relational aggregation;
scikit-learn supplies detectors, preprocessing and metric calculations.

No network service, account, secret, task scheduler or production payment API is
required. The documented dashboard command binds only to 127.0.0.1.
