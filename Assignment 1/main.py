import cv2
import numpy as np

class IntelligentObject():

    def __init__(self):
        pass

def play_random_sound():
    from threading import Thread
    def play(arg):
        import winsound
        winsound.PlaySound('./sounds/fired2.wav', winsound.SND_FILENAME)
    Thread(target=play, args=(None,)).start()

def threshold_red(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    frame_threshold1 = cv2.inRange(hsv_img, np.array([0, 100, 100],np.uint8), np.array([10, 255, 255],np.uint8))
    frame_threshold2 = cv2.inRange(hsv_img, np.array([160, 100, 100],np.uint8), np.array([179, 255, 255],np.uint8))
    final_threshold = frame_threshold1 + frame_threshold2
    kernel = np.ones((3,3))
    opening = cv2.morphologyEx(final_threshold, cv2.MORPH_OPEN, kernel)
    return opening


def combine(bg, fg):
    ret = np.copy(bg)
    t_channel_fg = cv2.cvtColor(fg, cv2.COLOR_BGRA2BGR)
    #thesholded_img = threshold_red(fg)
    for x in range(bg.shape[0]):
        for y in range(bg.shape[1]):
            if x < fg.shape[0] and y < fg.shape[1]:
                if fg[x,y,0] != 0:
                    ret[x,y] = t_channel_fg[x,y]
    return ret

if __name__ == '__main__':
    background = cv2.imread('tokyo.jpg')

    # read in the video
    cap = cv2.VideoCapture('monkey (option1).mov')

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frames = []

    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    # cleanup
    cap.release()
    #out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (int(width), int(height)))
    for img in frames:
        #out.write(combine(background, img))
        trump = cv2.imread('trump.png', cv2.IMREAD_UNCHANGED)
        cv2.imshow('show', combine(background,trump))
        if cv2.waitKey(30) == ord('q'):
            break
    #out.release()
    cv2.destroyAllWindows()
