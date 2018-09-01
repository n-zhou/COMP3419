import numpy as np
import cv2
import os
import sys
import math

def main(args):
    # K is preferred to be odd to make it easier to determine the central coordinate of
    # each grid block.
    K = 8
    if len(args) != 1:
        print("Error: Expected 1 argument but got %d" % len(args))
        sys.exit()
    PATH_TO_FILE = args[0]
    vid = cv2.VideoCapture(PATH_TO_FILE)
    frames = []
    n_of_rows, n_of_columns, n_of_colour_channels = (None, None, None)
    while 1:
        ret, frame = vid.read()
        if not ret:
            break
        n_of_rows, n_of_columns, n_of_colour_channels =  frame.shape
        frames.append(frame)
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''
    vid.release()
    cv2.destroyAllWindows()
    for frame in frames:
        cv2.imshow(PATH_TO_FILE, frame)
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break
    # SSD
    # REPEAT 1-5???
    print(n_of_rows, n_of_columns, n_of_colour_channels)

if __name__ == '__main__':
    main(sys.argv[1:])
