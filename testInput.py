from __future__ import print_function
from matplotlib import pyplot as plt
from myo.utils import TimeInterval
import collections
import myo
import numpy as np
import threading
import time
import os
import keyboard

class Listener(myo.DeviceListener):

  def __init__(self, queue_size=10):
    self.lock = threading.Lock()
    self.emg_data_queue = collections.deque(maxlen=queue_size)

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))

  def on_orientation(self, event):
    with self.lock:
      self.orientation = event.orientation
      self.acceleration = event.acceleration
      #self.emg_data_queue.append((event.timestamp, event.gyroscope))

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)


def main():
  queue_size = 10

  # Initialize Myo and create a Hub and our listener.
  myo.init()
  hub = myo.Hub()
  listener = Listener(queue_size)

  def update():
    emgs = np.array([x[1] for x in listener.get_emg_data()]).T
    for x in emgs:
        data = x
        if len(data) < queue_size:
            data = np.concatenate([np.zeros(queue_size - len(data)), data])
        word = 'Mean = %d , vector = ' %(data.mean())
        print(word + str(data))

  try:
    threading.Thread(target=lambda: hub.run_forever(listener.on_event)).start()
    time =  TimeInterval(None, 0.1)
    while True:
        if time.check_and_reset():
            os.system('cls')
            update()


  finally:
      hub.stop()  # Will also stop the thread


if __name__ == '__main__':
  main()
