"""Helper Functions to Calculate BABIP & Generate Plots"""

import polars as pl
import matplotlib.pyplot as plt


def babipCalculator(df: pl.DataFrame) -> pl.DataFrame:
    """
    Uses the Polars Aggregation Functionality to Calculate Each Team's BABIP

    Args:
        df (DataFrame): Raw Data From the pybaseball API
    Returns:
        grouped_df(DataFrame): Calculated BABIP From Each Year. Year is specified in API Call Parameters
    """
    BABIP = (
        df.group_by("Year")
        .agg(
            [
                pl.col("H").sum(),
                pl.col("HR").sum(),
                pl.col("BB").sum(),
                pl.col("SF").sum(),
                pl.col("AB").sum(),
                pl.col("SO").sum(),
            ]
        )
        .with_columns(
            (
                (
                    (pl.col("H") - pl.col("HR"))
                    / (pl.col("AB") - pl.col("SO") - pl.col("HR") + pl.col("SF"))
                )
                .cast(pl.Float32)
                .alias("BABIP")
            )
        )
    )
    return BABIP


def create_plot(x: str, y: str, label: str, title: str):
    """
    Creates Plot Using the Matplotlib Library

    Args:
        x (str): x-axis
        y (str): y-axis
        label(str): plotting labels
        title(str):Title of Graph
    Returns:
        graph
    """
    graph = plt.plot(x, y, label=label)

    plt.title(title)
    plt.xlabel('BABIP')
    plt.ylabel('Year')

    plt.legend()
    plt.grid(True)
    return graph
