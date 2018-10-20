import cv2
import numpy as np
import random
import math

FRAME_WIDTH = None
FRAME_HEIGHT = None
POW = None

class IntelligentObject():

    def __init__(self, img, sound=None, fx=0.3, fy=0.3, x=None, y=None):
        self.img = cv2.resize(img, (0,0), fx=fx, fy=fy)
        self.x = x
        self.y = y
        sequence = [i for i in range(-10, 11, 1) if i != 0]
        self.radius = max([int(element/2) for element in self.img.shape])
        self.sound = sound
        self.velocity = [random.choice(sequence),random.choice(sequence)]

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if (self.velocity[0] < 0 and self.x <= 0) or (self.velocity[0] > 0 and self.x + self.img.shape[0] >= FRAME_HEIGHT):
            self.velocity[0] *= -1
        if (self.velocity[1] < 0 and self.y <= 0) or (self.velocity[1] > 0 and self.y + self.img.shape[1] >= FRAME_WIDTH):
            self.velocity[1] *= -1

    def draw_on_background(self, bg):
        bgr_img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        try:
            self.draw_at(bg, (int(self.x), int(self.y)))
        except:
            '''
            use for loops if and exception is caught
            '''
            for x in range(self.img.shape[0]):
                for y in range(self.img.shape[1]):
                    if x + self.x < bg.shape[0] and y + self.y < bg.shape[1]:
                        if self.img[x,y,3] > 127:
                            bg[int(x+self.x),int(y+self.y)] = bgr_img[x,y]

    def calculate_center(self):
        return int(self.x+self.img.shape[0]/2), int(self.y + self.img.shape[1] / 2)

    def draw_at(self, bg, point):
        bgr_img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        rows, columns, chanels = bgr_img.shape
        endX = min(bg.shape[0], point[0] + bgr_img.shape[0])
        endY = min(bg.shape[1], point[1] + bgr_img.shape[1])

        # bg[point[0]:endX, point[1]:endY] = bgr_img[0:max(endX-point[0],0),0:max(endY-point[1],0)]
        try:
            bg[point[0]:endX, point[1]:endY, 0] = np.where(self.img[:max(endX-point[0],0),:max(endY-point[1],0),3] > 127, self.img[:max(endX-point[0],0),:max(endY-point[1],0),0],bg[point[0]:endX, point[1]:endY, 0])
            bg[point[0]:endX, point[1]:endY, 1] = np.where(self.img[:max(endX-point[0],0),:max(endY-point[1],0),3] > 127, self.img[:max(endX-point[0],0),:max(endY-point[1],0),1],bg[point[0]:endX, point[1]:endY, 1])
            bg[point[0]:endX, point[1]:endY, 2] = np.where(self.img[:max(endX-point[0],0),:max(endY-point[1],0),3] > 127, self.img[:max(endX-point[0],0),:max(endY-point[1],0),2],bg[point[0]:endX, point[1]:endY, 2])
        except:
            for x in range(self.img.shape[0]):
                for y in range(self.img.shape[1]):
                    if x + point[0] - int(rows/2) < bg.shape[0] and y + point[1] - int(columns/2) < bg.shape[1]:
                        if self.img[x,y,3] > 127:
                            bg[x+point[0]-int(rows/2),y+point[1]-int(columns/2)] = bgr_img[x,y]

    def set(self,x,y):
        self.x = x
        self.y = y

    def set_velocity(self,x,y):
        self.velocity = [x,y]

    def resolve(self, body_part):
        '''
        resolve a collision between an intelligent object and a body part
        '''
        collisionVector = np.array([body_part.calculate_center()[0] - self.calculate_center()[0], body_part.calculate_center()[1]-self.calculate_center()[1]])
        collisionVector = collisionVector/ np.linalg.norm(collisionVector)

        vA = np.dot(collisionVector, self.velocity)
        vB = np.dot(collisionVector, body_part.velocity)

        mR = 3
        a = -(mR + 1)
        b = 2 * (mR * vB + vA)
        c = -((mR - 1) * vB * vB + 2 * vA * vB)
        discriminant = math.sqrt(b * b - 4 * a * c)
        root = (-b + discriminant)/(2 * a)
        # only one of the roots is the solution, the other pertains to the current velocities
        if root - vB < 0.01:
            root = (-b - discriminant)/(2 * a)
        self.velocity = self.velocity + collisionVector * (vB - root)

    def pow(self, bg):
        POW.draw_at(bg, (int(self.x), int(self.y)))

    def make_noise(self):
        play_sound(self.sound)

