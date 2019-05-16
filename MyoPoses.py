from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys
import os

import serial


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
    self.arduino = serial.Serial('COM14', 9600)

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
        if self.acceleration:
           parts.append("Acceleration")
           for comp in self.acceleration:
              parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
        if self.gyroscope:
           parts.append("Gyroscope")
           for comp in self.gyroscope:
              parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
        #parts.append(str(self.pose).ljust(10))
        #parts.append('E' if self.emg_enabled else ' ')
        #parts.append('L' if self.locked else ' ')
        #parts.append(self.rssi or 'NORSSI')
        if self.emg:
           for comp in self.emg:
              parts.append(str(comp).ljust(5))
        os.system('cls')
        print('\r' + ''.join('[{}]'.format(p) for p in parts), end='')


  def on_connected(self, event):
    event.device.request_rssi()

  def on_pose(self, event):
    self.pose = event.pose
    vector = [0, 0, 0 ,0 ,0]
    if self.pose == myo.Pose.fist:
        vector = [80, 80, 80 ,80 ,80]
        print("fist")
    if self.pose == myo.Pose.rest:
        vector = [0, 0, 0 ,0 ,0]
        print("rest")
    if self.pose == myo.Pose.wave_in:
        vector = vector = [70,80,0,0,0]
        print("Wave In")
    if self.pose == myo.Pose.wave_out:
        vector = [80,0,80,80,0]
        print("Wave out")
    if self.pose == myo.Pose.fingers_spread:
        vector = [80,0,80,80,80]
        print("Fingers Spread")
    for x in vector:
        rnd = str(x) + ','
        self.arduino.write(rnd.encode('utf-8'))
    #self.output()


if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 1000):
    pass
