import numpy as np
import cv2
import os
import sys
import math

# probably don't need this function
def binarize(img):
    return cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]

# probably don't need this function
def invert(img):
    inverted_img = np.copy(img)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            inverted_img[x,y] = abs(255-img[x,y])
    return inverted_img

# calculating the sum of squared differences
def ssd(b1, b2):
    # TODO replace with numpy functions
    sum = 0
    diff = b1-b2
    return math.sqrt(np.sum(diff**2))

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
    n_of_rows, n_of_columns, n_of_colour_channels = (None, None, None)
    cap = cv2.VideoCapture(PATH_TO_FILE)
    # read in the frames
    while 1:
        ret, frame = cap.read()
        if not ret:
            break
        n_of_rows, n_of_columns, n_of_colour_channels = frame.shape
        frames.append(frame)
        grey_frames.append(cv2.cvtColor(frames[-1], cv2.COLOR_BGR2GRAY))
        binary_frames.append(binarize(grey_frames[-1]))
    # release the resources
    cap.release()
    cv2.destroyAllWindows()

    splits = []
    for i in range(len(frames)):
        splits.append({})
        for x in range(int(n_of_columns/K)):
            for y in range(int(n_of_rows/K)):
                splits[-1][(x,y)] = np.zeros((K,K))

    for frame in frames:
        cv2.imshow(PATH_TO_FILE, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main(sys.argv[1:])
