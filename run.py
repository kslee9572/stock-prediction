# API key: OS6T161LRRJ4V9N2
# pyenv activate stock_project
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas as pd
import time
import data as dt
import numpy as np
import preprocessing as pp

""" 

    Part that interacts with user.
    Asks user for name of ticke to be analyzed.
    Initializes main variables for analysis.

"""


def main():
    tickers = pd.read_csv("./Nasdaq_Screeners.csv")["Symbol"].tolist()

    ## asks user for the ticker to be analyzed
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

    ## asks user to specify two main variables for analyzing
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

    x_data = dt.to_techin(data, forecast_days, tech_days)
    y_data = dt.to_updown(data, forecast_days, tech_days, len(x_data))

    ##variables
    #### Need to makes these readable as well
    train_forward = 10
    n_training = 2000
    n_testing = 1000
    timesteps = 10

    toolbox = pp.pptoolbox(x_data, train_forward, n_training, n_testing, timesteps)

    x_train = toolbox.x_train()
    x_test = toolbox.x_test()
    y_train = toolbox.y_train(y_data)
    y_test = toolbox.y_test(y_data)

    ##data now ready to enter model

    # construct for loop to loop for entire matrix
    # give that data to plot.py
    # give user statistical report
    ##finsih!!!!


##
## shows process of fetching data
##
def process_bar():

    pass


main()
