# Application directory

See the [repository README](../../README.md) for final findings, setup and limitations.
Run the saved-evidence dashboard without regenerating experiments:

```powershell
& .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
& .\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

The first tab presents the accepted Stage 5 independent synthetic evaluation. All transactions are synthetic; neither pipeline met its research screening targets or is production-ready. Legacy CLI experiments remain available for historical source inspection, but are not needed to view saved results and should not overwrite accepted evidence.
