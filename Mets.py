import pybaseball as pyb
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt

from helper import aggregation_polars

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.DataFrame()
Mets_df_polars = pl.DataFrame()

# Mets specific analysis
for year in range(2009, 2025):
    if year == 2020:
        continue
    batting_logs = pyb.team_game_logs(year, "NYM", "batting")
    Mets_batting_logs_polars = pl.from_pandas(batting_logs)
    Mets_batting_logs_polars = Mets_batting_logs_polars.with_columns(Year=pl.lit(year))

    Mets_df_polars = pl.concat([Mets_df_polars, Mets_batting_logs_polars])

Mets_home_games = Mets_df_polars.filter(pl.col("Home") == True)
grouped_home_games_polars = aggregation_polars(Mets_home_games)

Mets_away_games = Mets_df_polars.filter(pl.col("Home") == False)
grouped_away_games_polars = aggregation_polars(Mets_away_games)

grouped_Mets_home_games = aggregation_polars(grouped_home_games_polars).to_pandas()
grouped_Mets_away_games = aggregation_polars(grouped_away_games_polars).to_pandas()

plt.plot(
    grouped_Mets_away_games["Year"],
    round(grouped_Mets_away_games["BABIP"], 4),
    label="Mets Away BABIP",
)
plt.plot(
    grouped_Mets_home_games["Year"],
    round(grouped_Mets_home_games["BABIP"], 4),
    label="Mets Home BABIP",
)

plt.title("Mets BABIP Home/Away")
plt.xlabel("Year")
plt.ylabel("BABIP")

plt.legend()
plt.grid(True)
plt.show()
