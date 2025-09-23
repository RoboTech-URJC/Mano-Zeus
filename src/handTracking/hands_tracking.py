#############################################
## github:    madport                      ##
## github:    vbarcena2020                 ##
#############################################

##############################################################################################
##                                                                                          ##
## You have to select how many hands you want and if it is only one wich one example        ##
##                                                                                          ##
## Usage: python3 hands_tracking --n 2            # detect two hands                        ##
##                                                                                          ##
## Usage: python3 hands_tracking --n 1 --hand 0   # detect left hand                        ##
##                                                                                          ##
## Usage: python3 hands_tracking --n 1 --hand 1   # detect right hand                       ##
##                                                                                          ##
##############################################################################################

import cv2
import mediapipe as mp
import time
import serial
import sys
import numpy as np

PORT = '/dev/ttyACM0'
SERIALBEGIN = 9600
INIT_CHAR = "$"

COLOR_LETTERS = (255, 255, 255)
COLOR_USED = (255, 0, 255)

RATIO_NODES = 4

USED_ARM_NODES = [11, 12, 13, 14, 15, 16]

THUMB_FINGER = 4
INDEX_FINGER = 8
MIDDLE_FINGER = 12
RING_FINGER = 16
PINKY_FINGER = 20

LEFT = 0
RIGHT = 1

REFERENCE_THUMB = 5
REFERENCE_UPPER = 13
REFERENCE_WRIST = 17

class armDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose

    def calculate_angle(self, a, b, c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
        
        return angle 

    def get_arms(self, image, pose):
            left_landmark_points = []
            right_landmark_points = []
            i = 0
            j = 0

            # Recolor image to RGB, make detection and recolor back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Calculate angle
                right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)    
                left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                
                # Draw arms
                for landmark in USED_ARM_NODES:
                    if (landmark % 2 == 0):
                        right_landmark_points.append((int(landmarks[landmark].x * image.shape[1]), int(landmarks[landmark].y * image.shape[0])))
                        cv2.circle(image, right_landmark_points[i], 5, COLOR_USED, -1)
                        i += 1
                    else:
                        left_landmark_points.append((int(landmarks[landmark].x * image.shape[1]), int(landmarks[landmark].y * image.shape[0])))
                        cv2.circle(image, left_landmark_points[j], 5, COLOR_USED, -1)
                        j += 1
                
                cv2.line(image, right_landmark_points[0], left_landmark_points[0], COLOR_USED, 2)
                for i in range(0, 2):
                    cv2.line(image, right_landmark_points[i], right_landmark_points[i+1], COLOR_USED, 2)
                    cv2.line(image, left_landmark_points[i], left_landmark_points[i+1], COLOR_USED, 2)
                
            except:
                pass

            return image

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
    
    def getFingersPosition_basic_left(self, lmlist, position):
        thumb, index, middle, ring, pinky, wrist = 0, 1, 2, 3, 4, 5

        if lmlist[THUMB_FINGER].x >= lmlist[REFERENCE_THUMB].x:
            position[thumb] = 0

        if lmlist[INDEX_FINGER].y >= lmlist[REFERENCE_UPPER].y:
            position[index] = 0

        if lmlist[MIDDLE_FINGER].y >= lmlist[REFERENCE_UPPER].y:
            position[middle] = 0

        if lmlist[RING_FINGER].y >= lmlist[REFERENCE_UPPER].y:
            position[ring] = 0

        if lmlist[PINKY_FINGER].y >= lmlist[REFERENCE_UPPER].y:
            position[pinky] = 0 

        if lmlist[THUMB_FINGER].x >= lmlist[REFERENCE_WRIST].x:
            position[wrist] = 0

            if lmlist[THUMB_FINGER].x <= lmlist[REFERENCE_THUMB].x:
                position[thumb] = 0
            else:
                position[thumb] = 1

        return position
    
    def getFingersPosition_basic_right(self, lmlist, position):
        thumb, index, middle, ring, pinky, wrist = 6, 7, 8, 9, 10, 11

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

def usage_error():
    print("Usage: python3 hands_tacking.py --n <num_hands> (1-2)  --hands <hand_wanted> (0-left, 1-right, if num_hands == 1)")
    sys.exit(1)

def detect_one_hand(img, hand, detector_hand, detector_arm, pose, ser):
    img = detector_arm.get_arms(img, pose)
    img = detector_hand.findHands(img)  # Draws all the nodes and lines
    detector_hand.showFps(img)
    lmlist = detector_hand.getNodesPosition()

    if len(lmlist) != 0:
        position = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        if (hand == LEFT):
            position = detector_hand.getFingersPosition_basic_left(lmlist, position)
        elif (hand == RIGHT):
            position = detector_hand.getFingersPosition_basic_right(lmlist, position)

        out = arrayToString(position)
        print(out, "\n")
        
        serialOut = bytes(out, 'utf-8')
        ser.write(serialOut)
    
    # Shows the image
    cv2.imshow("Image", img)

def detect_two_hands(img, hand, detector_left_hand, detector_right_hand, detector_arm, pose, ser):
    high, width, _ = img.shape
    
    img = detector_arm.get_arms(img, pose)
    img_right = img[:, 0:int(width/2)]
    img_left = img[:, int(width/2):width]

    img_left = detector_left_hand.findHands(img_left)  
    img_right = detector_right_hand.findHands(img_right) 

    lmlist_left = detector_left_hand.getNodesPosition()
    lmlist_right = detector_right_hand.getNodesPosition()

    position = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
    if len(lmlist_left) != 0:
        position = detector_left_hand.getFingersPosition_basic_left(lmlist_left, position)

    if len(lmlist_right) != 0:
        position = detector_right_hand.getFingersPosition_basic_right(lmlist_right, position)

    if len(lmlist_right) != 0 or len(lmlist_left) != 0:
        out = arrayToString(position)
        print(out, "\n")
        
        serialOut = bytes(out, 'utf-8')
        ser.write(serialOut)
    
    # Shows the images
    img = cv2.hconcat([img_right, img_left])

    cv2.line(img, (int(width/2), 0), (int(width/2),high), COLOR_LETTERS, 1)

    # cv2.imshow("Image_left_hand", img_left)
    # cv2.imshow("Image_right_hand", img_right)
    cv2.imshow("Image", img)

def main():
    hand = -1

    if len(sys.argv) < 3:
        usage_error()

    # Get the number of hands and the hand you want
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--n" and i + 1 < len(sys.argv):
            hands = int(sys.argv[i + 1])
        elif sys.argv[i] == "--hand" and i + 1 < len(sys.argv):
            hand = int(sys.argv[i + 1])

    if (hands != 1 and hands != 2):
        usage_error()
    
    if (hands == 1):
        if (len(sys.argv) != 5):
            usage_error()
        if (hand != LEFT and hand != RIGHT):
            usage_error()

    cap = cv2.VideoCapture(0)
    detector_hand = handDetector()
    detector_left_hand = handDetector()
    detector_right_hand = handDetector()
    detector_arm = armDetector()
    
    # ser = 0  # Only used to try the tracking without arduino
    
    ser = serial.Serial(
        port=PORT,
        baudrate=SERIALBEGIN,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    
    with detector_arm.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while True:
            success, img = cap.read()

            # Cortar la mitad izquierda de la imagen
            if (hands == 1):
                detect_one_hand(img, hand, detector_hand, detector_arm, pose, ser)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Image drawing
            elif (hands == 2):
                detect_two_hands(img, hand, detector_left_hand, detector_right_hand, detector_arm, pose, ser)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
