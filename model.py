from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras import optimizers


n_epochs = 10
n_batchsize = 50
learning_rate = 0.001


def run_model(timesteps, x_train, y_train):

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

    return predicted_change