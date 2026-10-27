# Final-study portfolio update — local publication review

Status: prepared locally; awaiting separate approval before any commit, GitHub push or Streamlit redeployment. No final experiment was rerun and no model development occurred.

## Proposed changes

The first dashboard tab presents the accepted Stage 5 independent synthetic evaluation. Phase 2 and Phase 6 v1 native decisions retain their different review counts and policies. Equal-budget ranking is separate, at exactly 8,000 reviews per pipeline. All eight scenarios, five-seed variability, every case/policy result and screening failures are retained. The dashboard highlights that 452/462 Phase 6 native detections were inactivity returns and that neither model passed the hypothetical screening targets or is production-ready.

Legacy overview/customer charts, transaction filters, saved rankings, validation threshold exploration and historical robustness remain available. The 100% validation result is labeled “Model Selection Only — Two Injected Anomalies.” Sidebar filters do not alter independent performance denominators. README, methodology and interview guidance now tell the same evidence-based story.

## Verification

The full research suite passed **82 tests**; the isolated allowlist-only checkout passed **32 tests**, without any full research datasets or model artifacts. Python 3.12 is used from the existing Windows virtual environment. `pip check` passed with no broken requirements. AppTest checks preserve empty filters, customer 100, saved alert rankings, historical evaluation, threshold exploration, robustness switching and independent-metric invariance. New checks reconcile exported metrics to all case records, verify exact budgets and detection concentration, test portable loading, reject altered evidence and preserve N/A gate semantics. Detailed console records stay local in `backups/portfolio-presentation-tests.log` and `backups/portfolio-allowlist-tests.log` because logs contain machine-specific paths.

Local browser verification uses `http://127.0.0.1:8502/`. The independent tab is selected at launch; native and ranking cards match saved evidence. The legacy overview shows 995 rows, $110,110.12 and 50 synthetic customers. Customer 100 yields 18 rows and $2,516.17 while independent cards remain unchanged. Scenario charts render and saved historical controls remain available. This is local Windows verification, not a claim of a new Linux or public deployment.

## Frozen evidence

Read-only preservation checks passed after implementation: 187 original artifacts, 144 earlier Phase 2 study entries, 513 Phase 6 development entries plus six report entries, 69 frozen Phase 6 entries, 517 Stage 5 entries, three final-review entries, 41 seed/study claims and all 652 archived live files. Both fitted models, thresholds, policies, source snapshots and previous archive hashes remain unchanged.

The approved live edits to `app.py`, `dashboard_data.py` and `tests/test_dashboard.py` intentionally differ from historical source hashes; their prior versions remain frozen. The preservation check explicitly records this allowlist rather than changing any historical manifest. New presentation code is separate from frozen model/generator code.

## Exact proposed publication scope

`PUBLICATION_FILES.txt` enumerates all **83 paths**, with no wildcard directory upload. The local `backups/portfolio-publication-inventory.json` records each path's byte size and SHA-256 and the scan findings. This inventory is a local review artifact, not an additional upload path.

The bundle retains the previous 59 reviewed public paths and adds 24: one dashboard presentation module, one test module, this review, 18 Stage 5 presentation/evidence files and three historical research evidence files. Existing public files with edits are README, the application README, dashboard source/data loader, dashboard tests, evaluation methodology, interview guide, deployment notes and the publication list.

The explicit bundle is approximately **0.81 MB** in total; its largest file is the 92,040-byte legacy development feature fixture. The scan found no private-key/token patterns, credential assignments, email addresses or personal Windows-home paths in the proposed files. No file exceeds 5 MB. Reviewed data consist of preserved seeded synthetic fixtures and saved synthetic study summaries; the generated evidence contains scenario/seed/model metrics, not real account or identity information. Automated pattern scanning is not an absolute proof of absence of secrets, and is supplemented by source and content review.

Stage 5 evidence comprises 16 byte-identical original outputs (170,065 bytes), an export manifest and a short explanatory README. Historical evidence includes the original Phase 2 independent metric JSON and all nine Phase 6 candidate summaries across calibration, selection and audit, plus provenance hashes. The original protocol's embedded proposal status is explicitly explained as historical text.

Excluded: the 146.5 MB final archive and all earlier archives, full final/development datasets, warmup/raw cases, row-level final predictions, profiles, feature matrices, fitted joblib/pickle files, SQLite databases, virtual environments, logs, seed claim files, machine settings, credentials and unrelated local tools. Existing small Phase 1/2 synthetic fixtures remain included because the explorer requires them. No new real transactions, personal customer data, credentials or bank information are included.

The public bundle is a compact evidence viewer and metric-inspection package. Full archival research tests require local research modules and frozen evidence that remain excluded; this limitation is explicit in the README. Portable dashboard/legacy/presentation tests must pass in an isolated copy containing only the allowlist. Full research reproduction is not implied by the compact bundle.

## Publication gate and limitations

The current local Git checkout remains on `codex/phase1-threshold-tuning` with an unborn history and untracked files; it is not a conventional checkout of the existing published main history. Do not stage the workspace wholesale. After approval, publication must preserve the existing remote history and use only the reviewed allowlist, with a fresh byte/hash comparison before upload. No commit or remote modification has been made here.

The target repository is `nicholelopez04/banking-transaction-intelligence`; the existing dashboard URL is `https://nicholelopez-banking-intelligence.streamlit.app/`. Authentication has not been exercised during this local-only task. Account authorization may be needed for the later publish. Pushing to the configured branch may automatically rebuild Streamlit. Updated live functionality must be verified after that separately approved step; the current public dashboard is not claimed to contain this update.
