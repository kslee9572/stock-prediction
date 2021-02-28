# API key: OS6T161LRRJ4V9N2
# pyenv activate stock_project
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas as pd
import time
import data as dt
import numpy as np
import preprocessing as pp
import model as md
import statistics as st

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

    ## Variables
    #### Need to makes these readable as well
    train_forward = 0
    n_training = 2000
    timesteps = 0
    repeat = 4

    all_data = np.zeros((10, 10, repeat))
    final_data = np.zeros((10, 10))

    for k in range(10):
        for j in range(10):

            timesteps = 10 * (j + 1)
            forecast_days = 10 * (k + 1)
            n_testing = timesteps + 70
            temp = np.zeros(repeat)

            for i in range(repeat):
                train_forward = 500 * i + 500

                x_data = dt.to_techin(data, forecast_days)
                y_data = dt.to_updown(data, forecast_days, len(x_data))

                toolbox = pp.pptoolbox(
                    x_data, train_forward, n_training, n_testing, timesteps
                )

                x_train = toolbox.x_train()
                x_test = toolbox.x_test()
                y_train = toolbox.y_train(y_data)
                y_test = toolbox.y_test(y_data)

                temp[i] = md.run_model(timesteps, x_train, y_train, x_test, y_test)
                all_data[k, j, i] = temp[i]
                final_data[k, j] = st.median(temp)

    # give final_data to plot.py
    # give user statistical report
    ##finsih!!!!


##
## shows process of fetching data
##
def process_bar():

    pass


main()
