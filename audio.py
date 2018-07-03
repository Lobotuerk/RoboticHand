import serial
import time
import random
import pyaudio
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

arduino = serial.Serial('COM14', 9600)
time.sleep(2)
while True:
    time.sleep(2)
    with mic as source:
        #r.adjust_for_ambient_noise(source)
        print('trying')
        audio = r.listen(source,phrase_time_limit=1)
        try:
            text = r.recognize_google(audio)
        except sr.RequestError:
            print("API unavailable")
        except sr.UnknownValueError:
            print("Unable to recognize speech")
            text = ''
        print('I heard: ' + text)
        if text.lower() == "rock":
            vector = [80,0,80,80,0]
            vector[0] = vector[0] * 4 / 10
            vector[1] = vector[1] * 11 / 10
            vector[2] = vector[2] * 11 / 10
            vector[3] = vector[3] * 11 / 10
            vector[4] = vector[4] * 7 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))
        if text.lower() == "fist":
            vector = [80,80,80,80,80]
            vector[0] = vector[0] * 8 / 10
            vector[1] = vector[1] * 10 / 10
            vector[2] = vector[2] * 10 / 10
            vector[3] = vector[3] * 10 / 10
            vector[4] = vector[4] * 8 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))
        if text.lower() == "sleep":
            vector = [0,0,0,0,0]
            vector[0] = vector[0] * 8 / 10
            vector[1] = vector[1] * 10 / 10
            vector[2] = vector[2] * 10 / 10
            vector[3] = vector[3] * 10 / 10
            vector[4] = vector[4] * 8 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))
        if text.lower() == "up":
            vector = [80,0,80,80,80]
            vector[0] = vector[0] * 8 / 10
            vector[1] = vector[1] * 10 / 10
            vector[2] = vector[2] * 10 / 10
            vector[3] = vector[3] * 10 / 10
            vector[4] = vector[4] * 8 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))
        if text.lower() == "circle":
            vector = [70,80,0,0,0]
            vector[0] = vector[0] * 8 / 10
            vector[1] = vector[1] * 10 / 10
            vector[2] = vector[2] * 10 / 10
            vector[3] = vector[3] * 10 / 10
            vector[4] = vector[4] * 8 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))
        if text.lower() == "nice":
            vector = [70,80,40,30,0]
            vector[0] = vector[0] * 8 / 10
            vector[1] = vector[1] * 10 / 10
            vector[2] = vector[2] * 10 / 10
            vector[3] = vector[3] * 10 / 10
            vector[4] = vector[4] * 8 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))
        if text.lower() == "peace":
            vector = [60,0,0,80,80]
            vector[0] = vector[0] * 8 / 10
            vector[1] = vector[1] * 10 / 10
            vector[2] = vector[2] * 10 / 10
            vector[3] = vector[3] * 10 / 10
            vector[4] = vector[4] * 8 / 10
            for x in vector:
                rnd = str(x) + ','
                arduino.write(rnd.encode('utf-8'))





arduino.close()
