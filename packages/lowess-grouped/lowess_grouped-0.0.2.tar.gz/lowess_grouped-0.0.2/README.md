# Lowess Grouped

Apply groupwise lowess smoothing to a dataframe.

![lowess-grouped-example](https://raw.githubusercontent.com/lukiwieser/lowess-grouped/main/docs/lowess-grouped-example.png)

## Usage

Install the package:
```console
pip install lowess-grouped
```

Then simply import the package, and call the function `lowess_grouped` with your dataframe `df`:

```python
from lowess_grouped.lowess_grouped import lowess_grouped

df_smoothed = lowess_grouped(df, 
                             x_name="year", 
                             y_name="temperature_anomaly",
                             group_name="region_name", 
                             frac=0.05)
```

For a more detailed example take a look at the notebook [temperature-example.ipynb](https://github.com/lukiwieser/lowess-grouped/blob/main/example/temperature-example.ipynb).

## More

This project builds upon the lowess function from [statsmodels](https://www.statsmodels.org).
