from teams_list import teams
from helper import aggregation_polars, create_plot
import pandas as pd
import pybaseball as pyb
import polars as pl
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

teams_df_polars = pl.DataFrame()
errors_list = []
for year in range(2009, 2025):
    if year == 2020:
        continue
    for key, value in teams.items():
        print(f"Processing: {year} {key}")
        try:
            batting_logs = pyb.team_game_logs(year, value, "batting")

            batting_logs_polars = pl.from_pandas(batting_logs)

        except Exception as e:
            errors_list.append([key, value])
            continue
            # raise KeyError(f"Error Retrieving Team: {e}")
        batting_logs_polars = batting_logs_polars.with_columns(
            Year=pl.lit(year), Team=pl.lit(value)
        )

        teams_df_polars = pl.concat([teams_df_polars, batting_logs_polars])

Citi_df_polars = teams_df_polars.filter(
    ((pl.col("Team") == "NYM") & (pl.col("Home") == True))
    | ((pl.col("Opp") == "NYM") & (pl.col("Home") == False))
)

Not_Citi_df_polars = teams_df_polars.filter(
    (pl.col("Team") != "NYM") | ((pl.col("Opp") == "NYM") & (pl.col("Home") == True))
)

grouped_citi_games = aggregation_polars(Citi_df_polars).to_pandas()
grouped_non_citi_games = aggregation_polars(Not_Citi_df_polars).to_pandas()

CitiGraph = create_plot(
    grouped_citi_games["Year"],
    grouped_citi_games["BABIP"],
    "Citi Field BABIP",
    "Citi Field vs Away BABIP",
)
nonCitiGraph = create_plot(
    grouped_citi_games["Year"],
    grouped_non_citi_games["BABIP"],
    "Away BABIP",
    "Citi Field vs Away BABIP",
)

plt.show()

print(errors_list)
