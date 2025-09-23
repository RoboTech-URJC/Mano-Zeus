#############################################
## github:    madport                      ##
#############################################

# You have to use your right hand


import cv2
import mediapipe as mp
import time
import serial

PORT = '/dev/ttyACM0'
SERIALBEGIN = 9600
INIT_CHAR = "$"

COLOR_LETTERS = (255, 255, 255)
COLOR_USED_NODES = (0, 255, 0)
COLOR_REFERENCE_NODES = (255, 255, 0)

RATIO_NODES = 4

USED_NODES = (4, 8, 12, 16, 20)
REFERENCE_NODES = (5, 13, 17)

THUMB_FINGER = 4
INDEX_FINGER = 8
MIDDLE_FINGER = 12
RING_FINGER = 16
PINKY_FINGER = 20

REFERENCE_THUMB = 5
REFERENCE_UPPER = 13
REFERENCE_WRIST = 17

class handDetector():
    def __init__(self):
        self.mode = False
        self.maxHands = 1
        self.detectionCon = 1
        self.trackCon = 0.5

        self.pTime_ = 0  # Used to calculate FPS

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        

    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    def getNodesPosition(self):

        lmlist = []  # All cordinates of all nodes
        all_points = self.results.multi_hand_landmarks
        n = 0  # Go across the lmlist array

        if all_points:
            myHand = all_points[0]  # We use only one hand
            for landmark in myHand.landmark:
                
                lmlist.append(landmark)
                n += 1

        return lmlist


    def showFps(self, img):
        cTime = time.time()
        fps = 1 / (cTime - self.pTime_)
        self.pTime_ = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, COLOR_LETTERS, 3)


    def showNodes(self, img, cap, nodes, color):
        all_points = self.results.multi_hand_landmarks
        frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if all_points:
            myHand = all_points[0]  # Only there is a one hand
            for node in nodes:
                landmark = myHand.landmark[node]
                pixelCoordinates = self.mpDraw._normalized_to_pixel_coordinates(landmark.x, landmark.y, frameWidth, frameHeight)
                cv2.circle(img, pixelCoordinates, RATIO_NODES, color, -1)
    

    def getFingersPosition_basic(self, lmlist):
        thumb = 0
        index = 1
        middle = 2
        ring = 3
        pinky = 4
        wrist = 5

        position = [1, 1, 1, 1, 1, 1]  # All fingers up

        if (lmlist[THUMB_FINGER].x <= lmlist[REFERENCE_THUMB].x):
            position[thumb] = 0 

        if (lmlist[INDEX_FINGER].y >= lmlist[REFERENCE_UPPER].y):
            position[index] = 0 

        if (lmlist[MIDDLE_FINGER].y >= lmlist[REFERENCE_UPPER].y):
            position[middle] = 0 

        if (lmlist[RING_FINGER].y >= lmlist[REFERENCE_UPPER].y):
            position[ring] = 0 

        if (lmlist[PINKY_FINGER].y >= lmlist[REFERENCE_UPPER].y):
            position[pinky] = 0 

        if (lmlist[THUMB_FINGER].x <= lmlist[REFERENCE_WRIST].x):
            position[wrist] = 0

            if (lmlist[THUMB_FINGER].x >= lmlist[REFERENCE_THUMB].x):
                position[thumb] = 0
            else:
                position[thumb] = 1
            

        return position

def arrayToString (array):
    string= INIT_CHAR
    for i in array:
        string=string + str(i)

    return string

def main():

    cap = cv2.VideoCapture(0)
    detector = handDetector()
    ser = serial.Serial(
        port=PORT,
        baudrate=SERIALBEGIN,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    while True:
        success, img = cap.read()

        # Image drawing
        img = detector.findHands(img)  # Draws all the nodes and lines
        detector.showFps(img)
        detector.showNodes(img, cap, USED_NODES, COLOR_USED_NODES)
        detector.showNodes(img, cap, REFERENCE_NODES, COLOR_REFERENCE_NODES)

        # Fingers position getter and publisher
        lmlist = detector.getNodesPosition()

        if len(lmlist) != 0:
            position = detector.getFingersPosition_basic(lmlist)

            out = arrayToString(position)
            print(out, "\n")
            serialOut = bytes(out, 'utf-8')
            ser.write(serialOut)
        
        # Shows the image
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
