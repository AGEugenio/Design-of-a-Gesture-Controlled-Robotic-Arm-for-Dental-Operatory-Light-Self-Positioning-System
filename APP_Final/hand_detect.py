"""
Hand Tracking Module
By: freeCodeCamp.org
Youtube: https://www.youtube.com/watch?v=01sAkU_NvOY

"""

# Needed libraries for image processing 
import cv2
import numpy as np


# This module is used to access the available classes 
# and functions of mediapipe framework                
import mediapipe as mp




class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        # IDs of the tip of thumb, index, middle, ring, and pinky
        self.tipIds = [4, 8, 12, 16, 20]

    # Function for accepting image and finding hand
    def find_hands(self, img, draw=True, flipType=True):


        self.results = self.hands.process(img)
        allHands = []
        h, w, c = img.shape

        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}

                # List for getting the coordinates of the detected hand
                mylmList = []
                xList = []
                yList = []

                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                # Identify the coordinates of the bounding box for the detectted hand
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                    bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                # Draw the bounding box
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20,
                                   bbox[1] + bbox[3] + 20),
                                  (255, 0, 0), 2)
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 0), 2)
        if draw:
            return allHands, img
        else:
            return allHands

    # Function for finding how many fingers are open
    def fingers_up(self, myHand):
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:

            # List for fingers that are up
            fingers = []

            # Thumb for right hand
            if myHandType == "Right":
                # If palm
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[4]][0]:
                    if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # If not palm
                else:
                    if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

            # Thumb for left hand
            else:
                # If palm
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[4]][0]:
                    if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # If not palm
                else:
                    if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

            # For the remaining four fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        # Count total fingers that are up
        totalFingers = fingers.count(1)
        return fingers, totalFingers

    def find_position(self, img, handNo=0, draw=False):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    # ID for pinky finger, can be changed
                    if id == 20:
                        cv2.circle(img, (cx, cy), 10,
                                   (255, 0, 255), cv2.FILLED)

        return lmlist
                 

def main():

    # Library used for measuring the elapsed time of a program
    import time
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    detector = HandDetector()

    while True:
        success, img = cap.read()
        hands, img = detector.find_hands(img, flipType=True)

        lmlist = detector.find_position(img, draw=True)
        if len(lmlist) != 0:
            print(lmlist[20])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.imshow("Image", img)
        cv2.waitKey(1)


def main_depthai():

    import depthai as dai
    detector = HandDetector()

    # Create pipeline
    pipeline = dai.Pipeline()

    # Define source and output
    camRgb = pipeline.create(dai.node.ColorCamera)
    xoutRgb = pipeline.create(dai.node.XLinkOut)

    xoutRgb.setStreamName("rgb")

    # Properties
    camRgb.setPreviewSize(500, 500)
    camRgb.setInterleaved(False)
    camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

    # Linking
    camRgb.preview.link(xoutRgb.input)

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:

        print('Connected cameras:', device.getConnectedCameraFeatures())
        # Print out usb speed
        print('Usb speed:', device.getUsbSpeed().name)
        # Bootloader version
        if device.getBootloaderVersion() is not None:
            print('Bootloader version:', device.getBootloaderVersion())
        # Device name
        print('Device name:', device.getDeviceName())

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            # Retrieve 'bgr' (opencv format) frame
            img = inRgb.getCvFrame()

            # success, img = cap.read()

            hands, img = detector.find_hands(img, flipType=True)

            lmlist = detector.find_position(img, draw=True)
            if len(lmlist) != 0:
                print(lmlist[20])

            cv2.imshow("Image", img)

            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
    main_depthai()
