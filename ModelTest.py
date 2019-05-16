import myo
import numpy as np
import time
import os
import keyboard
import threading
import collections
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model

Pulgar = [0,1,2,3]
Indice = [0,1,2,3,4,5,6]
Mayor = [0,1,2,3,4,5,6]
Anular = [0,1,2,3,4,5,6]
Menique = [0,1,2,3,4,5,6]

class Listener(myo.DeviceListener):

  def __init__(self, queue_size=8):
    self.lock = threading.Lock()
    self.emg_data_queue = collections.deque(maxlen=queue_size)

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)


def step(listener):
    emgs = np.array([x[1] for x in listener.get_emg_data()])
    return emgs

def main(model):
    numb = 0
    queue_size=10
    myo.init()
    hub = myo.Hub()
    listener = Listener(queue_size)
    try:
        threading.Thread(target=lambda: hub.run_forever(listener.on_event)).start()
        t = 0
        flag = 0
        data = []
        while True:
            emgs = step(listener)
            if len(emgs) != 10:
                continue
            if len(data) < 50:
                emgs = tf.keras.utils.normalize(emgs, axis = 0)
                data.append(emgs.reshape(1,80))
                continue
            else:
                predictions = []
                for x in data:
                    predictions.append(model.predict(x).argmax())
                os.system('cls')
                #print(predictions)
                data = []
                print(np.bincount(predictions).argmax())
    finally:
        hub.stop()

if __name__ == '__main__':
    '''Y = np.loadtxt("datasets/PruebaY.csv", delimiter=",")
    X = np.loadtxt("datasets/PruebaX.csv", delimiter=",")
    X = tf.keras.utils.normalize(X, axis=1)
    Y = Y.astype(int)
    config = tf.ConfigProto( device_count = {'GPU': 1})
    sess = tf.Session(config=config)
    tf.keras.backend.set_session(sess)
    model = Sequential()
    model.add(Dense(128, input_dim=X.shape[1]))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(Dense(7))
    model.add(Activation('softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, Y[0:,3], epochs=300, batch_size=32)'''
    model = load_model("modelo.h5")
    main(model)
