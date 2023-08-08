# lowess-grouped

Apply groupwise lowess smoothing to a dataframe.

This project builds upon the lowess function from statsmodels.

## Usage

Simply import the package, and pass your dataframe `df` to the function `lowess_grouped`:

```python
from lowess_grouped.lowess_grouped import lowess_grouped
df_smoothed = lowess_grouped(df, "x_col_name", "y_col_name", "group_name", frac=0.05)
```

For a more detailed example see the temperature-example.ipynb.
