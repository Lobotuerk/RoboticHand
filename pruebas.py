import serial
import time
import random

arduino = serial.Serial('COM14', 9600)
time.sleep(2)

vector = [80,0,0,0,0]
'''for x in range(5):
    vector[x] = random.randrange(60)'''
vector[0] = vector[0] * 8 / 10
vector[1] = vector[1] * 10 / 10
vector[2] = vector[2] * 10 / 10
vector[3] = vector[3] * 10 / 10
vector[4] = vector[4] * 8 / 10


for x in vector:
    rnd = str(x) + ','
    print('Sending ' + rnd )
    arduino.write(rnd.encode('utf-8'))
    rawString = arduino.readline()
    print(rawString)


arduino.close()
