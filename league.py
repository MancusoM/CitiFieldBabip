"""this file generates a png visualizing BABIP at/away from Citi Field"""

from teams_list import teams
from helper import babipCalculator, create_plot
import pybaseball as pyb
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


def retrieve_team_api_data(teams: dict) -> pl.DataFrame:
    """
    Retrieves raw data from 'team_game_logs' function from pybaseball

    :param teams: a predefined list of team names from teams.py.
        Key: Team Code; Value: Team Name
    :return:apiReturn:pl.DataFrame:team-level data from api
    """
    apiReturn = pl.DataFrame()
    # Retrieving Data For The Years Citi Field Is Open
    for year in range(2009, 2025):
        if year == 2020:
            continue

        # For Team in Year
        for key, value in teams.items():
            try:
                battingLogs = pyb.team_game_logs(year, value, "batting")
                teamBattingLogs = pl.from_pandas(battingLogs)
                print(f"Successfully Processed: {year} {key}")
            except RuntimeError:
                battingLogs = pyb.team_game_logs(year, "FLA", "batting")
                teamBattingLogs = pl.from_pandas(battingLogs)
                print(f"Successfully Processed: {year} {key}")

            teamBattingLogs = teamBattingLogs.with_columns(
                Year=pl.lit(year), Team=pl.lit(value)
            )
            apiReturn = pl.concat([apiReturn, teamBattingLogs])
    return apiReturn


def filter_and_process_team_data(
    apiReturn: pl.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    :param apiReturn: pl.DataFrame:raw team-level data from api
    :return:
        gamesNotAtCitiPandas:pd.DataFrame: BABIP From Games Not at Citi Field
        gamesAtCitiPandas:pd.DataFrame: BABIP From Games At Citi Field
    """
    gamesAtCiti = apiReturn.filter(
        ((pl.col("Team") == "NYM") & (pl.col("Home") == True))
        | ((pl.col("Opp") == "NYM") & (pl.col("Home") == False))
    )
    gamesNotAtCiti = apiReturn.filter(
        (pl.col("Team") != "NYM")
        | ((pl.col("Opp") == "NYM") & (pl.col("Home") == True))
    )

    # Calculate BABIP and convert to pandas
    gamesAtCitiPandas = babipCalculator(gamesAtCiti).to_pandas()
    gamesNotAtCitiPandas = babipCalculator(gamesNotAtCiti).to_pandas()

    return gamesAtCitiPandas, gamesNotAtCitiPandas


def show_team_plot(
    gamesAtCitiPandas: pl.DataFrame, gamesNotAtCitiPandas: pl.DataFrame
) -> None:
    """
    :param:
        gamesNotAtCitiPandas:pd.DataFrame: Aggregated BABIP Stats From Games Not at Citi Field
        gamesAtCitiPandas:pd.DataFrame: Aggregated BABIP Stats From Games At Citi Field
    """
    # Create Plot
    CitiBABIP = create_plot(
        gamesAtCitiPandas["Year"],
        gamesAtCitiPandas["BABIP"],
        "Citi Field BABIP",
        "BABIP @ Citi Field vs Away",
    )
    AwayBABIP = create_plot(
        gamesNotAtCitiPandas["Year"],
        gamesNotAtCitiPandas["BABIP"],
        "Away BABIP",
        "BABIP @ Citi Field vs Away",
    )

    plt.show()


def main():
    apiTeamsReturn = retrieve_team_api_data(teams)
    gamesAtCitiPandas, gamesNotAtCitiPandas = filter_and_process_team_data(
        apiTeamsReturn
    )
    show_team_plot(gamesAtCitiPandas, gamesNotAtCitiPandas)


main()
