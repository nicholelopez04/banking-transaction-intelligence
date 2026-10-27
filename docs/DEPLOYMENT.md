# Proposed deployment: awaiting approval

Service: Streamlit Community Cloud, free tier. No publication has occurred.
Proposed public GitHub repository: banking-transaction-intelligence (availability
and account owner not yet checked because authentication is unavailable).

## Configuration to be completed after approval

- Repository branch: use the branch containing the reviewed files.
- Main file: jpmorgan_transaction_project/jpmorgan_transaction_project/app.py
- Python: select 3.12 in Advanced settings.
- Dependencies: requirements.txt beside app.py is auto-detected. It includes requirements-lock.txt so the
  hosted install uses the same pinned packages as the verified local environment.
- No secrets, API keys, database service or packages.txt are required by this app.
- Data paths are based on Path(__file__).resolve(), not a Windows working directory.
- Synthetic Phase 1/2 fixtures are included. Robustness falls back to the existing
  compact docs/results evidence when ignored local runs are unavailable.
- Do not run training or regenerate evaluation data on the hosting service.

## Accounts, exposure and limits

GitHub and Streamlit accounts are required. Streamlit needs access to the chosen
GitHub repository and deployment requires repository admin permission. Public
repository deployment avoids the extra private-repository OAuth permissions.
Account sign-in, MFA, terms acceptance and OAuth consent may need the account owner.
Never paste credentials into the chat or commit them.

The proposed repository would expose source, tests, documentation, synthetic
reference CSVs/metrics and compact recorded evidence. The dashboard would be
accessible to anyone with its public URL, including its synthetic CSV downloads.
Environments, backups, secrets, SQLite databases, fitted models and full repeated-run
folders remain excluded. Git commit author details are public if commits are pushed;
choose an appropriate author identity, such as a GitHub noreply email.

Community Cloud is free with resource limits and can sleep when inactive. There is
no paid resource purchase or custom domain in this proposal. Provider terms and
limits apply. The dashboard is a batch viewer of synthetic results, not a real-time
payment system. The existing synthetic-data disclaimer remains visible.

Windows operation is tested with the existing Python 3.12 virtual environment.
There is no usable Linux/WSL or Docker runtime on this machine, so an actual Linux
build is not yet verified. The Cloud build and live dashboard must be checked after
approved publication. Relative paths and dependency declarations are portable;
that static check is not a substitute for a successful hosted build.

Official references:
- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account

## Current readiness

All 27 tests pass after adding one hosted-checkout regression test; the original
26 remain intact. Pip check passes, and all 187 original data/result artifacts
retain their hashes. A pattern-based scan found no secrets or sensitive filenames
in the included files; it is not a formal security guarantee. GitHub connector
authentication was verified for nicholelopez04. The proposed repository lookup
returned 404 (not visible to the connected account). Streamlit browser sign-in is
still required. The exact intended file set is in PUBLICATION_FILES.txt.
