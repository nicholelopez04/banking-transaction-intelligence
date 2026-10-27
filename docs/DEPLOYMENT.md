# Deployment and live verification

## Pending final-study presentation update

The accepted Stage 5 presentation has been prepared locally and is awaiting separate commit, push and deployment approval. The current proposed allowlist is `PUBLICATION_FILES.txt` (83 files); it is not the original 59-file upload list referenced in the historical record below. See `PORTFOLIO_PUBLICATION_REVIEW.md` for the new local checks and exclusions. No new Linux build or live verification of this update is claimed. The dashboard now also requires `dashboard_evaluation.py` and the compact `docs/results/stage5/` evidence directory; full research archives are not required at runtime.

The rest of this document records the earlier deployment and its checks at that time. Those older test counts and model-performance views do not describe the pending update. A push to the configured public branch may trigger automatic redeployment, so it remains subject to explicit publication approval.

- Public repository: https://github.com/nicholelopez04/banking-transaction-intelligence
- Live dashboard: https://nicholelopez-banking-intelligence.streamlit.app/
- Host: Streamlit Community Cloud, free tier.
- Branch: main.
- Entrypoint: jpmorgan_transaction_project/jpmorgan_transaction_project/app.py
- Python runtime: 3.12, explicitly selected in Advanced settings.
- Dependencies: requirements.txt beside app.py includes requirements-lock.txt.
- No app secrets, external database or packages.txt were required.

## Published files and integrity

Only the 59 paths in PUBLICATION_FILES.txt were uploaded. The original reviewed
upload is commit 7c4a077878bdbacfa9c77de7ed9a44eca5a13ac7, with Git tree
4e2d620002b165630114ea833e71989f0389a7f9. That tree matches a Git tree computed
from all 59 local reviewed files, including the screenshot binary. Later updates
to this guide and the README record deployment URLs and verification results.

The final file scan found no credential patterns, email addresses or personal
Windows-home paths. Raw reference transactions matched the seeded synthetic
generator. Environments, secrets, backups, databases, fitted model binaries and
full repeated-run folders remain excluded. All 187 pre-existing data/result
artifacts retain their original hashes. The ML evaluation methodology was not changed.

## Hosted build

The actual Linux Community Cloud build completed and the app started successfully.
File reads resolve relative to __file__, not the Windows working directory.
Phase 1/2 reference fixtures are committed. When ignored local experiment runs
are absent, the Robustness tab reads the existing compact docs/results snapshot.
No experiments run during dashboard startup. The original 26 tests plus the
hosted-checkout regression test pass (27 total); pip check passed locally.

## Live checks

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

## Ownership and operation

The account owner completed sign-in before deployment. No credentials were added
to app files or secrets settings. Repository updates on main can trigger automatic
redeployment. No custom domain or paid resources were enabled. Community Cloud's
free resource limits and inactivity sleep behavior apply. The URL is public and
synthetic CSV downloads are accessible to visitors.

Official references:
- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
