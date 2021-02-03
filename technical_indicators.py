import numpy as np


def RSI_Normal(difference, n_days):
    x = difference
    n = n_days

    # SMA
    sma_up = 0
    sma_down = 0
    for i in range(n):
        if x[i] > 0:
            sma_up += x[i]
        else:
            sma_down += x[i] * -1

    sma_up = sma_up / n
    sma_down = sma_down / n
    # SMMA
    smma_up = np.zeros(len(x) - n + 1)
    smma_down = np.zeros(len(x) - n + 1)
    smma_up[0] = sma_up
    smma_down[0] = sma_down

    for i in range(n, len(x)):
        if x[i] > 0:
            smma_up[i - n + 1] = (x[i] + (n - 1) * smma_up[i - n]) / n
            smma_down[i - n + 1] = (n - 1) * smma_down[i - n] / n
        else:
            smma_up[i - n + 1] = (n - 1) * smma_up[i - n] / n
            smma_down[i - n + 1] = (x[i] * (-1) + (n - 1) * smma_down[i - n]) / n
    # RS
    RS = np.zeros(len(smma_up))
    RSI = np.zeros(len(smma_up))
    for i in range(len(RS)):
        RS[i] = smma_up[i] / smma_down[i]
        RSI[i] = 100 - 100 / (1 + RS[i])

    return RSI


def Exp_Smoothing(x, n):
    alpha = 1 / n
    y = np.zeros(len(x))
    y[0] = x[0]
    for i in range(len(y) - 1):
        y[i + 1] = alpha * x[i + 1] + (1 - alpha) * y[i]

    return y


def RSI_Smoothed(difference, n_days):
    x = difference
    n = n_days

    av_up = np.zeros(len(x) - n + 1)
    av_down = np.zeros(len(x) - n + 1)
    up = 0
    down = 0
    for i in range(len(x) - n + 1):
        for j in range(n):
            if x[j + i] > 0:
                up += x[j + i]
            else:
                down += x[j + i] * -1
        av_up[i] = up / n
        av_down[i] = down / n
        up = 0
        down = 0

    RS = np.zeros(len(av_up))
    RSI = np.zeros(len(av_up))
    for i in range(len(RS)):
        if av_down[i] == 0:
            RS[i] = 0
            RSI[i] = 0
        else:
            RS[i] = av_up[i] / av_down[i]
            RSI[i] = 100 - 100 / (1 + RS[i])

    return RSI


def MACD(closing_price, n):
    smooth = 2 / (n + 1)
    initial_ema = 0
    x = closing_price
    MACD = np.zeros(len(x) - n + 1)

    for i in range(n):
        initial_ema += x[i]
    initial_ema = initial_ema / n

    MACD[0] = initial_ema

    for i in range(n, len(x)):
        MACD[i - n + 1] = x[i] * smooth + MACD[i - n] * (1 - smooth)

    return MACD


def OBV(volume, close):
    # Should On-Balance-Volume Data be normalised by itself?
    OBV = np.zeros(len(close))
    OBV[0] = volume[0]

    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            OBV[i] = OBV[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            OBV[i] = OBV[i - 1] - volume[i]
        else:
            OBV[i] = OBV[i - 1]

    return OBV


def PRC(close, n_days):
    n = n_days
    PRC = np.zeros(len(close) - n)
    for i in range(n, len(close)):
        PRC[i - n] = (close[i] - close[i - n]) / close[i - n] * 100

    return PRC


def Williams(high, low, close, n_days):
    n = n_days
    Williams = np.zeros(len(high) - n + 1)
    for i in range(n, len(high) + 1):
        temp_high = high[i - n : i]
        temp_low = low[i - n : i]
        High_n = np.amax(temp_high)
        Low_n = np.amin(temp_low)
        Williams[i - n] = (High_n - close[i - 1]) / (High_n - Low_n) * (-100)

    return Williams


def Stochastic_Oscillator(high, low, close, n_days):
    n = n_days
    StochOsc = np.zeros(len(high) - n + 1)
    for i in range(n, len(high) + 1):
        temp_high = high[i - n : i]
        temp_low = low[i - n : i]
        High_n = np.amax(temp_high)
        Low_n = np.amin(temp_low)
        StochOsc[i - n] = (close[i - 1] - Low_n) / (High_n - Low_n) * 100

    return StochOsc
