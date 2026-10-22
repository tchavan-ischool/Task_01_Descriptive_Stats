# Task 01 — Descriptive Statistics With and Without Pandas

## Project overview
This project examines a provided 2024 U.S. presidential election Facebook advertising dataset with two independent descriptive-statistics implementations: Python's standard library and Pandas. Both analyze every column, report missingness, and compute numerical or categorical summaries under matching rules. A third script verifies agreement.

## Dataset
The research-program dataset is **2024 Facebook Political Ads**, distributed via the course's Google Drive materials. Download the original CSV from the link in the assignment/course materials and place it at `data/fb_ads_president_scored_anon.csv` (create the `data/` directory). **The dataset is not included in this repository.** Replace this sentence with the actual course-authorized source URL if available. This file contains 246,745 records and 40 fields in the copy analyzed for this report. This Task 1 file must not be confused with any later task's file.

## Setup and execution
Requires Python 3.10+.

```bash
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
mkdir -p outputs
python pure_python_stats.py data/fb_ads_president_scored_anon.csv --output outputs/pure.json
python pandas_stats.py data/fb_ads_president_scored_anon.csv --output outputs/pandas.json
python verify_results.py outputs/pure.json outputs/pandas.json
```

`pure_python_stats.py` uses only Python's standard library. `pandas_stats.py` uses Pandas. Both produce machine-readable JSON. The Pandas implementation uses `value_counts`, `nunique`, `mean`, `median`, `min`, `max`, and sample `std`; `describe()` can be used for additional exploratory inspection.

## Shared analysis conventions
- Trim whitespace. Empty strings, `NA`, `N/A`, `null`, `none`, and `nan` (case-insensitive) count as missing.
- A column is numeric only when **all non-missing** entries parse as finite numbers (commas in numbers are accepted). Otherwise it is categorical. Empty columns have type `empty`.
- Numeric standard deviation is the **sample** standard deviation (`ddof=1`); for one observation it is `null`.
- Categorical ties are broken alphabetically for reproducibility.
- The `spend`, `impressions`, and `estimated_audience_size` fields contain serialized **range objects**, not direct numeric values. They are treated as categorical in the baseline analysis; any range midpoint estimates must be separately justified.
- Dates and identifiers are categorical in this baseline rather than misleadingly treated as measurements.

## Findings
See [FINDINGS.md](FINDINGS.md) for an evidence-based interpretation and important data-quality limitations.

## Approach comparison
See [COMPARISON.md](COMPARISON.md) for the tradeoffs and the cross-implementation verification procedure.

## Reproducibility and ethics
Do not upload the CSV, which is excluded by `.gitignore`. The records describe advertising activity; descriptive statistics alone do not establish causation, persuasion effects, or audience attitudes. Some flags and classifications are supplied by the dataset and should not be assumed error-free.
