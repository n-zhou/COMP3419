import cv2
import numpy as np
import random
import math

FRAME_WIDTH = None
FRAME_HEIGHT = None
POW = None

class IntelligentObject():
    '''
    '''

    def __init__(self, img, sound=None, fx=0.3, fy=0.3, x=None, y=None):
        '''Creates an intelligent object given the following parameters


        Parameters:
            img (cv2.img): The image with which our intelligent object will use as it's texture
            sound (str): The path to the sound file which the intelligent object will play when it's make_noise() method is called
            fx (float): The size we want to scale the input image along the x-axis
            fy (float): The size we want to scale the input image along the y-axis
            x (int): The x position of the image
            y (int): The y position of the image

        Returns:
            IntelligentObject: A newly created intelligent object
        '''
        self.img = cv2.resize(img, (0,0), fx=fx, fy=fy)
        self.x = x
        self.y = y
        sequence = [i for i in range(-10, 11, 1) if i != 0]
        self.radius = max([int(element/2) for element in self.img.shape])
        self.sound = sound
        self.velocity = [random.choice(sequence),random.choice(sequence)]

    def move(self):
        '''Moves the object according to it's current velocity and adjust it accordingly when it hits a wall.

        '''
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if (self.velocity[0] < 0 and self.x <= 0) or (self.velocity[0] > 0 and self.x + self.img.shape[0] >= FRAME_HEIGHT):
            self.velocity[0] *= -1
        if (self.velocity[1] < 0 and self.y <= 0) or (self.velocity[1] > 0 and self.y + self.img.shape[1] >= FRAME_WIDTH):
            self.velocity[1] *= -1

    def draw_on_background(self, bg):
        '''Draw the object at the background at it's current location

        Parameters:
            bg (np.array): The background we are drawing on
        '''
        bgr_img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        for x in range(self.img.shape[0]):
            for y in range(self.img.shape[1]):
                if x + self.x < bg.shape[0] and y + self.y < bg.shape[1]:
                    if self.img[x,y,3] > 127:
                        # replace the background only if the foreground pixel is not transparent
                        bg[int(x+self.x),int(y+self.y)] = bgr_img[x,y]

    def calculate_center(self):
        return int(self.x+self.img.shape[0]/2), int(self.y + self.img.shape[1] / 2)

    def draw_at(self, bg, point):
        '''Draws the object on the background at a specified point

        Parameters:
            bg (np.array): the background image we are drawing to
            point (tuple): A tuple of size two that represents the coordinate of where the image should be drawn
        '''
        bgr_img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        rows, columns, chanels = bgr_img.shape
        endX = min(bg.shape[0], point[0] + bgr_img.shape[0])
        endY = min(bg.shape[1], point[1] + bgr_img.shape[1])

        # bg[point[0]:endX, point[1]:endY] = bgr_img[0:max(endX-point[0],0),0:max(endY-point[1],0)]
        try:
            # replace the background only if the foreground pixel is not transparent
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
        '''Sets the position of this object at the given position

        Parameters:
            x (int): The x position we wish to set the object to
            y (int): The y position we wish to set the object to
        '''
        self.x = x
        self.y = y

    def set_velocity(self,x,y):
        '''Sets the velocity of the intelligent object to the given parameters

        Parameters:
            x (int): The x velocity we wish to set the object to
            y (int): The y velocity we wish to set the object to
        '''
        self.velocity = [x,y]

    def resolve(self, body_part):
        '''resolve a collision between an intelligent object and a body part

        Parameters:
            body_part (IntelligentObject): The body part with which the marionette collided
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

        # apply the resultant velocity to this current intelligent object
        self.velocity = self.velocity + collisionVector * (vB - root)

    def pow(self, bg):
        '''Draws a pow at the objects current location

        Parameters:
            bg (np.array): The background which we are drawing the pow image on
        '''
        POW.draw_at(bg, (int(self.x), int(self.y)))

    def make_noise(self):
        '''Play a sound track

        '''
        play_sound(self.sound)

from threading import Lock
lock = Lock()
playing = {}

def play_sound(name):
    '''Play an audio clip given the path to it

    Parameters:
        name (str): the path to the wav file that is to be played
    '''
    from threading import Thread
    def play(arg):
        import winsound
        if lock.acquire(False):
            winsound.PlaySound(name, winsound.SND_FILENAME)
            lock.release()
    Thread(target=play, args=(None,)).start()

def threshold_red(img):
    '''Turns an RGB image into a binary image with all the red pixels being white

    Parameters:
        img (np.array): The image which we are thresholding for the red dots

    Returns:
        np.array: A binary image where every non-red pixel is turned black and every red one is turned white
    '''
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
    '''Gets the number of red points of a given image

    Parameters:
        img (np.array): The image which we are finding the locations of the red points of

    Returns:
        list: a list of points (a two tuple) of the location of all the red points found in the image
    '''
    points = []
    binary_img = threshold_red(img)
    columns, rows = binary_img.shape[0], binary_img.shape[1]
    for x in range(columns):
        for y in range(rows):
            if binary_img[x,y] != 0:
                points.append((x,y))
    return points

def distance(p1, p2):
    '''Calculate the distance between two points

    Parameters:
        p1 (tuple): The first point we are calculating
        p2 (tuple): The second point we are calculating

    Returns:
        float: the distance between the points
    '''
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def make_clusters(points, clusters=None):
    '''Creates 5 clusters based on their points and the given cluster

    Parameters:
        points (list): A list of tuples that contain the coordinates of all the red points in an image
        clusters (dict): A dictionary of size 5 where the keys are the initial centroids

    Returns:
        dict: A dictionary of size 5 where the keys represent the final centroids
    '''
    if not clusters:
        clusters = {(120,180): [], (80,280): [], (260,230): [], (240,270): [], (170, 265): []}
    new_clusters = {}
    for point in points:
        closest = None
        for key in clusters:
            # form the clusters
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
        # if we get a nan error just set the center to the original point
        center_x = int(center_x) if not math.isnan(center_x) else key[0]
        center_y = int(center_y) if not math.isnan(center_y) else key[1]
        new_clusters[(center_x, center_y)] = []
        if center_x != key[0] or center_y != key[1]:
            # set change to true if any of the cluster center points change
            change = True
    # if the centroids do not change return the original clusters otherwise call itself again
    return clusters if not change else make_clusters(points, new_clusters)

if __name__ == '__main__':
    background = cv2.resize(cv2.imread('./images/whitehouse.jpg'), (568,320))

    background_frames = []
    cap = cv2.VideoCapture('./images/whitehouse.avi')
    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        # read in the frames of our replacement background and store them in a list
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

    # store the intelligent objects in a list
    intelligent_objects = [hillary, obama]

    # store the body parts in a list
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
        # read in all the frames of the monkey and store them in a list
        frames.append(frame)
    cap.release()

    clusters = None
    FRAME_RATE = 20

    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), FRAME_RATE, (int(FRAME_WIDTH), int(FRAME_HEIGHT)))

    copies = []
    sound = {}

    for count, img in enumerate(frames):
        if count > FRAME_RATE*31:
            # once we reach 31 seconds (the original length of the video) we break
            break
        # get all the red points in the image
        points = get_points(img)
        # create the clusters from the given points
        clusters = make_clusters(points) if not clusters else make_clusters(points, clusters)

        copy = np.copy(cv2.resize(background_frames[count], (568,320)))
        cluster_keys = list(clusters.keys())
        for counter, centroid in enumerate(clusters):
            # update the position of the body parts based on the cluster centers
            if body_parts[counter].x is None:
                body_parts[counter].set(centroid[0], centroid[1])
                body_parts[counter].set_velocity(0,0)
            else:
                body_parts[counter].set_velocity(centroid[0]-body_parts[counter].x, centroid[1]-body_parts[counter].y)
                body_parts[counter].set(centroid[0], centroid[1])

        for counter, centroid in enumerate(clusters):
            # connect the body parts to the head
            cv2.line(copy, (body_parts[counter].calculate_center()[1],body_parts[counter].calculate_center()[0]), (body_parts[-1].calculate_center()[1], body_parts[-1].calculate_center()[0]), (0,153,204), thickness=5)
            #draw the texture of the body part on top of the line
            body_parts[counter].draw_at(copy,centroid)
        for intel in intelligent_objects:
            # draw the intelligenet object onto the background
            intel.draw_on_background(copy)
            # move the object
            intel.move()
            for body_part in body_parts:
                if distance(intel.calculate_center(), body_part.calculate_center()) <= intel.radius + body_part.radius:
                    # resolve the collision with the body part
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
                # play the queued sound
                intel.make_noise()
        cv2.imshow('show', frame)
        if cv2.waitKey(int(1000/20)) == ord('q'):
            break