from threading import Lock
lock = Lock()
playing = {}

def play_sound(name):
    from threading import Thread
    def play(arg):
        import winsound
        if lock.acquire(False):
            winsound.PlaySound(name, winsound.SND_FILENAME)
            lock.release()
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

    POW = IntelligentObject(cv2.imread('./images/pow.png', cv2.IMREAD_UNCHANGED), None, 0.08, 0.08,x=30,y=30)
    hillary = IntelligentObject(cv2.imread('./images/hillary.png', cv2.IMREAD_UNCHANGED),'./sounds/nasty_woman.wav', 0.2, 0.2,x=10,y=10)
    obama = IntelligentObject(cv2.imread('./images/obama.png', cv2.IMREAD_UNCHANGED), './sounds/fired.wav',x=150,y=150)
    trump = IntelligentObject(cv2.imread('./images/trump.png', cv2.IMREAD_UNCHANGED), None,0.2,0.2)
    right_hand = IntelligentObject(cv2.imread('./images/right_hand.png', cv2.IMREAD_UNCHANGED), None,0.05,0.05)
    left_hand = IntelligentObject(cv2.imread('./images/left_hand.png', cv2.IMREAD_UNCHANGED), None,0.05,0.05)
    left_foot = IntelligentObject(cv2.imread('./images/leftfoot.png', cv2.IMREAD_UNCHANGED), None)
    right_foot = IntelligentObject(cv2.imread('./images/rightfoot.png', cv2.IMREAD_UNCHANGED),None)
    intelligent_objects = [hillary, obama]
    body_parts = [right_hand,left_hand,right_foot,left_foot,trump]
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

    copies = []
    sound = {}

    for count, img in enumerate(frames):
        if count > FRAME_RATE*31:
            break
        points = get_points(img)
        clusters = make_clusters(points) if not clusters else make_clusters(points, clusters)
        copy = np.copy(cv2.resize(background_frames[count], (568,320)))
        cluster_keys = list(clusters.keys())
        for counter, centroid in enumerate(clusters):
            body_parts[counter].draw_at(copy,centroid)

            if body_parts[counter].x is None:
                body_parts[counter].set(centroid[0], centroid[1])
                body_parts[counter].set_velocity(0,0)
            else:
                body_parts[counter].set_velocity(centroid[0]-body_parts[counter].x, centroid[1]-body_parts[counter].y)
                body_parts[counter].set(centroid[0], centroid[1])
        for intel in intelligent_objects:
            intel.draw_on_background(copy)
            intel.move()
            for body_part in body_parts:
                if distance(intel.calculate_center(), body_part.calculate_center()) <= intel.radius + body_part.radius:
                    intel.resolve(body_part)
                    intel.pow(copy)
                    if count not in sound:
                        sound[count] = []
                    sound[count].append(intel)
        out.write(copy)
        copies.append(copy)
        cv2.imshow('show',copy)
        if cv2.waitKey(1) == ord('q'):
            break
    out.release()

    # clear the list for garbage collection
    frames = []
    background_frames = []

    for count, frame in enumerate(copies):
        if count in sound:
            for intel in sound[count]:
                intel.make_noise()
        cv2.imshow('show', frame)
        if cv2.waitKey(int(1000/20)) == ord('q'):
            break
