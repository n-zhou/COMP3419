import cv2
import numpy as np

class IntelligentObject():

    def __init__(self):
        pass

def threshold_red(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    frame_threshold1 = cv2.inRange(hsv_img, np.array([0, 100, 100],np.uint8), np.array([10, 255, 255],np.uint8))
    frame_threshold2 = cv2.inRange(hsv_img, np.array([160, 100, 100],np.uint8), np.array([179, 255, 255],np.uint8))
    final_threshold = frame_threshold1 + frame_threshold2
    erosion = cv2.erode(final_threshold,np.ones((5,5)),iterations = 2)
    dilation = cv2.dilate(erosion,np.ones((5,5)),iterations=3)
    return dilation

def combine(bg, fg):
    ret = np.copy(bg)
    thesholded_img = threshold_red(fg)
    for x in range(bg.shape[0]):
        for y in range(bg.shape[1]):
            if thesholded_img[x,y] != 0:
                ret[x,y,0] = fg[x,y,0]
                ret[x,y,1] = fg[x,y,1]
                ret[x,y,2] = fg[x,y,2]

    return ret

if __name__ == '__main__':

    background = cv2.imread('tokyo.jpg')

    # read in the video
    cap = cv2.VideoCapture('monkey (option1).mov')

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(height,width)
    frames = []

    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    # cleanup
    cap.release()

    for img in frames:
        cv2.imshow('show', combine(background, img))
        if cv2.waitKey(15) == ord('q'):
            break
    cv2.destroyAllWindows()
