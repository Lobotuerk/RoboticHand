import serial

def send(vector,arduino):
    temp = [0,0,0,0,0]
    for x in range(len(vector)):
        if vector[x] < 0:
            vector[x] = 0
        if vector[x] > 100:
            vector[x] = 100
    temp[0] = vector[0] * 1.6
    temp[1] = vector[1] * 0.9
    temp[2] = vector[2] * 0.9
    temp[3] = vector[3] * 0.75
    temp[4] = vector[4] * 0.65
    for x in temp:
        rnd = str(x) + ','
        arduino.write(rnd.encode('utf-8'))
