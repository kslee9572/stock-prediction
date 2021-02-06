# API key: OS6T161LRRJ4V9N2
# source /Users/kslee9572/.pyenv/versions/stock_project/bin/activate
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas as pd
import time
import data as dt
import numpy as np

""" 

    Part that interacts with user. Asks for ticker that user wants analysis.

"""


def main():
    tickers = pd.read_csv("./Nasdaq_Screeners.csv")["Symbol"].tolist()

    while True:
        print("Type symbol of stock to be analyzed: ")
        user_input = input()

        if user_input.upper() in tickers:
            print("Ticker validation successful")
            ts = TimeSeries(key="OS6T161LRRJ4V9N2", output_format="pandas")
            data, meta_data = ts.get_daily_adjusted(
                symbol=user_input, outputsize="full"
            )
            break

        print("Invalid tickerv: try different ticker")

    # pprint(data.head)

    # need to take in user inputs for model
    print("Specify forecast days and learning days")
    print("Forecast days between 1 and 50, learning days between 1 and 100")
    while True:

        print("Forecast Days :")
        forecast_days = int(input())

        if forecast_days > 0 and forecast_days < 50:
            forecast_days = round(forecast_days)
            break
        print("Invalid forecast days")

    while True:

        print("Learning Days :")
        tech_days = int(input())

        if tech_days > 0 and tech_days < 50:
            tech_days = round(tech_days)
            break
        print("Invalid learning days")

    dataset = dt.to_techin(data, forecast_days, tech_days)
    # print(dataset)


## shows process of fetching data


def process_bar():

    pass


## takes in data from alpha vantage
## cleans up so it can run on the model


main()
