#############################################
## github:    madport                      ##
## github:    vbarcena2020                 ##
#############################################

##############################################################################################
##                                                                                          ##
## You have to select how many hands you want and if it is only one wich one example        ##
##                                                                                          ##
## Usage: python3 arms_tracking.py --n 2            # detect two hands                      ##
##                                                                                          ##
## Usage: python3 arms_tracking.py --n 1            # detect one hand                       ##
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

LEFTSTRING = "Left"
RIGHTSTRING = "Right"
NAMES = ["Thumb:  ", "Index:  ", "Middle: ", "Ring:   ", "Pinky:  ", "Wrist:  ", "Elbow:  "]

REFERENCE_INIT = 0
REFERENCE_THUMB = 5
REFERENCE_MIDDLE = 9
REFERENCE_UPPER = 13
REFERENCE_WRIST = 17

NODES_FINGERS = [(4, 8, 12, 16, 20), (5, 5, 9, 13, 17), (17, 0, 0, 0, 0)]

class armDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
    
    def get_arms(self, image, pose, angles):
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
                left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
 
                # Calculate angle
                angles[12] = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angles[13] = calculate_angle(right_shoulder, right_elbow, right_wrist)    

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

            return image, angles

class handDetector():
    def __init__(self, n):
        self.mode = False
        self.maxHands = n
        self.detectionCon = 1
        self.trackCon = 0.5

        self.pTime_ = 0  # Used to calculate FPS

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils   

    
    
    def findHands(self,img, img_2, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img_2, handLms, self.mpHands.HAND_CONNECTIONS)
        return img_2

    def getNodesPosition(self):

        lmlist = []  # All cordinates of all nodes
        typelist = [] # All types of all nodes
        all_points = self.results.multi_hand_landmarks
        all_types = self.results.multi_handedness
        n = 0  # Go across the lmlist array

        if all_points:
            myHand = all_points[0]  # We use only one hand
            for landmark in myHand.landmark:
                lmlist.append(landmark)
                n += 1
            if(len(self.results.multi_hand_landmarks) == 2):
                myHand = all_points[1]  # We use two hands
                for landmark in myHand.landmark:
                    lmlist.append(landmark)
                    n += 1

        n = 0
        if all_types:
            myHand = all_types[0]  # We use only one hand
            for label in myHand.classification:
                typelist.append(label)
                n += 1
            if(len(self.results.multi_handedness) == 2):
                myHand = all_types[1]  # We use two hands
                for label in myHand.classification:
                    typelist.append(label)
                    n += 1
        return lmlist, typelist

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
    
    def getAngles(self, lmlist, typelist, angles, hand):
        # Get the angles for each finger
        nodes = []
        value = 0 + 21*hand

        if (typelist[hand].label == RIGHTSTRING):
            nodes = [0, 1, 2, 3, 4, 5]
            if lmlist[THUMB_FINGER+value].x >= lmlist[REFERENCE_WRIST+value].x:
                angles[nodes[5]] = 0
        elif (typelist[hand].label == LEFTSTRING):
            nodes = [6, 7, 8, 9, 10, 11]
            if (lmlist[THUMB_FINGER+value].x <= lmlist[REFERENCE_WRIST+value].x):
                angles[nodes[5]] = 0

        for i in range(0, 5):
            a = [lmlist[NODES_FINGERS[0][i]+value].x, lmlist[NODES_FINGERS[0][i]+value].y]
            b = [lmlist[NODES_FINGERS[1][i]+value].x, lmlist[NODES_FINGERS[1][i]+value].y]
            c = [lmlist[NODES_FINGERS[2][i]+value].x, lmlist[NODES_FINGERS[2][i]+value].y]
            angles[nodes[i]] = calculate_angle(a,b,c)      
        
        if (typelist[hand].label == RIGHTSTRING):
            if lmlist[THUMB_FINGER+value].x >= lmlist[REFERENCE_WRIST+value].x:
                angles[nodes[5]] = 0
        elif (typelist[hand].label == LEFTSTRING):
            if (lmlist[THUMB_FINGER+value].x <= lmlist[REFERENCE_WRIST+value].x):
                angles[nodes[5]] = 0

        return angles     
       
    def getFingersAngles(self, lmlist, typelist, angles):
        # Get the all hands fingers
        hands = len(typelist)%21
        
        if (hands >= 1):
            angles = self.getAngles(lmlist, typelist, angles, 0)

        if (hands == 2):
            angles = self.getAngles(lmlist, typelist, angles, 1)

        return angles
    
def calculate_angle(a, b, c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
        
        return int(angle)

def arrayToString (array):
    string= INIT_CHAR
    for i in array:
        string=string + str(i)

    return string

def usage_error():
    print("Usage: python3 hands_tacking.py --n <num_hands> (1-2)")
    sys.exit(1)

def print_angles(angles):

    print("\nLeft: ")

    for i in range(0, 6):
        print(f"  ", NAMES[i], angles[i])

    print(f"  ", NAMES[6], angles[12])
    
    print("\nRight: ")

    for i in range(6, 12):
        print(f"  ", NAMES[i-6], angles[i])

    print(f"  ", NAMES[6], angles[13])


def detect_hand(img, detector_hand, detector_arm, pose, ser):
    angles = [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
    img_2, angles = detector_arm.get_arms(img, pose, angles)
    img = detector_hand.findHands(img, img_2)  # Draws all the nodes and lines
    detector_hand.showFps(img)
    lmlist, typelist = detector_hand.getNodesPosition()

    if len(lmlist) and len(typelist) != 0:

        angles = detector_hand.getFingersAngles(lmlist, typelist, angles)

    
        out = [str(numero).zfill(3) for numero in angles]
        out = arrayToString(out)

        # print(out, "\n")
        print_angles(angles)

        # serialOut = bytes(out, 'utf-8')
        # ser.write(serialOut)
    
    # Shows the image
    cv2.imshow("Image", img)


def main():
    hand = -1

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        usage_error()

    # Get the number of hands and the hand you want
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--n" and i + 1 < len(sys.argv):
            hands = int(sys.argv[i + 1])

    if (hands != 1 and hands != 2):
        usage_error()

    cap = cv2.VideoCapture(0)
    detector_hand = handDetector(hands)
    detector_arm = armDetector()
    
    ser = 0  # Only used to try the tracking without arduino
    
    # ser = serial.Serial(
    #     port=PORT,
    #     baudrate=SERIALBEGIN,
    #     parity=serial.PARITY_NONE,
    #     stopbits=serial.STOPBITS_ONE,
    #     bytesize=serial.EIGHTBITS,
    #     timeout=1
    # )
    
    with detector_arm.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while True:
            success, img = cap.read()
       
            detect_hand(img, detector_hand, detector_arm, pose, ser)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
           
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
