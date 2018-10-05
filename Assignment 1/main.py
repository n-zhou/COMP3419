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
    erosion = cv2.erode(final_threshold,np.ones((3,3)),iterations = 4)
    dilation = cv2.dilate(erosion,np.ones((3,3)),iterations = 4)
    return erosion


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
