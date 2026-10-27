# Application directory

The current project guide is the [repository README](../../README.md).
This directory retains the original working Python environment and runnable main.py.

From this directory in Windows PowerShell:

```powershell
& .\.venv\Scripts\python.exe main.py
& .\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
& .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

The default run compares Phase 2 features on validation only. `--phase 1`
reproduces the historical threshold experiment; `--phase 4` runs repeated model
comparison with a frozen future assessment. See the root guide for exact output
behavior, installation commands, measured results and limitations.

All data is synthetic; anomaly alerts are not verified fraud.
