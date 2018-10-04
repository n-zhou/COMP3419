import cv2
import numpy as np

'''
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
'''

lower_blue = np.array([0,0,0])
upper_blue = np.array([180,255,255])

def replace(background, foreground):
    ret = np.copy(backgound)
    hsv = cv2.cvtColor(foreground, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(foreground,foreground, mask= mask)

    outimageHSV = np.uint8(res)
    outimageBGR = cv2.cvtColor(outimageHSV, cv2.COLOR_HSV2BGR)

    for x in range(ret.shape[0]):
        for y in range(ret.shape[1]):
            if not np.sum(outimageBGR[x,y]):
                ret[x,y] = foreground[x,y]
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


    for img in frames:
        cv2.imshow('show', replace(backgound, img))
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
