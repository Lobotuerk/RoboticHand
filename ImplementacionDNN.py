from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys
import os
import numpy as np
from sklearn.model_selection import train_test_split as ts
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

import serial


class Listener(myo.DeviceListener):

    def __init__(self, model):
        self.vecout = None
        self.model = model
        self.interval = TimeInterval(None, 0.50)
        self.acceleration = None
        self.gyroscope = None
        self.orientation = None
        self.pose = myo.Pose.rest
        self.emg_enabled = True
        self.locked = False
        self.rssi = None
        self.emg = None
        self.temp = 0
        self.arduino = serial.Serial('COM14', 9600)

    def output(self):
        if not self.interval.check_and_reset():
            return
        self.temp = self.temp + 1
        if self.temp == 5:
            self.temp = 0
        os.system('cls')
        parts = []
        if self.emg:
            for comp in self.emg:
                parts.append(str(comp).ljust(5))
        vectornp = np.array(parts, dtype='float32')
        if (vectornp.shape[0] > 0):
            vectornp = vectornp.reshape((8,1))
            vectornp = vectornp / 90.0
            self.vecout = self.model.predict(vectornp.T, batch_size=None, verbose=0, steps=None)
            self.vecout = self.vecout * 100
            temp = self.vecout[0].tolist()
            for x in temp:
                rnd = str(x) + ','
                #print('Sending ' + rnd )
                self.arduino.write(rnd.encode('utf-8'))
                #rawString = self.arduino.readline()
                #print(rawString)
        print(self.vecout)

    def on_emg(self, event):
        self.emg = event.emg
        self.output()


    def on_connected(self, event):
        event.device.request_rssi()
        event.device.stream_emg(True)

    def on_rssi(self, event):
      self.rssi = event.rssi
      self.output()


if __name__ == '__main__':
  myo.init()
  model = load_model('modelo.h5')
  hub = myo.Hub()
  listener = Listener(model)
  while hub.run(listener.on_event, 1000):
    pass
