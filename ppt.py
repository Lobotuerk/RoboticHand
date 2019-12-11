from __future__ import print_function
from myo.utils import TimeInterval
import keyboard
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

  def on_connected(self, event):
    event.device.request_rssi()

  def on_pose(self, event):
    self.pose = event.pose
    if self.pose == myo.Pose.fist:
        #self.locked = not self.locked
        print(self.locked)
        print("fist")
    if self.pose == myo.Pose.rest:
        print("rest")
    if self.pose == myo.Pose.wave_in and not self.locked:
        keyboard.press_and_release("left_arrow")
        print("Wave In")
    if self.pose == myo.Pose.wave_out and not self.locked:
        keyboard.press_and_release("right_arrow")
        print("Wave out")
    if self.pose == myo.Pose.fingers_spread:
        print("Fingers Spread")


if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 1000):
    pass
