import serial
import time
import random
import keyboard
import os
from funciones import send

arduino = serial.Serial('COM14', 9600)
time.sleep(2)

vector = [0,0,0,0,59]
time = 0;
n = 4
send(vector, arduino)
while (True):
    time +=1
    if keyboard.is_pressed('w') and time > 40:
        vector[n] +=1
        time = 0
        os.system('cls')
        print(vector)
        send(vector,arduino)
    if keyboard.is_pressed('s') and time > 40:
        vector[n] -=1
        time = 0
        os.system('cls')
        print(vector)
        send(vector,arduino)


    if keyboard.is_pressed('q'):
        send([0,0,0,0,0], arduino)
        break






arduino.close()
