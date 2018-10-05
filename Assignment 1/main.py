import cv2
import numpy as np

class IntelligentObject():

    def __init__(self):
        pass

def threshold_red(img):
    return img


if __name__ == '__main__':
    # read in the video
    cap = cv2.VideoCapture('monkey (option1).mov')

    frames = []

    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    # cleanup
    cap.release()

    for img in frames:
        cv2.imshow('show', threshold_red(img))
        if cv2.waitKey(15) == ord('q'):
            break
    cv2.destroyAllWindows()
