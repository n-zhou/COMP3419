import numpy as np
import cv2
import os
import sys
import math


if __name__ == '__main__':
    # K is preferred to be odd to make it easier to determine the central coordinate of
    # each grid block.
    K = 5

    vid = cv2.VideoCapture('monkey.avi')

    frames = []

    while 1:
        ret, frame = vid.read()
        if not ret:
            break
        frames.append(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # SSD
    # REPEAT 1-5???
