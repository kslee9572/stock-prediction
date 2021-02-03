# API key: OS6T161LRRJ4V9N2
# source /Users/kslee9572/.pyenv/versions/stock_project/bin/activate
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas as pd
import time


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

    pprint(data.head)


main()
