import numpy as np
import cv2
import os
import sys
import math


# calculating the sum of squared differences
def ssd(b1, b2):
    return math.sqrt(np.sum((b1-b2)**2))

# check that the boundary we are checking is valid
def check_valid(img, x1, x2, y1, y2):
    return x1 >= 0 and x2 <= img.shape[0] and y1 >= 0 and y2 <= img.shape[1]

def magic(frame1, frame2, k = 8):
    # they come in size 2 because we hold 2 vectors
    displacement_vectors = np.array((int(frame1.shape[0]/k), int(frame1.shape[1]/k), 2))
    for x in range(0,frame1.shape[0],k):
        for y in range(0,frame1.shape[1],k):
            if check_valid(frame1,x,x+k,y,y+k):
                macroblock = frame1[x:x+k,y:y+k]
    # return the displacement vectors xd
    return displacement_vectors


if __name__ == '__main__':
    # K is preferred to be odd to make it easier to determine the central coordinate of
    # each grid block.
    K = 8
    PATH_TO_FILE = 'monkey.avi'
    frames = []
    cap = cv2.VideoCapture(PATH_TO_FILE)
    # read in the frames
    while 1 and len(frames) < 250:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    # release the resources
    cap.release()
    cv2.destroyAllWindows()

    counter = 0
    for frame in frames:
        step1(frame)
        cv2.imwrite('./output/frame%d.png' % counter, frame)
        counter += 1
