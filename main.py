import threading
import pygame

import cv2
import imutils
import time

# Initializer
pygame.mixer.init()

# Choose camera index 0
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
"""
This resize function of imutils maintains the aspect ratio and provides the
keyword arguments width and height so the image can be resized to the intended
width/height while (1) maintaining aspect ratio and (2) ensuring the dimensions
of the image do not have to be explicitly computed by the developer.
"""
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21),  0)

alarm = False
alarm_mode = False
alarm_counter = 0


def play_alarm():
    global alarm

    if not alarm_mode:
        return

    print("ALARM")
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    time.sleep(1)

    alarm = False


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 300:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=play_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destoryAllWindows()
