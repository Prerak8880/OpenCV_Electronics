import cv2 as cv
import serial
import struct
import time

a = 0
b = 0
x = 0
y = 0
ser = serial.Serial('com6', 9600)
time.sleep(2)
FaceCascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    face = FaceCascade.detectMultiScale(gray, 1.2, 4)

    try:
        for (x1, y1, w1, h1) in face:
            a = int((2 * x1 + w1) / 2)
            b = int((2 * y1 + h1) / 2)
            x = int(a / 3.66)
            y = int(b / 2.55)
            ser.write(struct.pack('>BB', x, y))

            cv.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

    except:
        pass

    cv.imshow('Servo Moving', frame)
    k = cv.waitKey(20) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()
