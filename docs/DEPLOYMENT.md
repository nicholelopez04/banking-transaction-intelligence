# Deployment and live verification

## Completed Stage 5 publication — October 27, 2026

The accepted Stage 5 presentation was published successfully to the existing repository and deployed to the existing Streamlit Community Cloud application.

- Repository: [nicholelopez04/banking-transaction-intelligence](https://github.com/nicholelopez04/banking-transaction-intelligence).
- Live dashboard: [Banking Transaction Intelligence](https://nicholelopez-banking-intelligence.streamlit.app/).
- Published and deployed commit: [d5879b7893ea0a8088f954dd6e062769bbae8b58](https://github.com/nicholelopez04/banking-transaction-intelligence/commit/d5879b7893ea0a8088f954dd6e062769bbae8b58).
- Parent: `e1782b584dddc284d9c1e473f4ad8d93e46fca37`; publication was a normal fast-forward, preserving repository history without modifying the approved commit.
- Published tree: `e0d31628118a32e72aeff13b33f9514844391a42`, containing exactly the 83 reviewed paths in [PUBLICATION_FILES.txt](PUBLICATION_FILES.txt). The remote commit and tree matched the reviewed publication.
- Entrypoint: `jpmorgan_transaction_project/jpmorgan_transaction_project/app.py`, branch `main`.

The [pre-publication review](PORTFOLIO_PUBLICATION_REVIEW.md) records the earlier local checks and exclusions. Its pending-publication wording describes that historical preparation stage. Full datasets, fitted model binaries, archives, environments, secrets and logs were excluded. The dashboard reads compact saved evidence and does not train models or regenerate experiments.

## Linux build and startup recovery

The fresh Community Cloud Linux build completed using **Python 3.12.15**, installed dependencies from `requirements.txt` beside the entrypoint, and started the application successfully. Paths resolve from source-file locations; no Windows working directory, external database or app secrets are required.

The initial automatic update reported `ImportError: cannot import name 'load_independent' from 'dashboard_data'`. The published source contained that function. Rebooting the existing app cleared the error in a fresh Python process, consistent with a stale imported module during the update. No application code, experiment results or dependency declarations were changed to resolve it. No further runtime errors were observed during the subsequent live checks.

Streamlit's build detected a compatibility issue with pinned **PyArrow 26.0.0** and automatically replaced it with **PyArrow 24.0.0**. This was a provider-side substitution, not a repository dependency edit. The verified hosted environment therefore differs from the exact lock file at that dependency.

## Completed live verification

- The default landing tab is **Independent evaluation**, presenting the accepted Stage 5 synthetic study.
- All 16 native-policy and equal-budget metric cards matched the saved [pooled metrics](results/stage5/pooled_metrics.csv). Native review counts remain 83 for Phase 2 and 5,184 for Phase 6 v1; the separate ranking comparison uses exactly 8,000 reviews per pipeline.
- Scenario charts, all eight scenarios, policy switching, variability and screening failures remained available.
- The public download containing all 160 case/policy records matched the saved [case-results CSV](results/stage5/all_case_metrics.csv) byte-for-byte: SHA-256 `6e15a99525f8fb323dba9e636f0b5722aaabb9b420772474ddb80877970d99a2`.
- The dashboard prominently disclosed that neither model met the hypothetical synthetic screening targets and neither is production-ready, and that 452 of 462 Phase 6 native detections were inactivity returns.
- The legacy explorer showed 995 transactions, $110,110.12 total volume and 50 synthetic customers. Customer 100 filtering returned 18 transactions and $2,516.17; independent-study metrics remained unchanged under filtering.
- Transaction overview charts, customer spending, saved anomaly rankings and alert-only filtering worked. Historical robustness charts loaded the recorded portfolio snapshot.
- Historical validation retained 100% precision/recall with the label **Model Selection Only — Two Injected Anomalies**. The separate Phase 1 historical view retained 333 rows, four missed injections, zero alerts and N/A precision.
- Synthetic-data and evaluation-limitations disclosures remained visible. No model was retrained, threshold changed, or frozen experiment or evaluation result modified for deployment.

The earlier local verification passed 82 tests in the full research workspace and 32 tests in an isolated publication-only checkout. Those were Windows test runs; they are separate from the successful hosted Linux build and live browser checks above.

## Historical deployment record — initial 59-file release

The record below describes the earlier deployment before the Stage 5 presentation update. Its 27-test count and older model-performance views are historical, not the current verification summary. The original reviewed file list contained 59 paths; the later Stage 5 publication expanded it to 83.

- Public repository: https://github.com/nicholelopez04/banking-transaction-intelligence
- Live dashboard: https://nicholelopez-banking-intelligence.streamlit.app/
- Host: Streamlit Community Cloud, free tier.
- Branch: main.
- Entrypoint: jpmorgan_transaction_project/jpmorgan_transaction_project/app.py
- Python runtime: 3.12, explicitly selected in Advanced settings.
- Dependencies: requirements.txt beside app.py includes requirements-lock.txt.
- No app secrets, external database or packages.txt were required.

### Published files and integrity

Only the original 59 reviewed paths were uploaded in that release. The original reviewed
upload is commit 7c4a077878bdbacfa9c77de7ed9a44eca5a13ac7, with Git tree
4e2d620002b165630114ea833e71989f0389a7f9. That tree matches a Git tree computed
from all 59 local reviewed files, including the screenshot binary. Later updates
to this guide and the README record deployment URLs and verification results.

The final file scan found no credential patterns, email addresses or personal
Windows-home paths. Raw reference transactions matched the seeded synthetic
generator. Environments, secrets, backups, databases, fitted model binaries and
full repeated-run folders remain excluded. All 187 pre-existing data/result
artifacts retain their original hashes. The ML evaluation methodology was not changed.

### Hosted build

The actual Linux Community Cloud build completed and the app started successfully.
File reads resolve relative to __file__, not the Windows working directory.
Phase 1/2 reference fixtures are committed. When ignored local experiment runs
are absent, the Robustness tab reads the existing compact docs/results snapshot.
No experiments run during dashboard startup. The original 26 tests plus the
hosted-checkout regression test pass (27 total); pip check passed locally.

### Live checks

- Overview charts render, with 995 cleaned transactions, $110,110.12 total volume
  and 50 synthetic customers.
- Data quality shows 1,000 raw rows, five missing/excluded amounts, and 15 injections.
- Customer 100 filter yields 18 transactions and $2,516.17, matching saved data.
- Customer spending chart renders for the selected transactions.
- Validation alert-only ranking shows transactions 324 and 754, the two saved alerts.
- Phase 2 validation evaluation shows 199 rows, two injections, two alerts and
  100% precision/recall/F1. These are selection results, not independent test quality.
- Phase 1 historical evaluation preserves zero alerts, four missed injections,
  N/A precision, zero recall/F1, TN=329 and precision@10=40%.
- Robustness loads the recorded portfolio snapshot, identifies the validation-selected
  Isolation Forest, and switches from precision to F1 charts successfully.
- The sharing dialog confirms Make this app public is enabled.
- The synthetic-data disclaimer remains visible. No real fraud claims were introduced.

### Ownership and operation

The account owner completed sign-in before deployment. No credentials were added
to app files or secrets settings. Repository updates on main can trigger automatic
redeployment. No custom domain or paid resources were enabled. Community Cloud's
free resource limits and inactivity sleep behavior apply. The URL is public and
synthetic CSV downloads are accessible to visitors.

Official references:
- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
