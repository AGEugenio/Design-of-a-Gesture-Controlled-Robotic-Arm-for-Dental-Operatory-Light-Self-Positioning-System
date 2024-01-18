from PyQt5 import QtCore, QtGui, QtWidgets

import Adafruit_PCA9685
import time
import tkinter as tk
import threading
import numpy as np
import os

class ErrorDisplay(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.leftBTN.clicked.connect(self.closeWindow)
        self.rightBTN.clicked.connect(self.restart)
    def setupUi(self, ERROR):
        
        ERROR.setObjectName("ERROR")
        ERROR.resize(453, 192)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ERROR.setWindowIcon(icon)
        ERROR.setStyleSheet("background-color: rgb(227, 227, 227);")
        ERROR.setSizeGripEnabled(False)
        ERROR.setModal(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ERROR)
        self.verticalLayout_2.setContentsMargins(-1, 20, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.errorLabel = QtWidgets.QLabel(ERROR)
        self.errorLabel.setStyleSheet("\n"
        "color:rgb(255, 0, 0);\n"
        "font: 87 20pt \"Arial Black\";")
        self.errorLabel.setScaledContents(True)
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setObjectName("errorLabel")
        self.verticalLayout.addWidget(self.errorLabel)
        self.groupBox = QtWidgets.QGroupBox(ERROR)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFlat
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(-1, 15, -1, 10)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.leftBTN = QtWidgets.QPushButton(self.groupBox)
        self.leftBTN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.leftBTN.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.leftBTN.setObjectName("leftBTN")
        self.gridLayout.addWidget(self.leftBTN, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.errorMsg = QtWidgets.QLabel(self.groupBox)
        self.errorMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.errorMsg.setWordWrap(True)
        self.errorMsg.setObjectName("errorMsg")
        self.gridLayout.addWidget(self.errorMsg, 1, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 3, 1, 1)
        self.rightBTN = QtWidgets.QPushButton(self.groupBox)
        self.rightBTN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rightBTN.setStyleSheet("\n"
        "background-color: rgb(39, 68, 114);\n"
        "color: rgb(255, 255, 255);")
        self.rightBTN.setObjectName("rightBTN")
        self.gridLayout.addWidget(self.rightBTN, 3, 2, 1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 4)
        self.gridLayout.setRowStretch(2, 1)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        
        self.retranslateUi(ERROR)
        QtCore.QMetaObject.connectSlotsByName(ERROR)
        
    def retranslateUi(self, ERROR):
        _translate = QtCore.QCoreApplication.translate
        ERROR.setWindowTitle(_translate("ERROR", "ERROR"))
        self.errorLabel.setText(_translate("ERROR", "ERROR"))
        self.leftBTN.setText(_translate("ERROR", "Ignore"))
        self.errorMsg.setText(_translate("ERROR", "Sample Error Message. Do you want to restart the system?"))
        self.rightBTN.setText(_translate("ERROR", "Restart"))
    def closeWindow(self):
        self.close()
    def restart(self):
        os.system("sudo reboot")
        
class ServoControl(QtWidgets.QMainWindow):
   

    def __init__(self):
        super().__init__()
        
        
        self.showError=ErrorDisplay()
        try:
            # Initialize the PCA9685 PWM device
            self.pwm = Adafruit_PCA9685.PCA9685()

            # Frequency of the PWM signal
            self.pwm.set_pwm_freq(60)

        
        except Exception as E:
            print(E)
            global error_
            error_='1'
            self.showError.show()
            self.showError.errorMsg.setText("Motor problem")
       
         # Set up Servo motor range
        self.servo_min = 150  # Min pulse length out of 4096
        self.servo_max = 600  # Max pulse length out of 4096
        self.servo_range = self.servo_max - self.servo_min

        # Set up the servo channels
        self.servo_channels = [0, 1, 2, 3, 4, 5, 6, 7]

        # Speed of the servo motors
        self.servo_speed = 1

        # Dictionary to store the servo angle values
        self.servo_angles = {channel: 90 for channel in self.servo_channels}
       
        # Dictionary to store the label text
        self.servo_labels = {}
        
        #show UI
        self.servoUI()
        
       
       
    
    def servoUI(self):
        self.setWindowTitle("Servo Control")
        self.setGeometry(100, 100, 400, 300)
             
        # GUI that the list the servo motors and updates the angle of the servo motors
        for i in range(8):
            servo_label = QtWidgets.QLabel("Servo " + str(i+1) + " Angle: " + str(self.servo_angles[i]), self)
            servo_label.setGeometry(QtCore.QRect(10, 10+i*30, 200, 30))
            self.servo_labels[i] = servo_label
                
        self.show()

    # Function to control servo motor
    def set_servo_angle(self,channel, angle):
        try:
            last_angle = self.servo_angles[channel]
            step = 1 if angle > last_angle else - 1
            for i in np.arange(last_angle, angle, step):
                self.pwm.set_pwm(channel, 0, int(((i / 180) * (self.servo_max - self.servo_min)) + self.servo_min))
                time.sleep(0.03 / self.servo_speed)
            self.pwm.set_pwm(channel, 0, int(((angle / 180) * (self.servo_max - self.servo_min)) + self.servo_min))
            self.servo_angles[channel] = angle
            self.update_servo_angle(channel)
            
            #Set the limit of the angle of each servo motor
            angles = [max(70, min(last_angle, 110)), max(0, min(last_angle, 180)), max(0, min(last_angle,35)), max(45, min(last_angle, 70)), max(90, min(last_angle, 180)), max(0, min(last_angle, 180))]
           
            
        except Exception as E:
            print("Error", E)
            self.showError.show()
            self.showError.errorMsg.setText("Motor Driver not Found. Do you want to restart the system?")
       
              
    #Starting of servo motor position
    def start_arm_position(self):
        time.sleep(1)
        self.set_servo_angle(0, 110)#Done SHOULDER
        self.set_servo_angle(1, 70)#Done SHOULDER
        time.sleep(2)
        self.set_servo_angle(2, 84)#Done BASE
        self.set_servo_angle(3, 19)#Done ELBOW
        time.sleep(1)
        self.set_servo_angle(4, 110)#Done WRIST
        time.sleep(1)
        self.set_servo_angle(5, 138)#Done 5TH AXIS
        self.set_servo_angle(6, 0)#Done   6TH AXIS

        
                   
    # Function to update the angle of a servo
    def update_servo_angle(self, servo_number):
        self.servo_labels[servo_number].setText(f"Servo  {servo_number+1} Angle: {self.servo_angles[servo_number]}°")

    # 1st postion for the arm finger 1
    def position_1(self):
        self.set_servo_angle(0,70) #Default 90
        self.set_servo_angle(1,110) #Default 90
        self.set_servo_angle(2,102) #Default 115
        self.set_servo_angle(3,13) #Default 19
        self.set_servo_angle(4,77) #Default 80
        self.set_servo_angle(5,145) #Default 143
        self.set_servo_angle(6,25) #Default 60

    # 2nd postion for the arm finger 2
    def position_2(self):
       
        self.set_servo_angle(0,90) #Default 94
        self.set_servo_angle(1,90) #Default 86
        time.sleep(3)
        self.set_servo_angle(2,100) #Default 122
        self.set_servo_angle(3,0) #Default 0
        time.sleep(1) 
        self.set_servo_angle(4,103) #Default 95
        self.set_servo_angle(5,135) #Default 157
        self.set_servo_angle(6,36) #Default 66

    
    # 3rd postion for the arm finger 3
    def position_3(self):
        self.set_servo_angle(0,70) #Default 80
        self.set_servo_angle(1,110) #Default 100
        self.set_servo_angle(2,113) #Default 115
        self.set_servo_angle(3,0) #Default 28
        self.set_servo_angle(4,90) #Default 73
        self.set_servo_angle(5,125) #Default 180
        self.set_servo_angle(6,20) #Default 40

    # 4th postion for the arm finger 4
    def position_4(self):
        self.set_servo_angle(0,70) #Default 70
        self.set_servo_angle(1,110) #Default 110
        self.set_servo_angle(2,113) #Default 104
        self.set_servo_angle(3,21) #Default 0
        self.set_servo_angle(4,72) #Default 90
        self.set_servo_angle(5,125) #Default 161
        self.set_servo_angle(6,15) #Default 0
        
