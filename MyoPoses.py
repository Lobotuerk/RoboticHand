from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys
import os
from funciones import send

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
    self.arduino = serial.Serial('COM9', 9600)

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
    send(vector,arduino)


if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 1000):
    pass
