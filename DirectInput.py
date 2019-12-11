import serial
import time
import random
import keyboard
import os
from funciones import send

arduino = serial.Serial('COM9', 9600)
time.sleep(2)

vector = [0,0,0,0,0]
time = 0;
n = 0
send(vector, arduino)
while (True):
    time +=1
    if keyboard.is_pressed('w') and time > 1000 and vector[n] < 170:
        vector[n] +=10
        time = 0
        os.system('cls')
        print(vector)
        print(n)
        send(vector,arduino)

    elif keyboard.is_pressed('d') and time > 1000 and n < 4:
        n += 1
        time = 0
        os.system('cls')
        print(vector)
        print(n)
    elif keyboard.is_pressed('a') and time > 1000 and n > 0:
        n -= 1
        time = 0
        os.system('cls')
        print(vector)
        print(n)
    elif keyboard.is_pressed('s') and time > 1000 and vector[n] > 0:
        vector[n] -=10
        time = 0
        os.system('cls')
        print(vector)
        print(n)
        send(vector,arduino)


    if keyboard.is_pressed('q'):
        send([0,0,0,0,0], arduino)
        break






arduino.close()
