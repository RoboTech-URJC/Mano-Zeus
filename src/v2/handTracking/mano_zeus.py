#############################################
## github:    madport                      ##
## github:    vbarcena2020                 ##
#############################################

##############################################################################################
##                                                                                          ##
## You have to select how many hands you want and if it is only one wich one example        ##
##                                                                                          ##
## Usage: python3 mano_zeus.py --n 2            # detect two hands                          ##
##                                                                                          ##
## Usage: python3 mano_zeus.py --n 1            # detect one hand                           ##
##                                                                                          ##
##############################################################################################

import cv2
import mediapipe as mp
import time
import serial
import sys
import numpy as np
import symbols
import tkinter as tk
from PIL import Image, ImageTk


#PORT = '/dev/ttyACM0'
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

USED_FACE_NODES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

manualangles = [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

traces = False
arms = True
mode = 0
root = tk.Tk()


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Mano Zeus")

        # Create two areas to show images
        self.img_label1 = tk.Label(self.root)
        self.img_label1.pack(side="left", padx=10, pady=10)

        self.img_label2 = tk.Label(self.root)
        self.img_label2.pack(side="right", padx=10, pady=10)

        # Create label
        self.l = tk.Label(root, text = "CHANGE MODE")
        self.l.config(font =("Courier", 20, "bold"))
        self.l.pack(side="top", pady= 5)

        self.l_2 = tk.Label(root, text = "MODE" + str(mode+1), fg="blue")
        self.l_2.config(font =("Courier", 15, "bold"))
        self.l_2.pack(side="top", pady= 5)

        # Buttons
        self.button1 = tk.Button(self.root, text="Mode 1: SYMBOLS", command=self.button_mode1)
        self.button1.pack(side="top", pady=5)

        self.button2 = tk.Button(self.root, text="Mode 2: HANDS", command=self.button_mode2)
        self.button2.pack(side="top", pady=5)

        self.button3 = tk.Button(self.root, text="Mode 3: FACE", command=self.button_mode3)
        self.button3.pack(side="top", pady=5)

        self.button4 = tk.Button(self.root, text="Mode 4: MANUAL", command=self.button_mode4)
        self.button4.pack(side="top", pady=5)

        self.label_manual = tk.Label(self.root, text = "MANUAL MODE")
        self.label_manual.config(font =("Courier", 20, "bold"))
        self.label_manual.pack(side="top", pady= 5)

        self.buttonmove = tk.Button(self.root, text="MOVE", command=self.button_move)
        self.buttonmove.pack(side="top", pady=5)

        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.pack()

        left_label = tk.Label(self.slider_frame, text="LEFT")
        left_label.grid(row=0, column=1)
        
        right_label = tk.Label(self.slider_frame, text="RIGHT")
        right_label.grid(row=0, column=2)

        # Crear 12 sliders y organizarlos en dos columnas de 6 dentro del frame
        self.sliders = []
        for i in range(12):
            if i < 6:
                # Colocar las etiquetas con números a la izquierda de los sliders
                tk.Label(self.slider_frame, text=str(NAMES[i])).grid(row=i + 1, column=0)

            slider = tk.Scale(self.slider_frame, from_=0, to=180, orient=tk.HORIZONTAL, troughcolor="red")
            slider.set(180)  # Establecer valor inicial en 180
            self.sliders.append(slider)
            # Colocarlos en una cuadrícula: 6 filas y 2 columnas dentro del frame
            slider.grid(row=(i % 6) + 1, column=(i // 6) + 1)

        self.label_manual = tk.Label(self.root, text = "OTHERS")
        self.label_manual.config(font =("Courier", 20, "bold"))
        self.label_manual.pack(side="top", pady= 5)

        self.buttontraces = tk.Button(self.root, text="Show/hide traces", command=self.button_traces)
        self.buttontraces.pack(side="top", pady=5)

        self.buttonarms = tk.Button(self.root, text="Show/hide arms", command=self.button_arms)
        self.buttonarms.pack(side="top", pady=5)

        self.buttonexit = tk.Button(self.root, text="EXIT", command=self.button_exit)
        self.buttonexit.pack(side="top", pady=5)

    def button_move(self):
        global mode, manualangles
        if mode == symbols.MANUAL_MODE:
            values = [slider.get() for slider in self.sliders]
            values.append(180)
            values.append(180)
            print(f"Valores actuales de los sliders: {values}")
            manualangles = values
        else:
            print("Manual mode not active")

    def update_sliders(self):
        if mode == symbols.MANUAL_MODE:
            i = 0
            for slider in self.sliders:
                if slider.get() == manualangles[i]:
                    slider.config(troughcolor="green")
                else: 
                    slider.config(troughcolor="yellow")
                i = i+1
        else:
            for slider in self.sliders:
                slider.config(troughcolor="red")
        self.root.update_idletasks()


    def update_images(self, img1, img2):    
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        self.img1 = ImageTk.PhotoImage(Image.fromarray(img1_rgb))
        self.img2 = ImageTk.PhotoImage(Image.fromarray(img2_rgb))

        self.img_label1.config(image=self.img1)
        self.img_label2.config(image=self.img2)

        self.root.update_idletasks()
    
    def update_text(self):
        global mode
        
        # Mostrar las imágenes en las etiquetas
        self.l_2.config(text="MODE " + str(mode+1))

        self.root.update_idletasks()

    def button_mode1(self):
        global mode
        mode = 0

    def button_mode2(self):
        #global mode
        #mode = 1
        print("""\n\n\n\n\n\n
        **********************************************
        * APLICACIÓN CAPADA PARA DEMOS.              *
        * SI NO TIENES UNA MANO CONECTADA NO LA     *
        * HABILITES. PETA EL PROGRAMA.               *
        * PARA HABILITAR ESTA FUNCIÓN CHECKEA LA    *
        * LÍNEA 198 DEL CÓDIGO                       *
        **********************************************
        \n\n\n\n\n\n""")

    def button_mode3(self):
        global mode
        mode = 2

    def button_mode4(self):
        #global mode
        #mode = 3
        print("""\n\n\n\n\n\n
        **********************************************
        * APLICACIÓN CAPADA PARA DEMOS.              *
        * SI NO TIENES UNA MANO CONECTADA NO LA     *
        * HABILITES. PETA EL PROGRAMA.               *
        * PARA HABILITAR ESTA FUNCIÓN CHECKEA LA    *
        * LÍNEA 221 DEL CÓDIGO                       *
        **********************************************
        \n\n\n\n\n\n""")    
    def button_traces(self):
        global traces
        traces = not traces

    def button_arms(self):
        global arms
        arms = not arms

    def button_exit(self):
        root.quit()

class faceDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
    
    def get_face(self, image, pose):
        face_landmarks = []

        # Recolor image to RGB, make detection and recolor back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            for landmark in USED_FACE_NODES:
                face_landmarks.append((int(landmarks[landmark].x * image.shape[1]), int(landmarks[landmark].y * image.shape[0])))
            
                cv2.circle(image, face_landmarks[landmark], 5, (255, 0, 0), -1)      
            
        except:
            pass

        return image

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
            
            if arms:
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

def get_symbol(angles):
    left_status = [1, 1, 1, 1, 1, 1, 1]
    right_status = [1, 1, 1, 1, 1, 1, 1]
    for i in range(0, 6):  # don't check the elbows
        if angles[i] < 100:
            left_status[i] = 0

    for i in range(0, 6):  # don't check the elbows
        if angles[i+6] < 100:
            right_status[i] = 0
    
    return left_status, right_status

def show_hands(angles, image, color):

    point = [(250, 140), (200, 100), (130, 70), (80, 90), (40, 140), (170, 320), (330, 140), (380, 100), (450, 70), (500, 90), (540, 140), (410, 320)]  
    font = cv2.FONT_HERSHEY_SIMPLEX 
    size = 0.75  
    thick = 2  
    line = cv2.LINE_AA
    for i in range (0, 12):
        cv2.putText(image, str(angles[i]), point[i], font, size, color, thick, line)

    return image

def detect_hand(img, detector_hand, detector_arm, detector_face, pose, ser, app):
    global mode, manualangles
    angles = [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
    image = cv2.imread('hands.jpg') 
    image = cv2.flip(image,1)
    img_2 = img
    if arms:
        img_2, angles = detector_arm.get_arms(img, pose, angles)

    if mode != symbols.MANUAL_MODE:
        img = detector_hand.findHands(img, img_2)  # Draws all the nodes and lines
    img = cv2.flip(img,1)

    detector_hand.showFps(img)
    if mode != symbols.MANUAL_MODE:
        lmlist, typelist = detector_hand.getNodesPosition()

        if len(lmlist) and len(typelist) != 0:
            angles = detector_hand.getFingersAngles(lmlist, typelist, angles)
        
            out = [str(numero).zfill(3) for numero in angles]
            out = arrayToString(out)

            # print(out, "\n")
            left_status, right_status = get_symbol(angles)
            mode = symbols.change_mode(left_status, right_status, mode)

            if mode == symbols.MOVE_MODE:
                if traces:
                    print_angles(angles)
                image = show_hands(angles, image, color=(0, 255, 0))
                if traces:
                    print("\n-----------------------------------------------------------------------\n")
                serialOut = bytes(out, 'utf-8')
                ser.write(serialOut)
            elif mode == symbols.SYMBOLS_MODE:
                image = symbols.get_symbols(left_status, right_status)
                image = cv2.flip(image,1)
                image = show_hands(angles, image, color=(0, 0, 255))
            elif mode == symbols.FACE_MODE:
                image = show_hands(angles, image, color=(0, 0, 255))

            

    elif mode == symbols.MANUAL_MODE:
        image = show_hands(manualangles, image, color=(0, 255, 0))
        out = [str(numero).zfill(3) for numero in manualangles]
        out = arrayToString(out)
        serialOut = bytes(out, 'utf-8')
        ser.write(serialOut)

    if mode == symbols.MOVE_MODE or mode == symbols.MANUAL_MODE:
        cv2.putText(image, "ON", (290, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(image, "OFF", (285, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.putText(image, "LEFT", (120, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, "RIGHT", (430, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    if mode == symbols.FACE_MODE:
        img = detector_face.get_face(img, pose)

    # Shows the image
    # cv2.imshow("Image", img)
    # cv2.imshow("hands", image)
    app.update_text()
    app.update_images(img,image)
    app.update_sliders()

def update_frame(cap, detector_hand, detector_arm, detector_face, pose, ser, app, root):
    global mode

    success, img = cap.read()

    if success:
        detect_hand(img, detector_hand, detector_arm, detector_face, pose, ser, app)

    root.after(10, update_frame, cap, detector_hand, detector_arm, detector_face, pose, ser, app, root)

def main():
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
    detector_face = faceDetector()

    # ser = 0  # Only used to try the tracking without arduino
    
    ser = serial.Serial(
       # port=PORT,
        baudrate=SERIALBEGIN,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    app = Interface(root)

    with detector_arm.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        root.after(0, update_frame, cap, detector_hand, detector_arm, detector_face, pose, ser, app, root)

        root.mainloop()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
