import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam, RMSprop
import os

Y = np.loadtxt("TestY.csv", delimiter=",")
X = np.loadtxt("TestX.csv", delimiter=",")

X = (((X - np.amin(X)) * (1)) / (np.amax(X) - np.amin(X)))
Y = (((Y - np.amin(Y)) * (1)) / (np.amax(Y) - np.amin(Y)))

Y = np.round(Y * 9)
X = np.round(X, decimals=2)

config = tf.ConfigProto( device_count = {'GPU': 4})
sess = tf.Session(config=config)
tf.keras.backend.set_session(sess)


model = Sequential()
model.add(Dense(528, input_dim=X.shape[1]))
model.add(Activation('relu'))
#model.add(Dropout(0.2))
model.add(Dense(786))
model.add(Activation('relu'))
#model.add(Dropout(0.2))
model.add(Dense(1248))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(9))
model.add(Activation('softmax'))
NAME = 'logsC/CLASSIFICATION-SINGLEFINGER'
print(NAME)

tensorboard = TensorBoard(log_dir=NAME)
#optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.01, amsgrad=False)
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimiser, metrics=['accuracy'])
model.fit(X, Y[:,0], epochs=1000, batch_size=32, validation_split=0.15, callbacks=[tensorboard])
model.save(os.path.join(NAME, 'modelo.h5'))
