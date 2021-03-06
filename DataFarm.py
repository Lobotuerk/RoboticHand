from __future__ import print_function
from matplotlib import pyplot as plt
import collections
import myo
import numpy as np
import threading
import time
import os
import keyboard
import serial
import random
import sys
from funciones import send



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


def main():
  arduino = serial.Serial('COM14', 9600)
  time.sleep(2)
  queue_size = 1
  temp = 0
  check = 0
  vector = [0, 0, 0 ,0 ,0]
  for x in range(5):
      vector[x] = random.randrange(100)
  # Initialize Myo and create a Hub and our listener.
  send(vector, arduino)
  myo.init()
  hub = myo.Hub()
  listener = Listener(queue_size)

  # Create the axes for the plot.
  def plot_main(temp,check):
    flag = check
    emgs = np.array([x[1] for x in listener.get_emg_data()])
    if temp == 1200:
        os.system('cls')
        print(''.join('{}'.format(p) for p in emgs))
        print(vector)
        print(' flag: ' + str(flag))
    if keyboard.is_pressed('s') and flag == 0:
        f = open('InputX.csv','a')
        vectornp = np.asarray(vector)
        vectornp = vectornp / 100
        np.savetxt(f, emgs, delimiter=",")
        f.close()
        f = open('OutputY.csv','a')
        vectornp = vectornp.reshape(1,5)
        np.savetxt(f, vectornp, delimiter=",")
        f.close()
        flag = flag + 10000
        for x in range(5):
            vector[x] = random.randrange(100)
        send(vector, arduino)
    if keyboard.is_pressed('q'):
        hub.stop()
        send([0,0,0,0,0], arduino)
        arduino.close()
        sys.exit()
    return flag

  try:
    threading.Thread(target=lambda: hub.run_forever(listener.on_event)).start()
    while True:
      temp = temp + 1
      check = plot_main(temp,check)
      if temp == 1200:
          temp = 0
      if check > 0:
          check = check - 1
  finally:
    hub.stop()  # Will also stop the thread


if __name__ == '__main__':
  main()
