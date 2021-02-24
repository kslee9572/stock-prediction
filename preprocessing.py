from sklearn.preprocessing import MinMaxScaler
import numpy as np


class pptoolbox:

    """ toolbox for preprocessing data for training/testing """

    def __init__(self, x_data, train_forward, n_training, n_testing, timesteps):
        self.train_forward = train_forward
        self.n_training = n_training
        self.n_testing = n_testing
        self.timesteps = timesteps
        self.train_data = x_data[train_forward : train_forward + n_training]
        self.test_data = x_data[train_forward + n_training :]

    def normalize(self, train):
        sc = MinMaxScaler(feature_range=(0, 1))

        # empty shells
        shell_train = np.zeros((self.train_data.shape[0], self.train_data.shape[1]))
        shell_test = np.zeros((self.test_data.shape[0], self.test_data.shape[1]))

        # normalize by columns
        for i in range(self.train_data.shape[1]):
            shell_train[:, i] = np.reshape(
                sc.fit_transform(
                    np.reshape(self.train_data[:, i], (len(self.train_data), 1))
                ),
                len(self.train_data),
            )

            shell_test[:, i] = np.reshape(
                sc.transform(
                    np.reshape(self.test_data[:, i], (len(self.test_data), 1))
                ),
                len(self.test_data),
            )

        x_train_raw = shell_train
        x_test_raw = shell_test[: self.n_testing]

        if train:
            return x_train_raw
        else:
            return x_test_raw

    def y_train(self, updown):
        return updown[
            self.timesteps
            - 1
            + self.train_forward : self.n_training
            - 1
            + self.train_forward
        ]

    def y_test(self, updown):
        return updown[
            self.train_forward
            + self.n_training
            + self.timesteps
            - 1 : self.train_forward
            + self.n_testing
            + self.n_training
            - 1
        ]

    def x_train(self):
        x_raw = self.normalize(True)

        xtrain = []
        for i in range(self.timesteps, len(x_raw)):
            xtrain.append(x_raw[i - self.timesteps : i, : x_raw.shape[1]])

        xtrain = np.array(xtrain)
        return xtrain

    def x_test(self):
        x_raw = self.normalize(False)

        xtest = []
        for i in range(self.timesteps, len(x_raw)):
            xtest.append(x_raw[i - self.timesteps : i, : x_raw.shape[1]])

        xtest = np.array(xtest)
        return xtest
