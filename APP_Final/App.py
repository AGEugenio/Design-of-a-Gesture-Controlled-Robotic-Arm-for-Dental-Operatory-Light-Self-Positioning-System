# Required libraries for the UI 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Modules for the UI of the different windows of the App 
from instruct_window import Ui_Instructions
from main_win import Ui_MainWindow
from settings_window import Ui_Settings
from about_window import Ui_AboutWin
from error import Ui_ERROR
from passcode_window import Ui_Passcode
from devmode_win import Ui_DevWindow, ControlMotor, GetData


# These modules are for the Servo Control, Hand Detection, and Identifying Face Coordinates 
import servo_motor as sm
import hand_detect as hdm
import face_coord as fc


# The required libraries for Hand and Face Detection, as well as for Depthai Cam 
import cv2
import time
import depthai as dai
import blobconverter
import dlib
import numpy as np

#Import for Interacting with Operating System ###
import os

# Import for Interacting with the interpreter from within a Python program
import sys

#This module is for controlling the GPIO pins of RPI 
import RPi.GPIO as GPIO

#This module is for creating and managing threads 
import threading


class InstructWindow(QtWidgets.QMainWindow, Ui_Instructions):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setupUi(self)


class ErrorMsg(QtWidgets.QDialog, Ui_ERROR):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


class AboutWindow(QtWidgets.QMainWindow, Ui_AboutWin):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setupUi(self)


class SettingsWindow(QtWidgets.QWidget, Ui_Settings):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)


