import cv2
import numpy as np
import random
import math

FRAME_WIDTH = None
FRAME_HEIGHT = None

class IntelligentObject():

    def __init__(self, img, fx=0.3, fy=0.3, x=0, y=0):
        self.img = cv2.resize(img, (0,0), fx=fx, fy=fy)
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

    def draw_at(self, bg, point):
        bgr_img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        rows, columns, chanels = bgr_img.shape
        for x in range(self.img.shape[0]):
            for y in range(self.img.shape[1]):
                if x + point[0] - int(rows/2) < bg.shape[0] and y + point[1] - int(columns/2) < bg.shape[1]:
                    if self.img[x,y,3] > 127:
                        bg[x+point[0]-int(rows/2),y+point[1]-int(columns/2)] = bgr_img[x,y]


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
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    erosion = cv2.erode(final_threshold,kernel,iterations=2)
    dilation = cv2.dilate(erosion, kernel,iterations=1)
    erosion = cv2.erode(dilation,kernel,iterations=1)
    return erosion

def get_points(img):
    points = []
    binary_img = threshold_red(img)
    columns, rows = binary_img.shape[0], binary_img.shape[1]
    for x in range(columns):
        for y in range(rows):
            if binary_img[x,y] != 0:
                points.append((x,y))
    return points

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def make_clusters(points, clusters=None):
    if not clusters:
        clusters = {(120,180): [], (80,280): [], (260,230): [], (240,270): [], (170, 265): []}
    new_clusters = {}
    for point in points:
        closest = None
        for key in clusters:
            if closest is None or distance(point, closest) > distance(point, key):
                closest = key
        clusters[closest].append(point)
    change = False
    for key in clusters:
        center_x, center_y = 0, 0
        x = [p[0] for p in clusters[key]]
        y = [p[1] for p in clusters[key]]
        center_x = np.mean(x)
        center_y = np.mean(y)
        center_x = int(center_x) if not math.isnan(center_x) else key[0]
        center_y = int(center_y) if not math.isnan(center_y) else key[1]
        new_clusters[(center_x, center_y)] = []
        if center_x != key[0] or center_y != key[1]:
            change = True
    return clusters if not change else make_clusters(points, new_clusters)

if __name__ == '__main__':
    background = cv2.resize(cv2.imread('./images/whitehouse.jpg'), (568,320))

    background_frames = []
    cap = cv2.VideoCapture('./images/whitehouse.avi')
    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        background_frames.append(frame)
    cap.release()

    hillary = IntelligentObject(cv2.imread('./images/hillary.png', cv2.IMREAD_UNCHANGED), 0.2, 0.2)
    trump = IntelligentObject(cv2.imread('./images/trump.png', cv2.IMREAD_UNCHANGED), 0.2,0.2)
    obama = IntelligentObject(cv2.imread('./images/obama.png', cv2.IMREAD_UNCHANGED), x=200,y=200)
    hand = IntelligentObject(cv2.imread('./images/hand.png', cv2.IMREAD_UNCHANGED), 0.05,0.05)
    right_hand = IntelligentObject(cv2.imread('./images/righthand.png', cv2.IMREAD_UNCHANGED), 0.05,0.05)
    left_foot = IntelligentObject(cv2.imread('./images/leftfoot.png', cv2.IMREAD_UNCHANGED))
    right_foot = IntelligentObject(cv2.imread('./images/rightfoot.png', cv2.IMREAD_UNCHANGED))
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
    cap.release()

    clusters = None
    FRAME_RATE = 20
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), FRAME_RATE, (int(FRAME_WIDTH), int(FRAME_HEIGHT)))
    for count, img in enumerate(frames):
        if count > FRAME_RATE*31:
            break
        points = get_points(img)
        clusters = make_clusters(points) if not clusters else make_clusters(points, clusters)
        copy = np.copy(cv2.resize(background_frames[count], (568,320)))
        cluster_keys = list(clusters.keys())
        for counter, centroid in enumerate(clusters):
            if counter == 0:
                right_hand.draw_at(copy, centroid)
            if counter == 1:
                hand.draw_at(copy, centroid)
            if counter == 2:
                right_foot.draw_at(copy, centroid)
            if counter == 3:
                left_foot.draw_at(copy, centroid)
            if counter == 4:
                trump.draw_at(copy, centroid)
        cv2.imshow('show', copy)
        out.write(copy)
        if cv2.waitKey(1) == ord('q'):
            break
    out.release()
    cv2.destroyAllWindows()
