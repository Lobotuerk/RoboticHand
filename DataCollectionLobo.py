import myo
import numpy as np
import time
import os
import keyboard
import threading
import collections
import sys

Pulgar = [0,1,2,3]
Indice = [0,1,2,3,4,5,6]
Mayor = [0,1,2,3,4,5,6]
Anular = [0,1,2,3,4,5,6]
Menique = [0,1,2,3,4,5,6]

class Listener(myo.DeviceListener):

  def __init__(self, queue_size=8):
    self.queue_size = queue_size
    self.lock = threading.Lock()
    self.emg_data_queue = collections.deque(maxlen=queue_size)

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    with self.lock:
      temp = np.array(event.emg)
      temp = np.concatenate((temp, [temp.mean()], [temp.max()], [temp.min()]),axis=0)
      temp = temp.reshape(1,11)
      self.emg_data_queue.append((event.timestamp, temp))

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)


def step(listener):
    emgs = np.array([x[1] for x in listener.get_emg_data()])
    return emgs

def main():
    numb = 0
    queue_size=100
    myo.init()
    hub = myo.Hub()
    listener = Listener(queue_size)
    go = int(input())
    try:
        threading.Thread(target=lambda: hub.run_forever(listener.on_event)).start()
        t = 0
        flag = 0
        for p in Pulgar:
            for men in Menique:
                for a in Anular:
                    for m in Mayor:
                        for i in Indice:
                            while True:
                                emgs = step(listener)
                                if numb < go:
                                    numb +=1
                                    break
                                if t == 5000:
                                    os.system('cls')
                                    print("Valor {} de 9604".format(numb))
                                    #print("{} numeros en EMG".format(len(emgs)))
                                    #print(emgs.shape)
                                    print("Valor Actual:\n {} {} {} {} {}\n P I M A m".format(p,i,m,a,men))
                                    t = 0
                                    flag = 1
                                if keyboard.is_pressed('s') and flag:
                                    file = open('datasets/PruebaX2.0.csv','a')
                                    emgs = emgs.reshape(1,1100)
                                    np.savetxt(file, emgs, delimiter=",")
                                    file.close()
                                    file = open('datasets/PruebaY2.0.csv','a')
                                    vectornp = np.asarray([p,i,m,a,men])
                                    vectornp = vectornp.reshape(1,5)
                                    np.savetxt(file, vectornp, delimiter=",")
                                    file.close()
                                    flag = 0
                                    t = 0
                                    numb += 1
                                    break
                                if keyboard.is_pressed('q'):
                                    hub.stop()
                                    sys.exit()
                                t += 1
    finally:
        hub.stop()

if __name__ == '__main__':
  main()