class DevWindow(QtWidgets.QMainWindow, Ui_DevWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.DataWorker = GetData()
        self.MotorWorker = ControlMotor()
        self.SPS = MainProc()
        self.setupUi(self)

        self.axis2_inc.clicked.connect(
            lambda: self.MotorWorker.increase_servo0and1_angle()
        )
        self.axis2_dec.clicked.connect(
            lambda: self.MotorWorker.decrease_servo0and1_angle()
        )
        self.axis1_inc.clicked.connect(
            lambda: self.MotorWorker.increase_servo2_base_angle()
        )
        self.axis1_dec.clicked.connect(
            lambda: self.MotorWorker.decrease_servo2_base_angle()
        )
        self.axis3_inc.clicked.connect(
            lambda: self.MotorWorker.increase_servo3_angle()
        )
        self.axis3_dec.clicked.connect(
            lambda: self.MotorWorker.decrease_servo3_angle()
        )
        self.axis4_inc.clicked.connect(
            lambda: self.MotorWorker.increase_servo4_angle()
        )
        self.axis4_dec.clicked.connect(
            lambda: self.MotorWorker.decrease_servo4_angle()
        )
        self.axis5_inc.clicked.connect(
            lambda: self.MotorWorker.increase_servo5_angle()
        )
        self.axis5_dec.clicked.connect(
            lambda: self.MotorWorker.decrease_servo5_angle()
        )
        self.axis6_inc.clicked.connect(
            lambda: self.MotorWorker.increase_servo6_angle()
        )
        self.axis6_dec.clicked.connect(
            lambda: self.MotorWorker.decrease_servo6_angle()
        )

        self.axis1_test.clicked.connect(self.MotorWorker.loopBase)
        self.axis2_test.clicked.connect(self.MotorWorker.loopShoulder)
        self.axis3_test.clicked.connect(self.MotorWorker.loopElbow)
        self.axis4_test.clicked.connect(self.MotorWorker.loopWrist)
        self.axis5_test.clicked.connect(self.MotorWorker.loopFifth)
        self.axis6_test.clicked.connect(self.MotorWorker.loopSixth)


class EnterPasscode(QtWidgets.QWidget, Ui_Passcode):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setupUi(self)
        self.go_back_btn.hide()
        self.passcode = ""
        self.back_btn.clicked.connect(self.backspace)
        for button in self.findChildren(QtWidgets.QPushButton):
            if button.text() not in ("done", ""):
                button.clicked.connect(self.button_clicked)


class SetPasscode(QtWidgets.QWidget, Ui_Passcode):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setupUi(self)
        self.resize(700, 450)
        self.go_back_btn.show()
        self.passcode = ""
        self.title_lbl.setText("SET PASSCODE")
        self.notif_lbl.setText("Leave it blank if you don't want a passcode")
        self.back_btn.clicked.connect(self.backspace)
        for button in self.findChildren(QtWidgets.QPushButton):
            if button.text() not in ("done", ""):
                button.clicked.connect(self.button_clicked)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.main_proc = MainProc()
        self.setupUi(self)

    def ImageUpdateSlot(self, Image):
        self.imageLBL.setPixmap(QPixmap.fromImage(Image))

    def StartFeed(self):
        self.main_proc.start()
        self.main_proc.ImageUpdate.connect(self.ImageUpdateSlot)


class MainProc(QThread):
    # Signal for updating the content of imageLBL
    ImageUpdate = pyqtSignal(QImage)

    # Function for connecting with DepthAI camera, Hand Detection, and Face Detection
    def run(self):
        self.ThreadActive = True
        global mouth_detect, button_reset, button_gesture

        detector = hdm.HandDetector(detectionCon=0.5, maxHands=1)
        get_coord = fc.CheckCoord()

        # Define Frame size
        FRAME_SIZE = (640, 460)

        # Define the NN model name and input size
        DET_INPUT_SIZE = (300, 300)
        model_name = "face-detection-retail-0004"
        zoo_type = "depthai"
        blob_path = None

        pipeline = dai.Pipeline()

        # Define a source – RGB camera
        cam = pipeline.createColorCamera()
        cam.setPreviewSize(FRAME_SIZE[0], FRAME_SIZE[1])
        cam.setInterleaved(False)
        cam.setResolution(
            dai.ColorCameraProperties.SensorResolution.THE_1080_P
        )
        cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
       

        cam.initialControl.setAutoFocusMode(
            dai.RawCameraControl.AutoFocusMode.OFF
        )
        cam.initialControl.setBrightness(-3)
        cam.initialControl.setContrast(2)
   
        # Define mono camera sources for stereo depth
        mono_left = pipeline.createMonoCamera()
        mono_left.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P
        )
        mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        mono_right = pipeline.createMonoCamera()
        mono_right.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P
        )
        mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        # Create stereo node
        stereo = pipeline.createStereoDepth()

        # Linking mono cam outputs to stereo node
        mono_left.out.link(stereo.left)
        mono_right.out.link(stereo.right)

        # Use blobconverter to get the blob of the required model
        if model_name is not None:
            blob_path = blobconverter.from_zoo(
                name=model_name,
                # The ‘shaves’ argument in blobconverter determines the number of SHAVE cores used to compile the neural network. The higher the value, the faster network can run.
                shaves=6,
                zoo_type=zoo_type,
            )

        # Define face detection NN node
        face_spac_det_nn = pipeline.createMobileNetSpatialDetectionNetwork()
        face_spac_det_nn.setConfidenceThreshold(0.75)
        face_spac_det_nn.setBlobPath(blob_path)
        face_spac_det_nn.setDepthLowerThreshold(100)
        face_spac_det_nn.setDepthUpperThreshold(5000)

        # Define face detection input config
        face_det_manip = pipeline.createImageManip()
        face_det_manip.initialConfig.setResize(
            DET_INPUT_SIZE[0], DET_INPUT_SIZE[1]
        )
        face_det_manip.initialConfig.setKeepAspectRatio(False)

        # Linking
        cam.preview.link(face_det_manip.inputImage)
        face_det_manip.out.link(face_spac_det_nn.input)
        stereo.depth.link(face_spac_det_nn.inputDepth)

        # Preview Output
        x_preview_out = pipeline.createXLinkOut()
        x_preview_out.setStreamName("preview")
        cam.preview.link(x_preview_out.input)

        # Detection Output
        det_out = pipeline.createXLinkOut()
        det_out.setStreamName("det_out")
        face_spac_det_nn.out.link(det_out.input)

        # Frame count
        frame_count = 0

        # Placeholder fps value
        fps = 0

        # Used to record the time when we processed last frames
        prev_frame_time = 0

        # Used to record the time at which we processed current frames
        new_frame_time = 0

        # Set status colors
        status_color = {
            "Face Detected": (0, 255, 0),
            "No Face Detected": (0, 0, 255),
        }

        # Load shape predictor for 68 landmarks
        shape_predictor = dlib.shape_predictor(
            "68_points/shape_predictor_68_face_landmarks.dat"
        )

        # List for detected hand gesture
        gestureList = []

        # While this thread is active, it will do the following tasks inside
        while self.ThreadActive:
            try:
                # Connect to device and start pipeline
                with dai.Device(pipeline) as device:
                    # Output queue will be used to get the right camera frames from the outputs defined above
                    q_cam = device.getOutputQueue(
                        name="preview", maxSize=1, blocking=False
                    )

                    # Output queue will be used to get nn data from the video frames
                    q_det = device.getOutputQueue(
                        name="det_out", maxSize=1, blocking=False
                    )

                    while True:
                        # Get right camera frame
                        in_cam = q_cam.get()
                        frame = in_cam.getCvFrame()

                        # Retrieve 'bgr' (opencv format) frame
                        img = frame

                        hands, img = detector.find_hands(img, flipType=True)

                        lmList = detector.find_position(img, draw=False)

                        # If button_gesture is true, it will detect hand gestures and put it into the list 'gestureList'
                        if button_gesture:
                            # If a hand is detected
                            if len(lmList) != 0:
                                hand = hands[0]
                                # List of which fingers are up
                                fingers, count = detector.fingers_up(hand)
                                # Show total count of fingers
                                cv2.putText(
                                    img,
                                    f"Gesture: {int(count)}",
                                    (445, 25),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2,
                                    (255, 0, 0),
                                    2,
                                )
                                gestureList.append(count)
                                print(gestureList[-1])

                            else:
                                print("NO HAND DETECTED")

                            # If button_gesture is false, it will stop hand detection and it will check the last detected hand gesture
                        else:
                            # If the gestureList has elements, it will check the last added gesture
                            if gestureList:
                                print(gestureList[-1])
                                ges = gestureList[-1]
                                if ges == 1:
                                    print("ONE")
                                    goMotor.position_1()
                                    mouth_detect = True
                                elif ges == 2:
                                    print("TWO")
                                    goMotor.position_2()
                                    mouth_detect = True
                                elif ges == 3:
                                    print("THREE")
                                    goMotor.position_3()
                                    mouth_detect = True
                                elif ges == 4:
                                    print("FOUR")
                                    goMotor.position_4()
                                    mouth_detect = True
                                elif ges == 5:
                                    print("FIVE")
                                    mouth_detect = False
                                else:
                                    print("Only 1 to 5")

                                gestureList.clear()
                                button_gesture = True

                            else:
                                print("GESTURELIST IS EMPTY")
                                button_gesture = True

                        # If button_reset is True, it will do the assigned reset position
                        if button_reset:
                            print("RESTING POSITION")
                            goMotor.start_arm_position()
                            mouth_detect = False

                        bbox = None
                        coordinates = None

                        inDet = q_det.tryGet()

                        # Get Coordinates
                        result = get_coord.coord_info(inDet, FRAME_SIZE)

                        if result is not None:
                            coordinates, bbox, face = result

                        # Check if a face was detected in the frame
                        if bbox:
                            global pan_angle, tilt_angle, pan_servo, tilt_servo
                            # Face detected
                            status = "Face Detected"

                            # Convert to grayscale
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                            # Get landmarks for face
                            landmarks = shape_predictor(gray, face)

                            # Extract coordinates for mouth
                            mouth_points = landmarks.parts()[48:68]
                            mouth_points = [[p.x, p.y] for p in mouth_points]
                            mouth_center = np.mean(
                                mouth_points, axis=0
                            ).astype(int)

                            # If mouth_detect is True, it will check the coordinates of mouth and move the motor
                            if mouth_detect:
                                # Get center of mouth
                                x, y = mouth_center
                                w, h = 40, 40
                                
                                # Draw bounding box around mouth
                                x_rec, y_rec, w_rec, h_rec = cv2.boundingRect(np.array(mouth_points))
                                cv2.rectangle(frame, (x_rec, y_rec), (x_rec + w_rec, y_rec + h_rec), (0, 0, 255), 2)
                               
                                # Calculate the pan and tilt angles based on the center coordinates
                                pan_error = x - img.shape[1] // 2
                                tilt_error = y - img.shape[0] // 2 - 15 #Default 100
                                pan_angle += pan_error / 50
                                tilt_angle += tilt_error / 50
                                pan_angle = min(max(pan_angle, 0), 180)
                                tilt_angle = min(max(tilt_angle, 0), 180)
                                # tilt_angle = 180 -  tilt_angle

                                # Move the servo motors to the new angles
                                goMotor.set_servo_angle(pan_servo, pan_angle)
                                goMotor.set_servo_angle(tilt_servo, tilt_angle)

                                # Display the frame with the face bounding box and servo angles
                                cv2.putText(
                                    img,
                                    "Pan: {:.1f} Tilt: {:.1f}".format(
                                        pan_angle, tilt_angle
                                    ),
                                    (20, 350),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,
                                    (0, 0, 255),
                                    2,
                                )
                            else:
                                pass

                        else:
                            # No face detected
                            status = "No Face Detected"

                            # Calculate average fps
                        if frame_count % 10 == 0:
                            # Time when we finish processing last 100 frames
                            new_frame_time = time.time()
                            # Fps will be number of frame processed in one second
                            fps = 1 / ((new_frame_time - prev_frame_time) / 10)
                            prev_frame_time = new_frame_time

                        # Display info on image
                        get_coord.display_info(
                            img, bbox, coordinates, status, status_color, fps
                        )

                        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        ConvertToQtFormat = QImage(
                            image.data,
                            image.shape[1],
                            image.shape[0],
                            QImage.Format_RGB888,
                        )
                        pic = ConvertToQtFormat.scaled(
                            640, 480, Qt.KeepAspectRatio
                        )
                        # Update the imageLBL with the pic
                        self.ImageUpdate.emit(pic)

                        # Increment frame count
                        frame_count += 1

            except Exception as E:
                print(E)
                camError.show()
                camError.errorMsg.setText(
                    "Camera not Found. Do you want to restart?"
                )


