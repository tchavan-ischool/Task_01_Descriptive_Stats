# Validation record

Dataset: `fb_ads_president_scored_anon.csv` (246,745 rows, 40 columns).

Executed the following commands on the provided CSV:

```bash
python pure_python_stats.py <dataset.csv> --output pure_check.json
python pandas_stats.py <dataset.csv> --output pandas_check.json
python verify_results.py pure_check.json pandas_check.json
```

**Observed result:** `PASS: all columns and statistics agree (within floating point tolerance)`.

This validates agreement under the shared analysis conventions, not the underlying accuracy of the advertising data. Validation JSON is excluded from the submission package because the scripts can reproduce it.
