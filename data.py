import pandas as pd
import numpy as np
import technical_indicators as tech

""" 

    Part that does all the data preprocessing.

"""
##
## basic cleaning of data from api for better use.
## shapes raw data from alpha vantage to columns
## of numbers needed for converting to data feedible to neural networks
##
def alpha_clean(alpha_data, forecast_days, tech_days):

    ## dataset: raw data
    ## data : dataset converted to numpy
    dataset = alpha_data.drop(
        columns=["5. adjusted close", "7. dividend amount", "8. split coefficient"]
    )
    dataset = dataset.rename(columns={"6. volume": "5. volume"})

    data = dict()
    for value in dataset.columns:
        data[value] = dataset[value].to_numpy()

    return data


##
## returns raw x_data
## after cleanining data, converts them to technical indicators
##
def to_techin(alpha_data, forecast_days, tech_days):

    ## tech_data: data converted to technical indicators

    data = alpha_clean(alpha_data, forecast_days, tech_days)

    difference = np.zeros(len(data["4. close"]) - 1)
    for i in range(len(data["4. close"]) - 1):
        difference[i] = data["4. close"][i + 1] - data["4. close"][i]

    RSI = tech.RSI_Normal(difference, tech_days)
    MACD = tech.MACD(data["4. close"], tech_days)
    OBV = tech.OBV(data["5. volume"], data["4. close"])
    PRC = tech.PRC(data["4. close"], tech_days)
    Williams = tech.Williams(
        data["2. high"], data["3. low"], data["4. close"], tech_days
    )
    SOsc = tech.Stochastic_Oscillator(
        data["2. high"], data["3. low"], data["4. close"], tech_days
    )

    OBV = OBV[tech_days:-forecast_days]
    MACD = MACD[1:-forecast_days]
    Williams = Williams[1:-forecast_days]
    SOsc = SOsc[1:-forecast_days]
    RSI = RSI[:-forecast_days]
    PRC = PRC[:-forecast_days]

    tech_data = np.stack((RSI, MACD, PRC, Williams, SOsc, OBV), axis=1)

    return tech_data


##
## returns raw y_data
## creates binomial data representing 1 for a rise in price and 0 for a fall
##
## length must match the length of x_data!
##
def to_updown(alpha_data, forecast_days, tech_days, length):

    data = alpha_clean(alpha_data, forecast_days, tech_days)

    updown = np.zeros(length)
    for i in range(len(updown)):
        if (
            data["4. close"][i + tech_days + forecast_days]
            - data["4. close"][i + tech_days]
            >= 0
        ):
            updown[i] = 1
        else:
            updown[i] = 0

    return updown


class pptoolbox:

    """ toolbox for preprocessing data for training/testing """

    pass
