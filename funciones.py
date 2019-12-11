import serial

def send(vector,arduino):
    temp = [0,0,0,0,0]
    for x in range(len(vector)):
        if vector[x] < 0:
            vector[x] = 0
        if vector[x] > 170:
            vector[x] = 170
    temp[0] = (vector[0] * 1) + 0
    temp[1] = (vector[1] * 1) + 0
    temp[2] = (vector[2] * 1) + 0
    temp[3] = (vector[3] * 1) + 0
    temp[4] = (vector[4] * 1) + 0
    for x in temp:
        rnd = str(x) + ','
        arduino.write(rnd.encode('utf-8'))
