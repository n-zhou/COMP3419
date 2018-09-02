import numpy as np
import cv2
import os
import sys
import math

# probably don't need this function
def binarize(img):
    img_bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    return img_bw

# probably don't need this function
def invert(img):
    inverted_img = np.copy(img)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            inverted_img[x,y] = abs(255-img[x,y])
    return inverted_img

# calculating the sum of squared differences
def ssd(b1, b2):
    sum = 0
    for x in range(b1.shape[0]):
        for y in range(b2.shape[1]):
            for c in range(b2.shape[3])
                sum += math.pow(b1[x,y,c]-b2[x,y,c],2)
    return math.sqrt(sum)

def step1(img, k = 8):
    pass

def step2():
    pass

def step3():
    pass

def step4():
    pass

def step5():
    pass

def main(args):
    # K is preferred to be odd to make it easier to determine the central coordinate of
    # each grid block.
    K = 8
    if len(args) != 1:
        print("Error: Expected 1 argument but got %d" % len(args))
        sys.exit()

    PATH_TO_FILE = args[0]
    frames = []
    grey_frames = []
    binary_frames = []
    inverted_frames = []
    n_of_rows, n_of_columns, n_of_colour_channels = (None, None, None)
    vid = cv2.VideoCapture(PATH_TO_FILE)
    # read in the frames
    while 1:
        ret, frame = vid.read()
        if not ret:
            break
        n_of_rows, n_of_columns, n_of_colour_channels =  frame.shape
        frames.append(frame)
        grey_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        binary_frames.append(binarize(grey_frames[-1]))
        inverted_frames.append(invert(binary_frames[-1]))
        cv2.imshow('inverted', inverted_frames[-1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # release the resources
    vid.release()
    cv2.destroyAllWindows()

    for frame in inverted_frames:
        cv2.imshow(PATH_TO_FILE, frame)
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main(sys.argv[1:])
