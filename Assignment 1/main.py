import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture('monkey (option1).mov')
    while 1 :
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('lol',frame)
        if cv2.waitKey(30) == ord('a'):
            break
