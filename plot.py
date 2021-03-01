# returns a heat map as a result

import matplotlib.pyplot as plt
import numpy as np


def plot(x_max, y_max, data):
    x = np.arange(10, x_max + 1, 10)
    y = np.arange(10, y_max + 1, 10)

    plot = plt.contourf(x, y, data, cmap=plt.cm.coolwarm)
    plt.title("Accuracy")
    plt.ylabel("Forecast Days")
    plt.xlabel("Timesteps")

    plt.show()