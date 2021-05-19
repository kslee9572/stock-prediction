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
import plot as plt

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
    #### Need to edit this part

    train_forward = 0
    n_training = 2000
    timesteps = 0
    repeat = 1

    all_data = np.zeros((10, 10, repeat))
    final_data = np.zeros((10, 10))

    for k in range(1):  ##change to x axis
        for j in range(1):  ## change to y axis

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

    test_data = [
        [36.0, 46.0, 54.0, 58.5, 24.5, 57.5, 63.0, 48.0, 52.0, 58.5],
        [52.0, 43.5, 54.5, 49.5, 44.0, 45.0, 58.5, 38.0, 69.0, 59.5],
        [33.5, 35.0, 56.0, 47.0, 61.0, 49.0, 63.0, 56.0, 57.5, 49.5],
        [33.0, 44.5, 48.5, 53.5, 49.5, 59.5, 64.0, 62.5, 49.5, 42.5],
        [40.0, 41.0, 53.0, 46.0, 55.0, 59.0, 46.5, 56.0, 51.0, 52.0],
        [28.0, 39.5, 53.5, 57.0, 60.5, 59.5, 58.0, 57.0, 69.0, 57.0],
        [32.5, 44.0, 42.5, 57.0, 59.5, 56.5, 61.0, 56.0, 66.0, 65.5],
        [34.0, 31.0, 47.0, 52.5, 56.5, 60.0, 63.0, 37.0, 52.5, 62.0],
        [27.0, 41.5, 56.0, 54.5, 57.0, 41.0, 61.0, 51.5, 56.5, 65.0],
        [28.0, 35.0, 50.0, 50.0, 60.0, 60.0, 45.0, 52.5, 64.5, 56.0],
    ]
    final_data = np.array(test_data)
    dt.report(final_data, user_input)
    plt.plot(100, 100, final_data)


##
## shows process of fetching data
##
def process_bar():

    pass


main()
