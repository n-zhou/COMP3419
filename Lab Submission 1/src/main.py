import numpy as np
import cv2
import os
import sys

if __name__ == '__main__':
    # K is preferred to be odd to make it easier to determine the central coordinate of
    # each grid block.
    K = 9

    vid = cv2.VideoCapture('background.mov')
    while 1:
        ret, frame = vid.read()
        if not ret:
            break
        cv2.imshow('background', frame)
