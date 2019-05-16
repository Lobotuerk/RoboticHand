from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys
import os


class Listener(myo.DeviceListener):

  def __init__(self):
    self.interval = TimeInterval(None, 0.05)
    self.acceleration = None
    self.gyroscope = None
    self.orientation = None
    self.pose = myo.Pose.rest
    self.emg_enabled = True
    self.locked = False
    self.rssi = None
    self.emg = None
    self.temp = 0

  def output(self):
     if not self.interval.check_and_reset():
        return
     self.temp = self.temp + 1
     if self.temp == 5:
        self.temp = 0
        os.system('cls')
        parts = []
        if self.orientation:
           parts.append("Orientation")
           for comp in self.orientation:
              parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
           parts.append('\n')
        if self.acceleration:
           parts.append("Acceleration")
           for comp in self.acceleration:
              parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
           parts.append('\n')
        if self.gyroscope:
           parts.append("Gyroscope")
           for comp in self.gyroscope:
              parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
           parts.append('\n')
        #parts.append(str(self.pose).ljust(10))
        #parts.append('E' if self.emg_enabled else ' ')
        #parts.append('L' if self.locked else ' ')
        #parts.append(self.rssi or 'NORSSI')
        if self.emg:
            parts.append("EMG")
            for comp in self.emg:
                parts.append(str(comp).ljust(5))
        os.system('cls')
        print('\r' + ''.join('[{}]'.format(p) for p in parts), end='')


  def on_connected(self, event):
    event.device.request_rssi()
    event.device.stream_emg(True)

  def on_rssi(self, event):
    self.rssi = event.rssi
    self.output()

  def on_orientation(self, event):
    self.orientation = event.orientation
    self.acceleration = event.acceleration
    self.gyroscope = event.gyroscope
    self.output()

  def on_emg(self, event):
    self.emg = event.emg
    self.output()

  def on_unlocked(self, event):
    self.locked = False
    self.output()

  def on_locked(self, event):
    self.locked = True
    self.output()


if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 1):
    pass
