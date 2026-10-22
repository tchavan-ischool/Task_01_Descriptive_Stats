# Comparison — Pure Python and Pandas

## Purpose
Task 1 requires two independent implementations of the same descriptive statistics. The comparison is meaningful only when both approaches use the same definitions of missingness, numeric type inference, sample standard deviation, and categorical ties.

## Pure Python
The standard-library implementation uses `csv.DictReader`, `collections.Counter`, `math.fsum`, sorting, and explicit formulas. It makes the algorithm visible: parse every cell, decide whether the column is numeric, compute a mean and sample standard deviation, or build categorical frequency tables. It requires more code and manual handling of nulls, edge cases, and type conversion. This visibility is useful for understanding what a statistical summary actually means.

## Pandas
The Pandas implementation uses column operations, `pd.to_numeric`, `value_counts`, `nunique`, `mean`, `median`, and `std(ddof=1)`. The result is more concise and easier to extend to larger grouped analyses. However, automatic inference and defaults can conceal important choices. In particular, `std()` uses a sample denominator, missing values may be handled implicitly, and a range object stored as text is not a single number. The script reads all columns as strings first and applies the same explicit inference rules as pure Python.

## Verification
Run both scripts on the same CSV and then execute `verify_results.py`. It compares every statistic and category, allowing a small tolerance only for floating-point arithmetic. The scripts should be rerun after any changes to cleaning or type inference. A successful comparison shows that two implementations agree under shared rules; it does not prove that the original data is accurate.

## Reflection
The most important lesson is that data preparation and metric definitions matter as much as the choice of tool. Pure Python forces the researcher to confront missingness, mixed types, and standard-deviation formulas. Pandas makes the same analysis shorter and easier to maintain, but the analyst must still verify what the library assumes. For this dataset, treating `spend` and `impressions` as plain numeric columns would be a bigger mistake than any minor difference in calculation speed. The most defensible workflow is to inspect raw values, document assumptions, implement independently, compare results, and then write cautious conclusions.
