from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras.optimizers import Adadelta
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import _pickle as pickle


class Songwriter():
    def __init__(self):
        self.__model = Sequential()

    def add_middle_layer(self, n_neurons, input_shape):
        self.__model.add(LSTM((n_neurons), input_shape=input_shape, return_sequences=True))
        self.__model.add(Dropout(0.2))
    
    def add_final_layer(self, n_neurons, input_shape=None):
        if input_shape:
            self.__model.add(LSTM((n_neurons), input_shape=input_shape, return_sequences=False))
            self.__model.add(Dense(input_shape[1]))
        else:
            self.__model.add(LSTM((n_neurons), return_sequences=False))
        self.__model.add(Activation('softmax'))

    def train(self, data, epochs=20, save=False, plot=False):
        self.__model.compile(optimizer=Adadelta(lr=0.05), loss='categorical_crossentropy')
        self.__model.summary()
        self.history = self.__model.fit(data[0], data[1], epochs=epochs, batch_size=256)
        if plot:
            self.plot_loss()
        if self.__model_exists() and save:
            self.__shouldOverwrite()
        return self.history
    
    def predict(self, data):
        probs = self.__model.predict(data)
        probs = np.reshape(probs, probs.shape[1])
        return probs

    def save_model(self):
        self.__model.save('model.h5')
        self.__model.summary()
        print('Model saved to disk!')

    def load_model(self):
        self.__model = load_model('model.h5')
        print('Model loaded!')
        return self.__model
    
    def __model_exists(self):
        if 'model.h5' in os.listdir():
            return True
        return False
    
    def __shouldOverwrite(self):
        r = input("There is model saved. Do you want to overwrite it? [y]/n: ")
        if r.lower() != 'n':
            self.save_model()
    
    def plot_loss(self):
        _, ax = plt.subplots(1)
        ax.plot(self.history.history['loss'])
        ax.set_ylim(ymin=0)
        plt.show()