from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras import optimizers
import numpy as np


""" 

    Part that runs model.

"""

n_epochs = 10
n_batchsize = 50
learning_rate = 0.001


def run_model(timesteps, x_train, y_train, x_test, y_test):

    n_features = x_train.shape[2]

    model = Sequential()
    model.add(
        LSTM(
            units=70,
            name="lstm_input",
            return_sequences=True,
            input_shape=(timesteps, n_features),
        )
    )
    model.add(Dropout(0.2, name="lstm_dropout_1"))
    model.add(LSTM(units=70, name="lstm_1"))
    model.add(Dense(units=1, name="dense_out", activation="sigmoid"))

    adam = optimizers.Adam(learning_rate)
    model.compile(optimizer=adam, loss="binary_crossentropy", metrics=["Accuracy"])
    history = model.fit(x_train, y_train, epochs=n_epochs, batch_size=n_batchsize)
    predicted_change = model.predict(x_test)

    binary_data = data_to_binary(predicted_change)

    return accuracy(binary_data, y_test)


def data_to_binary(predicted_change):

    predicted_change = np.reshape(predicted_change, len(predicted_change))

    for i in range(len(predicted_change)):
        if predicted_change[i] > 0.5:
            predicted_change[i] = 1
        else:
            predicted_change[i] = 0

    return predicted_change


def accuracy(predicted_change, y_test):

    counter = 0

    for i in range(len(predicted_change)):
        if predicted_change[i] == y_test[i]:
            counter += 1
    counter / len(predicted_change)

    return counter