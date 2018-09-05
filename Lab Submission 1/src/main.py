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
    displacement_vectors = np.ones((int(frame1.shape[0]/k), int(frame1.shape[1]/k), 2))
    for x in range(0,frame1.shape[0],k):
        for y in range(0,frame1.shape[1],k):
            if check_valid(frame1,x,x+k,y,y+k):
                macroblock = frame1[x:x+k,y:y+k]
                ssd(macroblock, macroblock)
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

    # write an output vid
    #out = cv2.VideoWriter('outputVid.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (int(frames[-1].shape[1]), int(frames[-1].shape[0])))
    for index in range(1,len(frames)):
        copy = np.copy(frames[index])
        for x in range(int(copy.shape[0]/K)):
            for y in range(int(copy.shape[1]/K)):
                displacement_vectors = magic(frames[index-1], frames[index],K)
                # TODO v1 < displacement vectors to be displayed < v2
                # v1 -> 0
                # v2 -> ?
                if displacement_vectors[x,y,0] == 0 and displacement_vectors[x,y,1] == 0:
                    continue
                # visualising the displacements
                copy = cv2.circle(copy, (int(y*K + displacement_vectors[x,y,1]), int(x*K + displacement_vectors[x,y,0])), 1, (0,0,255), thickness=1, lineType=-1, shift=0)
        cv2.imwrite('./output/frame%d.png' % index, copy)
        #out.write(copy)

    out.release()
    cv2.destroyAllWindows()