def verify_code(w1, w2, code, label):
    input_code = code

    # Read the passwords file
    with open("passwords.txt", "r") as f:
        lines = f.readlines()
        f.close()

    # Search for the saved passcode
    for line in lines:
        line = line.strip()
        parts = line.split(":")
        if parts[0] == "passcode":
            saved_password = parts[1]

            # Compare the entered password to the saved password
            if saved_password == input_code:
                QMessageBox.information(
                    w1, "Login successful", "You have successfully logged in!"
                )
                w1.close()
                w2.show()
                return

    # If no match was found, show an error message
    QMessageBox.warning(w1, "Login failed", "Invalid password.")

    return


def edit_code(w1, code):
    input_code = code
    digits = len(code)

    if digits == 4 or digits == 0:
        # update passwords.txt file with new password
        with open("passwords.txt", "w") as f:
            f.write(f"passcode:{input_code}\n")
            QtWidgets.QMessageBox.information(
                w1, "Password Updated", "Your password has been updated."
            )
            w1.close()
    else:
        QtWidgets.QMessageBox.warning(
            w1, "Invalid Password", "It should be 4 digits."
        )


def check_passcode():
    # Read the passcode file
    with open("passwords.txt", "r") as f:
        lines = f.readlines()
        f.close()

    # Search for the passcode and check the saved passcode
    for line in lines:
        line = line.strip()
        parts = line.split(":")
        if parts[0] == "passcode":
            saved_password = parts[1]

            # Compare the entered passcode to the saved password
            if saved_password == "":
                ins_win.show()
                return
            else:
                code_win.show()
                return


