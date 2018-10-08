import cv2
import numpy as np
import random

FRAME_WIDTH = None
FRAME_HEIGHT = None

class IntelligentObject():

    def __init__(self, img, x=0, y=0):
        self.img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
        self.x = x
        self.y = y
        sequence = [i for i in range(-10, 11, 1) if i != 0]
        self.velocity = [random.choice(sequence),random.choice(sequence)]

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if (self.velocity[0] < 0 and self.x <= 0) or (self.velocity[0] > 0 and self.x + self.img.shape[0] >= FRAME_WIDTH):
            self.velocity[0] *= -1
        if (self.velocity[1] < 0 and self.y <= 0) or (self.velocity[1] > 0 and self.y + self.img.shape[1] >= FRAME_HEIGHT):
            self.velocity[1] *= -1

    def draw_on_background(self, bg):
        bgr_img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        for x in range(self.img.shape[0]):
            for y in range(self.img.shape[1]):
                if x + self.y < bg.shape[0] and y + self.x < bg.shape[1]:
                    if self.img[x,y,0] != 0:
                        bg[x+self.y,y+self.x] = bgr_img[x,y]

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

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def make_clusters(points, clusters=None):
    change = False
    if not clusters:
        clusters = {(0,0): [], (FRAME_HEIGHT,FRAME_WIDTH): [], (0,FRAME_HEIGHT): [], (FRAME_HEIGHT/2, FRAME_WIDTH/2): [], (FRAME_HEIGHT,FRAME_WIDTH): []}
    for point in points:
        closest = None
        for key in clusters:
            if not closest or distance(point, closest) > distance(point, key):
                closest = key
        clusters[closest].append(point)

    current_centroids = []
    for key in sorted(clusters):
        current_centroids.append(key)
    return clusters, change

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

    hillary = IntelligentObject(cv2.imread('hillary.png', cv2.IMREAD_UNCHANGED))
    trump = IntelligentObject(cv2.imread('trump.png', cv2.IMREAD_UNCHANGED), 100,100)
    obama = IntelligentObject(cv2.imread('obama.png', cv2.IMREAD_UNCHANGED), 200,200)
    intelligent_objects = [hillary, obama]

    # read in the video
    cap = cv2.VideoCapture('monkey (option1).mov')

    FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frames = []

    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    # cleanup
    cap.release()
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (int(FRAME_WIDTH), int(FRAME_HEIGHT)))
    for img in frames:
        copy = np.copy(background)
        cv2.imshow('show', copy)
        out.write(copy)
        if cv2.waitKey(1) == ord('q'):
            break
    out.release()
    cv2.destroyAllWindows()
