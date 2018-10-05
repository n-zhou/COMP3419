import cv2
import numpy as np

class IntelligentObject():

    def __init__(self):
        pass

lower_hsv = np.array([0,100,100])
upper_hsv = np.array([10,255,255])

def replace(foreground):
    ret = np.copy(foreground)
    hsv = cv2.cvtColor(foreground, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    res = cv2.bitwise_and(foreground,foreground, mask= mask)
    return res
    outimageHSV = np.uint8(res)
    outimageBGR = cv2.cvtColor(outimageHSV, cv2.COLOR_HSV2BGR)
    '''
    for x in range(ret.shape[0]):
        for y in range(ret.shape[1]):
            if not np.sum(outimageBGR[x,y]):
                ret[x,y] = foreground[x,y]
    return ret
    '''


if __name__ == '__main__':
    # read in the video
    cap = cv2.VideoCapture('monkey (option1).mov')

    frames = []
    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        cv2.imshow('show',frame)
        if cv2.waitKey(24) == ord('q'):
            break
    # cleanup
    cap.release()
    cv2.destroyAllWindows()

    '''
    for img in frames:
        cv2.imshow('show', replace(img))
        if cv2.waitKey(15) == ord('q'):
            break
    cv2.destroyAllWindows()
    '''
