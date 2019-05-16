import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
import os

Y = np.loadtxt("TestY.csv", delimiter=",")
X = np.loadtxt("TestX.csv", delimiter=",")

X = (((X - np.amin(X)) * (1)) / (np.amax(X) - np.amin(X)))
Y = (((Y - np.amin(Y)) * (1)) / (np.amax(Y) - np.amin(Y)))

Y = np.round(Y, decimals=1)
X = np.round(X, decimals=1)

config = tf.ConfigProto( device_count = {'GPU': 4})
sess = tf.Session(config=config)
tf.keras.backend.set_session(sess)

LOSS = ['mean_squared_error', 'mean_absolute_error']
DENSE = [1,2,8,16,32]
SIZE = [2,4,8,16,32,64,128]
SINGLE = [True,False]

for single in SINGLE:
    for size in SIZE:
        for loss in LOSS:
            for numb_layers in DENSE:
                model = Sequential()
                model.add(Dense(10, input_dim=X.shape[1]))
                model.add(Activation('relu'))
                model.add(Dropout(0.2))
                for i in range(numb_layers):
                    model.add(Dense(size))
                    model.add(Activation('relu'))
                    model.add(Dropout(0.2))

                if single:
                    model.add(Dense(1))
                    model.add(Activation('sigmoid'))
                    NAME = 'logs/{}layers-{}size-{}-Single-{}'.format(numb_layers,size,loss,int(time.time()))

                else:
                    model.add(Dense(5))
                    model.add(Activation('sigmoid'))
                    NAME = 'logs/{}layers-{}size-{}-Multi-{}'.format(numb_layers,size,loss,int(time.time()))
                print(NAME)

                tensorboard = TensorBoard(log_dir=NAME)
                adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.01, amsgrad=False)
                model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])
                if single:
                    model.fit(X, Y[:,0], epochs=100, batch_size=30, validation_split=0.15, callbacks=[tensorboard])
                else:
                    model.fit(X, Y, epochs=100, batch_size=30, validation_split=0.15, callbacks=[tensorboard])
                model.save(os.path.join(NAME, 'modelo.h5'))
