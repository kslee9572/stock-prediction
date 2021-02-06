import pandas as pd
import numpy as np
import technical_indicators as tech

## shapes raw data from alpha vantage to columns
## of technical indicator data


def to_techin(alpha_data, forecast_days, tech_days):

    dataset = alpha_data.drop(
        columns=["5. adjusted close", "7. dividend amount", "8. split coefficient"]
    )
    dataset = dataset.rename(columns={"6. volume": "5. volume"})

    data = dict()
    for value in dataset.columns:
        data[value] = dataset[value].to_numpy()

    difference = np.zeros(len(dataset) - 1)
    for i in range(len(dataset) - 1):
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
