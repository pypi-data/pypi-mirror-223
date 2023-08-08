from typing import Union

import pandas as pd
import statsmodels.api as sm


def lowess_grouped(
        data: pd.DataFrame,
        x_name: str,
        y_name: str,
        group_name: Union[str, None],
        smoothed_col_suffix="_smooth",
        frac=0.6666666666666666,
        it=3,
        delta=0.0,
        is_sorted=False,
        missing='drop',
        return_sorted=True
) -> pd.DataFrame:
    """
    applies lowess smoothing to each group
    if no group is supplied lowess will be applied to the whole dataset
    """
    df = data.copy()
    y_name_smoothed = y_name + smoothed_col_suffix
    if group_name is not None:
        groups = df[group_name].unique().tolist()
        smoothed_dfs = []
        for group in groups:
            df_by_select_group = df[df[group_name] == group]
            smoothed_df = sm.nonparametric.lowess(
                df_by_select_group[y_name],
                df_by_select_group[x_name],
                frac=frac,
                it=it,
                delta=delta,
                is_sorted=is_sorted,
                missing=missing,
                return_sorted=return_sorted
            )
            smoothed_df = pd.DataFrame(smoothed_df)
            smoothed_df.columns = [x_name, y_name_smoothed]
            smoothed_df[x_name] = smoothed_df[x_name].astype(int)
            smoothed_df[group_name] = group
            smoothed_dfs.append(smoothed_df)
        return pd.merge(df, pd.concat(smoothed_dfs), how="left", on=[x_name, group_name])
    else:
        smoothed_df = sm.nonparametric.lowess(
            df[y_name],
            df[x_name],
            frac=frac,
            it=it,
            delta=delta,
            is_sorted=is_sorted,
            missing=missing,
            return_sorted=return_sorted
        )
        smoothed_df = pd.DataFrame(smoothed_df)
        smoothed_df.columns = [x_name, y_name_smoothed]
        return pd.merge(df, smoothed_df, how="left", on=x_name)
