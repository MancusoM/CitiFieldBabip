import polars as pl
import matplotlib.pyplot as plt


def aggregation_polars(df):
    grouped_polars = (
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
    return grouped_polars


def create_plot(x, y, label, title):
    graph = plt.plot(x, y, label=label)

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("BABIP")

    plt.legend()
    plt.grid(True)
    return graph