# Function for checking the state of pedal switch for capturing the gesture
def button_call_gesture(channel):
    global button_gesture
    # Read the button state
    button_input = GPIO.input(channel)
    # If the pedal switch is pressed, it will get gesture
    if button_input == GPIO.HIGH:
        button_gesture = True
    else:
        button_gesture = False
    time.sleep(0.01)


# Function for checking the state of pedal switch for reset
def button_call_reset(channel):
    global button_reset
    # Read the button state
    button_input = GPIO.input(channel)
    # If the pedal switch is pressed, it will move the robot arm into resting position
    if button_input == GPIO.HIGH:
        button_reset = True
    else:
        button_reset = False
    time.sleep(0.01)


# Function for changing value of button_gesture and button_reset


def check_switch():
    while True:
        button_call_gesture(23)
        button_call_reset(25)


def display_dev():
    dev_win.show()
    dev_win.StartUpdate()
    set_win.hide()
    main_win.hide()


def startMain(w1):
    switch_.start()
    w1.close()
    main_win.show()
    main_win.StartFeed()


def changeWindow(w1, w2):
    w1.hide()
    w2.show()


def closeWindow(w1):
    w1.close()


def shutdown():
    os.system("sudo shutdown -h now")


def restart():
    os.system("sudo reboot")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ins_win = InstructWindow()
    main_win = MainWindow()
    about_win = AboutWindow()
    set_win = SettingsWindow()
    code_win = EnterPasscode()
    set_code = SetPasscode()
    dev_win = DevWindow()
    camError = ErrorMsg()

    goMotor = sm.ServoControl()
    errorMotor = sm.ErrorDisplay()

    # Set up the channel of pan_servo and tilt_servo
    pan_servo = 5
    tilt_servo = 6

    # Set the initial pan and tilt angles to the center position
    pan_angle = 135 #changed from 180 to 90     #Default 143
    tilt_angle = 30                        #Default 70
    goMotor.start_arm_position()

    # Set the pan and tilt increment values
    pan_increment = 1
    tilt_increment = 1

    # sets the numbering mode used for the GPIO pins
    GPIO.setmode(GPIO.BCM)

    # sets the direction of a GPIO pin and resistor state of the pin
    # GPIO.IN means it will be an INPUT pin or it will be used to read a signal
    # GPIO.PUD_DOWN means that pin is normally low (0V) when nothing is connected to it
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    button_gesture = True
    button_reset = False
    mouth_detect = False

    # Create a new thread which will run check_switch function
    switch_ = threading.Thread(target=check_switch)

    ins_win.continue_btn.clicked.connect(lambda: startMain(ins_win))

    main_win.settingsBTN.clicked.connect(lambda: set_win.show())
    main_win.aboutBTN.clicked.connect(
        lambda: changeWindow(main_win, about_win)
    )

    about_win.back_btn.clicked.connect(
        lambda: changeWindow(about_win, main_win)
    )

    set_win.setBTN.clicked.connect(lambda: changeWindow(set_win, set_code))
    set_win.shutBTN.clicked.connect(shutdown)
    set_win.rebootBTN.clicked.connect(restart)
    set_win.devBTN.clicked.connect(display_dev)

    camError.leftBTN.clicked.connect(lambda: closeWindow(camError))
    camError.rightBTN.clicked.connect(restart)

    code_win.enter_btn.clicked.connect(
        lambda: verify_code(
            code_win, ins_win, code_win.passcode, code_win.passcode_lbl
        )
    )
    set_code.enter_btn.clicked.connect(
        lambda: edit_code(set_code, set_code.passcode)
    )
    set_code.go_back_btn.clicked.connect(
        lambda: changeWindow(set_code, set_win)
    )
    dev_win.back_btn.clicked.connect(lambda: changeWindow(dev_win, main_win))

    check_passcode()

    sys.exit(app.exec_())
