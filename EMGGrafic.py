from __future__ import print_function
from matplotlib import pyplot as plt
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

  # Create the axes for the plot.
  fig = plt.figure()
  axes = [fig.add_subplot('81' + str(i)) for i in range(1, 9)]
  [(ax.set_ylim([-255, 255])) for ax in axes]
  graphs = [ax.plot(np.arange(queue_size), np.zeros(queue_size))[0] for ax in axes]
  plt.ion()

  def plot_main():
    emgs = np.array([x[1] for x in listener.get_emg_data()]).T
    for g, data in zip(graphs, emgs):
      if len(data) < queue_size:
        data = np.concatenate([np.zeros(queue_size - len(data)), data])
      g.set_ydata(data)
    plt.draw()

  try:
    threading.Thread(target=lambda: hub.run_forever(listener.on_event)).start()
    while True:
      plot_main()
      plt.pause(0.0001)
  finally:
      hub.stop()  # Will also stop the thread


if __name__ == '__main__':
  main()
