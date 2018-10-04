import cv2
import numpy as np

def replace(background, foreground):
    ret = np.copy(backgound)
    for x in range(ret.shape[0]):
        for y in range(ret.shape[1]):
            if foreground[x,y,0] < 120:
                ret[x,y,z] = foreground[x,y,z]
    return ret


if __name__ == '__main__':
    # read in the background
    backgound = cv2.imread('background.jpg')

    # read in the video
    cap = cv2.VideoCapture('monkey (option1).mov')

    frames = []
    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        cv2.imshow('show',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    # cleanup
    cap.release()
    cv2.destroyAllWindows()


    for frame in frames:
        cv2.imshow('show', replace(backgound, frame))
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
