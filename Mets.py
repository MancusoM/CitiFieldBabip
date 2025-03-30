import pybaseball as pyb
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple

from helper import babipCalculator, create_plot
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def retrieveMetsAPIData()->pl.DataFrame:
    """
    Calls The Function 'team_game_logs' from pybaseball package
    :return: Mets_df_polars:pl.DataFrame: Raw Data From 'team_game_logs' function
    """
    initialDf = pl.DataFrame()
    # For Each Year Citi Field's Been Open
    for year in range(2009, 2025):
        #Ignore 2020
        if year == 2020:
            continue
        try:
            batting_logs = pyb.team_game_logs(year, "NYM", "batting")
        except Exception:
            raise ValueError(Exception)
        MetsYearReturn = pl.from_pandas(batting_logs)

        #Adds Year To Return
        MetsYearReturn = MetsYearReturn.with_columns(
            Year=pl.lit(year)
        )

        #Stacks Each Year's Return on Top of Another
        initialDf = pl.concat([initialDf, MetsYearReturn])
    return initialDf

def filterAndProcessData(apiReturn:pl.DataFrame)->Tuple[pd.DataFrame,pd.DataFrame]:
    """
    :param apiReturn:pl.DataFrame: DataFrame containing api Data
    :return: metsHomeGamesPandas:pd.DataFrame: Mets Home BABIP
    :return: metsAwayGamesPandas:pd.DataFrame: Mets Away BABIP
    """
    # Filter to Citi Field games & Calculates BABIP
    metsHomeGames = apiReturn.filter(pl.col("Home") == True)

    # Filter To Away Games & Calculates BABIP
    metsAwayGames = apiReturn.filter(pl.col("Home") == False)

    # Convert from Polars DF to Pandas DF for visualization
    groupedMetsHomeGames = babipCalculator(metsHomeGames).to_pandas()
    groupedMetsAwayGames = babipCalculator(metsAwayGames).to_pandas()

    return groupedMetsHomeGames, groupedMetsAwayGames


def displayMetsPlot(groupedMetsHomeGames, groupedMetsAwayGames)-> None:
    """
    :param: metsHomeGamesPandas:pd.DataFrame: Mets Home BABIP
    :param: metsAwayGamesPandas:pd.DataFrame: Mets Away BABIP
    :return:
    """
    # Create Plot
    MetsHomeGraph = create_plot(
        groupedMetsHomeGames["Year"],
        groupedMetsHomeGames["BABIP"],
        "Home BABIP",
        "Mets BABIP:Home vs Away",
    )
    MetsAwayGraph = create_plot(
        groupedMetsAwayGames["Year"],
        groupedMetsAwayGames["BABIP"],
        "Away BABIP",
        "Mets BABIP: Home vs Away",
    )

    plt.show()
def main():
    apiReturn = retrieveMetsAPIData()
    groupedMetsHomeGames, groupedMetsAwayGames = filterAndProcessData(apiReturn)
    displayMetsPlot(groupedMetsHomeGames, groupedMetsAwayGames)
main()