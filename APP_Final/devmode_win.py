from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import serial
import time
import Adafruit_PCA9685
import numpy as np
import depthai
from PyQt5.QtWidgets import QMessageBox
import subprocess


try:
    #This code is only for getting the serial monitor from the arduino to the python
    # set up the serial connection with the Arduino
    ser = serial.Serial('/dev/ttyACM0', 38400)
except Exception as E:
    print("Error", E)
      

# define the delimeter character
delimeter = ','
driver=False
try:
    # Initialize the PCA9685 PWM device
    pwm = Adafruit_PCA9685.PCA9685()

    # Frequency of the PWM signal
    pwm.set_pwm_freq(60)
    driver=True

except Exception as E: 
      print("Error", E)
      driver=False

# Set up Servo motor range
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_range = servo_max - servo_min

# Set up the servo channels
servo_channels = [0, 1, 2, 3, 4, 5, 6, 7]

# Speed of the servo motors
servo_speed = 1

# Dictionary to store the servo angle values
servo_angles = {channel: 90 for channel in servo_channels}

#Setting the initial angles at the resting state of arm
servo_angles[0]=90
servo_angles[1]=90
servo_angles[2]=90
servo_angles[3]=30
servo_angles[4]=90
servo_angles[5]=140
servo_angles[6]=0

# Dictionary to store the label text
servo_labels = {}

Potentiometer1=0
Potentiometer2=0
Potentiometer3=0
Potentiometer4=0
Potentiometer5=0
Potentiometer6=0

pot_channel = {}

channel0=False

class Ui_DevWindow(object):
       
    def setupUi(self, DevWindow):
        DevWindow.setObjectName("DevWindow")
        DevWindow.resize(800, 480)
        DevWindow.setMinimumSize(QtCore.QSize(800, 480))
        DevWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.centralwidget = QtWidgets.QWidget(DevWindow)
        self.centralwidget.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.VL1 = QtWidgets.QVBoxLayout()
        self.VL1.setObjectName("VL1")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.back_btn.sizePolicy().hasHeightForWidth())
        self.back_btn.setSizePolicy(sizePolicy)
        self.back_btn.setMinimumSize(QtCore.QSize(30, 30))
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back_btn.setStyleSheet("QPushButton{\n"
                                    "    font: 9pt \"Arial\";\n"
                                    "    color: rgb(0, 0, 0);}\n"
                                    "\n"
                                    "QPushButton:pressed{ \n"
                                    "    color: rgb(39, 68, 139);\n"
                                    "    border:0pt;\n"
                                    "}")
        self.back_btn.setFlat(True)
        self.back_btn.setObjectName("back_btn")
        self.VL1.addWidget(self.back_btn)
        self.HL1 = QtWidgets.QHBoxLayout()
        self.HL1.setObjectName("HL1")
        self.VL2 = QtWidgets.QVBoxLayout()
        self.VL2.setContentsMargins(5, -1, 5, -1)
        self.VL2.setObjectName("VL2")
        spacerItem = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.VL2.addItem(spacerItem)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(10, -1, 10, -1)
        self.gridLayout_4.setVerticalSpacing(40)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.axis1_val = QtWidgets.QLabel(self.centralwidget)
        self.axis1_val.setStyleSheet("\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.axis1_val.setAlignment(QtCore.Qt.AlignCenter)
        self.axis1_val.setObjectName("axis1_val")
        self.gridLayout_4.addWidget(self.axis1_val, 2, 3, 1, 1)
        self.axis4_dec = QtWidgets.QPushButton(self.centralwidget)
        self.axis4_dec.setMinimumSize(QtCore.QSize(30, 30))
        self.axis4_dec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis4_dec.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis4_dec.setObjectName("axis4_dec")
        self.gridLayout_4.addWidget(self.axis4_dec, 5, 1, 1, 1)
        self.axis2_test = QtWidgets.QPushButton(self.centralwidget)
        self.axis2_test.setMinimumSize(QtCore.QSize(60, 30))
        self.axis2_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis2_test.setStyleSheet("QPushButton{\n"
                                      "border: none;\n"
                                      "border-radius:15px;\n"
                                      "background-color: rgb(212, 211, 197);\n"
                                      "color: rgb(25, 25, 25);\n"
                                      "\n"
                                      "font: 12pt \"Arial\";\n"
                                      "\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed{ \n"
                                      "    border-radius:5px;\n"
                                      "    background-color: rgb(197, 220, 227);\n"
                                      "    color: rgb(25, 25, 25);}")
        self.axis2_test.setObjectName("axis2_test")
        self.gridLayout_4.addWidget(self.axis2_test, 3, 5, 1, 1)
        self.axis2_val2 = QtWidgets.QLabel(self.centralwidget)
        self.axis2_val2.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                      "\n"
                                      "color: rgb(18, 18, 18);\n"
                                      "")
        self.axis2_val2.setAlignment(QtCore.Qt.AlignCenter)
        self.axis2_val2.setObjectName("axis2_val2")
        self.gridLayout_4.addWidget(self.axis2_val2, 3, 4, 1, 1)
        self.axis5_lbl = QtWidgets.QLabel(self.centralwidget)
        self.axis5_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "\n"
                                     "color: rgb(39, 68, 114);")
        self.axis5_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.axis5_lbl.setObjectName("axis5_lbl")
        self.gridLayout_4.addWidget(self.axis5_lbl, 6, 2, 1, 1)
        self.axis2_dec = QtWidgets.QPushButton(self.centralwidget)
        self.axis2_dec.setMinimumSize(QtCore.QSize(30, 30))
        self.axis2_dec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis2_dec.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis2_dec.setObjectName("axis2_dec")
        self.gridLayout_4.addWidget(self.axis2_dec, 3, 1, 1, 1)
        self.axis2_val = QtWidgets.QLabel(self.centralwidget)
        self.axis2_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.axis2_val.setAlignment(QtCore.Qt.AlignCenter)
        self.axis2_val.setObjectName("axis2_val")
        self.gridLayout_4.addWidget(self.axis2_val, 3, 3, 1, 1)
        self.axis2_inc = QtWidgets.QPushButton(self.centralwidget)
        self.axis2_inc.setMinimumSize(QtCore.QSize(30, 30))
        self.axis2_inc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis2_inc.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis2_inc.setObjectName("axis2_inc")
        self.gridLayout_4.addWidget(self.axis2_inc, 3, 0, 1, 1)
        self.axis4_val = QtWidgets.QLabel(self.centralwidget)
        self.axis4_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.axis4_val.setAlignment(QtCore.Qt.AlignCenter)
        self.axis4_val.setObjectName("axis4_val")
        self.gridLayout_4.addWidget(self.axis4_val, 5, 3, 1, 1)
        self.axis4_inc = QtWidgets.QPushButton(self.centralwidget)
        self.axis4_inc.setMinimumSize(QtCore.QSize(30, 30))
        self.axis4_inc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis4_inc.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis4_inc.setObjectName("axis4_inc")
        self.gridLayout_4.addWidget(self.axis4_inc, 5, 0, 1, 1)
        self.axis1_inc = QtWidgets.QPushButton(self.centralwidget)
        self.axis1_inc.setMinimumSize(QtCore.QSize(30, 30))
        self.axis1_inc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis1_inc.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis1_inc.setObjectName("axis1_inc")
        self.gridLayout_4.addWidget(self.axis1_inc, 2, 0, 1, 1)
        self.axis5_test = QtWidgets.QPushButton(self.centralwidget)
        self.axis5_test.setMinimumSize(QtCore.QSize(60, 30))
        self.axis5_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis5_test.setStyleSheet("QPushButton{\n"
                                      "border: none;\n"
                                      "border-radius:15px;\n"
                                      "background-color: rgb(212, 211, 197);\n"
                                      "color: rgb(25, 25, 25);\n"
                                      "\n"
                                      "font: 12pt \"Arial\";\n"
                                      "\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed{ \n"
                                      "    border-radius:5px;\n"
                                      "    background-color: rgb(197, 220, 227);\n"
                                      "    color: rgb(25, 25, 25);}")
        self.axis5_test.setObjectName("axis5_test")
        self.gridLayout_4.addWidget(self.axis5_test, 6, 5, 1, 1)
        self.axis1_test = QtWidgets.QPushButton(self.centralwidget)
        self.axis1_test.setMinimumSize(QtCore.QSize(60, 30))
        self.axis1_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis1_test.setStyleSheet("QPushButton{\n"
                                      "border: none;\n"
                                      "border-radius:15px;\n"
                                      "background-color: rgb(212, 211, 197);\n"
                                      "color: rgb(25, 25, 25);\n"
                                      "\n"
                                      "font: 12pt \"Arial\";\n"
                                      "\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed{ \n"
                                      "    border-radius:5px;\n"
                                      "    background-color: rgb(197, 220, 227);\n"
                                      "    color: rgb(25, 25, 25);}")
        self.axis1_test.setObjectName("axis1_test")
        self.gridLayout_4.addWidget(self.axis1_test, 2, 5, 1, 1)
        self.axis2_lbl = QtWidgets.QLabel(self.centralwidget)
        self.axis2_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "color: rgb(39, 68, 114);")
        self.axis2_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.axis2_lbl.setObjectName("axis2_lbl")
        self.gridLayout_4.addWidget(self.axis2_lbl, 3, 2, 1, 1)
        self.axis4_lbl = QtWidgets.QLabel(self.centralwidget)
        self.axis4_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "color: rgb(39, 68, 114);")
        self.axis4_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.axis4_lbl.setObjectName("axis4_lbl")
        self.gridLayout_4.addWidget(self.axis4_lbl, 5, 2, 1, 1)
        self.axis5_inc = QtWidgets.QPushButton(self.centralwidget)
        self.axis5_inc.setMinimumSize(QtCore.QSize(30, 30))
        self.axis5_inc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis5_inc.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis5_inc.setObjectName("axis5_inc")
        self.gridLayout_4.addWidget(self.axis5_inc, 6, 0, 1, 1)
        self.axis6_test = QtWidgets.QPushButton(self.centralwidget)
        self.axis6_test.setMinimumSize(QtCore.QSize(60, 30))
        self.axis6_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis6_test.setStyleSheet("QPushButton{\n"
                                      "border: none;\n"
                                      "border-radius:15px;\n"
                                      "background-color: rgb(212, 211, 197);\n"
                                      "color: rgb(25, 25, 25);\n"
                                      "\n"
                                      "font: 12pt \"Arial\";\n"
                                      "\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed{ \n"
                                      "    border-radius:5px;\n"
                                      "    background-color: rgb(197, 220, 227);\n"
                                      "    color: rgb(25, 25, 25);}")
        self.axis6_test.setObjectName("axis6_test")
        self.gridLayout_4.addWidget(self.axis6_test, 7, 5, 1, 1)
        self.axis3_test = QtWidgets.QPushButton(self.centralwidget)
        self.axis3_test.setMinimumSize(QtCore.QSize(60, 30))
        self.axis3_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis3_test.setStyleSheet("QPushButton{\n"
                                      "border: none;\n"
                                      "border-radius:15px;\n"
                                      "background-color: rgb(212, 211, 197);\n"
                                      "color: rgb(25, 25, 25);\n"
                                      "\n"
                                      "font: 12pt \"Arial\";\n"
                                      "\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed{ \n"
                                      "    border-radius:5px;\n"
                                      "    background-color: rgb(197, 220, 227);\n"
                                      "    color: rgb(25, 25, 25);}")
        self.axis3_test.setObjectName("axis3_test")
        self.gridLayout_4.addWidget(self.axis3_test, 4, 5, 1, 1)
        self.axis1_lbl = QtWidgets.QLabel(self.centralwidget)
        self.axis1_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "\n"
                                     "\n"
                                     "color: rgb(39, 68, 114);")
        self.axis1_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.axis1_lbl.setObjectName("axis1_lbl")
        self.gridLayout_4.addWidget(self.axis1_lbl, 2, 2, 1, 1)
        self.axis5_val = QtWidgets.QLabel(self.centralwidget)
        self.axis5_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.axis5_val.setAlignment(QtCore.Qt.AlignCenter)
        self.axis5_val.setObjectName("axis5_val")
        self.gridLayout_4.addWidget(self.axis5_val, 6, 3, 1, 1)
        self.axis6_inc = QtWidgets.QPushButton(self.centralwidget)
        self.axis6_inc.setMinimumSize(QtCore.QSize(30, 30))
        self.axis6_inc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis6_inc.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis6_inc.setObjectName("axis6_inc")
        self.gridLayout_4.addWidget(self.axis6_inc, 7, 0, 1, 1)
        self.axis3_dec = QtWidgets.QPushButton(self.centralwidget)
        self.axis3_dec.setMinimumSize(QtCore.QSize(30, 30))
        self.axis3_dec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis3_dec.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis3_dec.setObjectName("axis3_dec")
        self.gridLayout_4.addWidget(self.axis3_dec, 4, 1, 1, 1)
        self.axis6_val = QtWidgets.QLabel(self.centralwidget)
        self.axis6_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.axis6_val.setAlignment(QtCore.Qt.AlignCenter)
        self.axis6_val.setObjectName("axis6_val")
        self.gridLayout_4.addWidget(self.axis6_val, 7, 3, 1, 1)
        self.axis5_dec = QtWidgets.QPushButton(self.centralwidget)
        self.axis5_dec.setMinimumSize(QtCore.QSize(30, 30))
        self.axis5_dec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis5_dec.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis5_dec.setObjectName("axis5_dec")
        self.gridLayout_4.addWidget(self.axis5_dec, 6, 1, 1, 1)
        self.axis4_test = QtWidgets.QPushButton(self.centralwidget)
        self.axis4_test.setMinimumSize(QtCore.QSize(60, 30))
        self.axis4_test.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis4_test.setStyleSheet("QPushButton{\n"
                                      "border: none;\n"
                                      "border-radius:15px;\n"
                                      "background-color: rgb(212, 211, 197);\n"
                                      "color: rgb(25, 25, 25);\n"
                                      "\n"
                                      "font: 12pt \"Arial\";\n"
                                      "\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed{ \n"
                                      "    border-radius:5px;\n"
                                      "    background-color: rgb(197, 220, 227);\n"
                                      "    color: rgb(25, 25, 25);}")
        self.axis4_test.setObjectName("axis4_test")
        self.gridLayout_4.addWidget(self.axis4_test, 5, 5, 1, 1)
        self.axis6_dec = QtWidgets.QPushButton(self.centralwidget)
        self.axis6_dec.setMinimumSize(QtCore.QSize(30, 30))
        self.axis6_dec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis6_dec.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis6_dec.setObjectName("axis6_dec")
        self.gridLayout_4.addWidget(self.axis6_dec, 7, 1, 1, 1)
        self.axis6_lbl = QtWidgets.QLabel(self.centralwidget)
        self.axis6_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "color: rgb(39, 68, 114);")
        self.axis6_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.axis6_lbl.setObjectName("axis6_lbl")
        self.gridLayout_4.addWidget(self.axis6_lbl, 7, 2, 1, 1)
        self.axis1_dec = QtWidgets.QPushButton(self.centralwidget)
        self.axis1_dec.setMinimumSize(QtCore.QSize(30, 30))
        self.axis1_dec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis1_dec.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis1_dec.setObjectName("axis1_dec")
        self.gridLayout_4.addWidget(self.axis1_dec, 2, 1, 1, 1)
        self.axis3_inc = QtWidgets.QPushButton(self.centralwidget)
        self.axis3_inc.setMinimumSize(QtCore.QSize(30, 30))
        self.axis3_inc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.axis3_inc.setStyleSheet("\n"
                                     "\n"
                                     "\n"
                                     "QPushButton{\n"
                                     "border: none;\n"
                                     "border-radius:15px;\n"
                                     "background-color: rgb(212, 211, 197);\n"
                                     "color: rgb(25, 25, 25);\n"
                                     "\n"
                                     "font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "QPushButton:pressed{ \n"
                                     "    border-radius:5px;\n"
                                     "    background-color: rgb(197, 220, 227);\n"
                                     "    color: rgb(25, 25, 25);}")
        self.axis3_inc.setObjectName("axis3_inc")
        self.gridLayout_4.addWidget(self.axis3_inc, 4, 0, 1, 1)
        self.axis3_lbl = QtWidgets.QLabel(self.centralwidget)
        self.axis3_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "color: rgb(39, 68, 114);")
        self.axis3_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.axis3_lbl.setObjectName("axis3_lbl")
        self.gridLayout_4.addWidget(self.axis3_lbl, 4, 2, 1, 1)
        self.axis3_val = QtWidgets.QLabel(self.centralwidget)
        self.axis3_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.axis3_val.setAlignment(QtCore.Qt.AlignCenter)
        self.axis3_val.setObjectName("axis3_val")
        self.gridLayout_4.addWidget(self.axis3_val, 4, 3, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout_4.setColumnStretch(2, 2)
        self.gridLayout_4.setColumnStretch(3, 1)
        self.gridLayout_4.setColumnStretch(4, 1)
        self.gridLayout_4.setColumnStretch(5, 2)
        self.VL2.addLayout(self.gridLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.VL2.addItem(spacerItem1)
        self.HL1.addLayout(self.VL2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.HL1.addWidget(self.line)
        spacerItem2 = QtWidgets.QSpacerItem(
            10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HL1.addItem(spacerItem2)
        self.VL3 = QtWidgets.QVBoxLayout()
        self.VL3.setContentsMargins(5, -1, 5, -1)
        self.VL3.setObjectName("VL3")
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.VL3.addItem(spacerItem3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(5, -1, 5, -1)
        self.gridLayout_2.setVerticalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cam_val = QtWidgets.QLabel(self.centralwidget)
        self.cam_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                   "\n"
                                   "color: rgb(18, 18, 18);")
        self.cam_val.setAlignment(QtCore.Qt.AlignCenter)
        self.cam_val.setObjectName("cam_val")
        self.gridLayout_2.addWidget(self.cam_val, 1, 1, 1, 1)
        self.servo_val = QtWidgets.QLabel(self.centralwidget)
        self.servo_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                     "\n"
                                     "color: rgb(18, 18, 18);\n"
                                     "")
        self.servo_val.setAlignment(QtCore.Qt.AlignCenter)
        self.servo_val.setObjectName("servo_val")
        self.gridLayout_2.addWidget(self.servo_val, 0, 1, 1, 1)
        self.driver_lbl = QtWidgets.QLabel(self.centralwidget)
        self.driver_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                      "color: rgb(39, 68, 114);")
        self.driver_lbl.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.driver_lbl.setObjectName("driver_lbl")
        self.gridLayout_2.addWidget(self.driver_lbl, 2, 0, 1, 1)
        self.servo_lbl = QtWidgets.QLabel(self.centralwidget)
        self.servo_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                     "\n"
                                     "color: rgb(39, 68, 114);")
        self.servo_lbl.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.servo_lbl.setObjectName("servo_lbl")
        self.gridLayout_2.addWidget(self.servo_lbl, 0, 0, 1, 1)
        self.cam_lbl = QtWidgets.QLabel(self.centralwidget)
        self.cam_lbl.setStyleSheet("font: 12pt \"Arial\";\n"
                                   "\n"
                                   "color: rgb(39, 68, 114);")
        self.cam_lbl.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.cam_lbl.setObjectName("cam_lbl")
        self.gridLayout_2.addWidget(self.cam_lbl, 1, 0, 1, 1)
        self.driver_val = QtWidgets.QLabel(self.centralwidget)
        self.driver_val.setStyleSheet("font: 87 12pt \"Arial Black\";\n"
                                      "\n"
                                      "color: rgb(18, 18, 18);")
        self.driver_val.setAlignment(QtCore.Qt.AlignCenter)
        self.driver_val.setObjectName("driver_val")
        self.gridLayout_2.addWidget(self.driver_val, 2, 1, 1, 1)
        self.VL3.addLayout(self.gridLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(
            80, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.VL3.addItem(spacerItem4)
        self.VL3.setStretch(1, 1)
        self.HL1.addLayout(self.VL3)
        self.HL1.setStretch(0, 1)
        self.HL1.setStretch(3, 1)
        self.VL1.addLayout(self.HL1)
        self.verticalLayout.addLayout(self.VL1)
        DevWindow.setCentralWidget(self.centralwidget)

        servo_labels[0] = self.axis2_val
        servo_labels[1] = self.axis2_val2
        servo_labels[2] = self.axis1_val
        servo_labels[3] = self.axis3_val
        servo_labels[4] = self.axis4_val
        servo_labels[5] = self.axis5_val
        servo_labels[6] = self.axis6_val

        self.retranslateUi(DevWindow)
        QtCore.QMetaObject.connectSlotsByName(DevWindow)

    def retranslateUi(self, DevWindow):
        _translate = QtCore.QCoreApplication.translate
        DevWindow.setWindowTitle(_translate("DevWindow", "DevWindow"))
        self.back_btn.setText(_translate("DevWindow", "<<<BACK"))
        self.axis1_val.setText(_translate("DevWindow", "90"))
        self.axis4_dec.setText(_translate("DevWindow", "-"))
        self.axis2_test.setText(_translate("DevWindow", "TEST"))
        self.axis2_val2.setText(_translate("DevWindow", "90"))
        self.axis5_lbl.setText(_translate("DevWindow", "Axis5"))
        self.axis2_dec.setText(_translate("DevWindow", "-"))
        self.axis2_val.setText(_translate("DevWindow", "90"))
        self.axis2_inc.setText(_translate("DevWindow", "+"))
        self.axis4_val.setText(_translate("DevWindow", "90"))
        self.axis4_inc.setText(_translate("DevWindow", "+"))
        self.axis1_inc.setText(_translate("DevWindow", "+"))
        self.axis5_test.setText(_translate("DevWindow", "TEST"))
        self.axis1_test.setText(_translate("DevWindow", "TEST"))
        self.axis2_lbl.setText(_translate("DevWindow", "Axis2"))
        self.axis4_lbl.setText(_translate("DevWindow", "Axis4"))
        self.axis5_inc.setText(_translate("DevWindow", "+"))
        self.axis6_test.setText(_translate("DevWindow", "TEST"))
        self.axis3_test.setText(_translate("DevWindow", "TEST"))
        self.axis1_lbl.setText(_translate("DevWindow", "Axis1"))
        self.axis5_val.setText(_translate("DevWindow", "140"))
        self.axis6_inc.setText(_translate("DevWindow", "+"))
        self.axis3_dec.setText(_translate("DevWindow", "-"))
        self.axis6_val.setText(_translate("DevWindow", "0"))
        self.axis5_dec.setText(_translate("DevWindow", "-"))
        self.axis4_test.setText(_translate("DevWindow", "TEST"))
        self.axis6_dec.setText(_translate("DevWindow", "-"))
        self.axis6_lbl.setText(_translate("DevWindow", "Axis6"))
        self.axis1_dec.setText(_translate("DevWindow", "-"))
        self.axis3_inc.setText(_translate("DevWindow", "+"))
        self.axis3_lbl.setText(_translate("DevWindow", "Axis3"))
        self.axis3_val.setText(_translate("DevWindow", "30"))
        self.servo_val.setText(_translate("DevWindow", ""))
        self.servo_lbl.setText(_translate("DevWindow", "SERVO MOTOR VOLTAGE "))
        self.cam_lbl.setText(_translate("DevWindow", "CAMERA"))
        self.cam_val.setText(_translate("DevWindow", "-"))
        self.driver_lbl.setText(_translate("DevWindow", "MOTOR DRIVER"))
        self.driver_val.setText(_translate("DevWindow", ""))


    def ValuesUpdateSlot(self, vol1,driver_mode, cam_mode):
        self.servo_val.setText(vol1)
        self.driver_val.setText(driver_mode)
        self.cam_val.setText(cam_mode)             

    def StartUpdate(self):
        self.DataWorker.start()
        self.DataWorker.ValuesUpdate.connect(self.ValuesUpdateSlot)
        self.MotorWorker.start()
        self.MotorWorker.ServoUpdate.connect(self.update_servo_angle)
   
        
    def CancelFeed(self):
        self.DataWorker.stop()
        
      #Function to update the angle of a servo
    def update_servo_angle(self, servo_number):
        servo_labels[servo_number].setText(f"{servo_angles[servo_number]}°")
       
           
   
class ControlMotor(QThread):
    #Signal to update value of servo
    ServoUpdate=pyqtSignal(int,int)
   

    #Function to control servo motor         
    def set_servo_angle(self,channel, angle):
            try:
                last_angle = servo_angles[channel]
                step = 1 if angle > last_angle else - 1
                for i in np.arange(last_angle, angle, step):
                    pwm.set_pwm(channel, 0, int(((i / 180) * (servo_max - servo_min)) + servo_min))
                    time.sleep(0.01 / servo_speed)
                pwm.set_pwm(channel, 0, int(((angle / 180) * (servo_max - servo_min)) + servo_min))
                servo_angles[channel] = angle
                self.ServoUpdate.emit(channel, angle)
                
            except Exception as E:
                print("Error", E)

    #Starting of servo motor position
    def start_arm_position():
            set_servo_angle(0, 90)
            set_servo_angle(1, 90)
            set_servo_angle(2, 90)
            set_servo_angle(3, 25)
            set_servo_angle(4, 90)
            set_servo_angle(5, 140)
            set_servo_angle(6, 0)
   
    """"
     Function to increase the Axis2 or "SHOULDER" (channel 0 & 1) angle by 1 degree 
    """
    def increase_servo0and1_angle(self):
      
        newAngle0 = servo_angles[0] + servo_speed
        print(newAngle0)
        if newAngle0 <= 110:
            self.set_servo_angle(0, newAngle0)
            servo_angles[0] = newAngle0
            
        newAngle1 = servo_angles[1] - servo_speed
        if newAngle1 >= 70:
            self.set_servo_angle(1, newAngle1)
            servo_angles[1] = newAngle1

    """
    'Function to decrease the Axis2 or "SHOULDER" (channel 0 & 1) angle by 1 degree
    """
    def decrease_servo0and1_angle(self):
        newAngle1 = servo_angles[1] + servo_speed
        if newAngle1 <= 110:
            self.set_servo_angle(1, newAngle1)
            servo_angles[1] = newAngle1
        newAngle0 = servo_angles[0] - servo_speed
        if newAngle0 >=70:
            self.set_servo_angle(0, newAngle0)
            servo_angles[0] = newAngle0      
   
      
    """
    Function to increase the Axis1 or "BASE" (channel 2) base by 1 degree
    """
    def increase_servo2_base_angle(self):
        new_angle_base = servo_angles[2] + servo_speed
        if new_angle_base <= 180:
            self.set_servo_angle(2, new_angle_base)
            servo_angles[2] = new_angle_base
            
    """
    Function to decrease the Axis1 or "BASE" (channel 2) base by 1 degree
    """
    def decrease_servo2_base_angle(self):
        new_angle_base = servo_angles[2] - servo_speed
        if new_angle_base >= 0:
            self.set_servo_angle(2, new_angle_base)
            servo_angles[2] = new_angle_base
    
    """
    Function to increase the Axis3 or"ELBOW" (channel 3) angle by 1 degree
    """
    def increase_servo3_angle(self):
        new_angle = servo_angles[3] + servo_speed
        if new_angle <= 30:
            self.set_servo_angle(3, new_angle)
            servo_angles[3] = new_angle
    """
    Function to decrease the Axis3 "ELBOW" (channel 3) angle by 1 degree
    """
    def decrease_servo3_angle(self):
        new_angle = servo_angles[3] - servo_speed
        if new_angle >= 0:
            self.set_servo_angle(3, new_angle)
            servo_angles[3] = new_angle
    
    """
    Function to incerase the Axis4 or "WRIST"(channel 4) angle by 1 degree
    """
    def increase_servo4_angle(self):
        new_angle = servo_angles[4] + servo_speed
        if new_angle <= 110:
            self.set_servo_angle(4, new_angle)
            servo_angles[4] = new_angle

    
    """
    Function to decrease the Axis4 or "WRIST" (channel 4) angle by 1 degree
    """
    def decrease_servo4_angle(self):
        new_angle = servo_angles[4] - servo_speed
        if new_angle >= 70:
            self.set_servo_angle(4, new_angle)
            servo_angles[4] = new_angle
    """
    Function to increase the servo "5TH AXIS" (channel 5) angle by 1 degree
    """
    def increase_servo5_angle(self):
        new_angle = servo_angles[5] + servo_speed
        if new_angle <= 180:
            self.set_servo_angle(5, new_angle)
            servo_angles[5] = new_angle
    """
    Function to decrease the servo "5TH AXIS" (channel 5) angle by 1 degree
    """
    def decrease_servo5_angle(self):
        new_angle = servo_angles[5] - servo_speed
        if new_angle >= 90:
            self.set_servo_angle(5, new_angle)
            servo_angles[5] = new_angle
    
    """
    Function to increase the servo "6TH AXIS" (channel 6) angle by 1 degree
    """
    def increase_servo6_angle(self):
        new_angle = servo_angles[6] + servo_speed
        if new_angle <= 100:
            self.set_servo_angle(6, new_angle)
            servo_angles[6] = new_angle
    """
    Function to decrease the servo 6TH AXIS (channel 6) angle by 1 degree
    """
    def decrease_servo6_angle(self):
        new_angle = servo_angles[6] - servo_speed
        if new_angle >= 0:
            self.set_servo_angle(6, new_angle)
            servo_angles[6] = new_angle

    ######################################
    ###           FUNCTIONS            ###
    ######################################
    ######################
    ###      BASE      ###
    ######################
    def loopBase(self):
        dev_ui = QtWidgets.QMainWindow()
        for angle in range(45, 135, 1):
            self.set_servo_angle(2, angle)
            if angle == 45:
                time.sleep(3)
            else:
                pot_val_inc_10 = pot_channel[0] + 25
                pot_val_dec_10 = pot_channel[0] - 25

                if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                    print("Servo is ok.")
                else:
                    QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 2 is not working properly. POT {pot_channel[0]}, {pot_val_dec_10} and {pot_val_inc_10}")
            time.sleep(0.2)

        # Loop from 135 degrees to 45 degrees
        for angle in range(135, 45, -1):
            self.set_servo_angle(2, angle)
            pot_val_inc_10 = pot_channel[0] + 25
            pot_val_dec_10 = pot_channel[0] - 25

            if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                print("Servo is ok.")
            else:
                QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 2 is not working properly. POT {pot_channel[0]}, {pot_val_dec_10} and {pot_val_inc_10}")
            time.sleep(0.2)
        self.set_servo_angle(2, 90)
   
    ######################
    ###   SHOULDER     ###
    ######################
    def loopShoulder(self):
        dev_ui = QtWidgets.QMainWindow()
        self.set_servo_angle(0, 70)
        self.set_servo_angle(1, 110)
        StartLoop_0 = 70
        StartLoop_1 = 110
        
        for angle in range(0, 40, 1):
            newAngleLoop0 = StartLoop_0 + 1
            if newAngleLoop0 <= 110:
                self.set_servo_angle(0, newAngleLoop0)
                if newAngleLoop0 == 71:
                 time.sleep(3)
                else:
                    pot_val_inc_10 = pot_channel[1] + 15
                    pot_val_dec_10 = pot_channel[1] - 15

                    if newAngleLoop0 >= pot_val_dec_10 and newAngleLoop0 <= pot_val_inc_10:
                        print("Servo is ok.")
                    else:
                        QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 0 or 1 is not working properly.")
                servo_angles[0] = newAngleLoop0
                StartLoop_0 = newAngleLoop0
            newAngleLoop1 = StartLoop_1 - 1
            if newAngleLoop1 >= 70:
                self.set_servo_angle(1, newAngleLoop1)
                servo_angles[1] = newAngleLoop1
                StartLoop_1 = newAngleLoop1
            time.sleep(0.2)
        
        for angle in range(0, 40, 1):
            newAngleLoop0 = StartLoop_0 - 1
            if newAngleLoop0 >= 70:
                self.set_servo_angle(0, newAngleLoop0)
                if newAngleLoop0 == 109:
                 time.sleep(3)
                else:
                    pot_val_inc_10 = pot_channel[1] + 15
                    pot_val_dec_10 = pot_channel[1] - 15

                    if newAngleLoop0 >= pot_val_dec_10 and newAngleLoop0 <= pot_val_inc_10:
                        print("Servo is ok.")
                    else:
                        QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 0 or 1 is not working properly.")
                servo_angles[0] = newAngleLoop0
                StartLoop_0 = newAngleLoop0
            newAngleLoop1 = StartLoop_1 + 1
            if newAngleLoop1 <= 110:
                self.set_servo_angle(1, newAngleLoop1)
                servo_angles[1] = newAngleLoop1
                StartLoop_1 = newAngleLoop1
            time.sleep(0.2)
        self.set_servo_angle(0, 90)
        self.set_servo_angle(1, 90)


    ######################
    ###     ELBOW      ###
    ######################
    def loopElbow(self):
        dev_ui = QtWidgets.QMainWindow()
        for angle in range(30, 0, -2):
            self.set_servo_angle(3, angle)
            if angle == 30:
                 time.sleep(3)
            else:
                pot_val_inc_10 = pot_channel[2] + 15
                pot_val_dec_10 = pot_channel[2] - 15

                if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                    print("Servo is ok.")
                else:
                    QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 3 is not working properly.")
                time.sleep(0.2)

        # Loop from 180 degrees to 0 degrees
        for angle in range(1, 30, 2):
            self.set_servo_angle(3, angle)
            pot_val_inc_10 = pot_channel[2] + 15
            pot_val_dec_10 = pot_channel[2] - 15

            if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                print("Servo is ok.")
            else:
                QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 3 is not working properly.")
            time.sleep(0.2)
        self.set_servo_angle(3, 25)
    ######################
    ###     WRIST      ###
    ######################

    def loopWrist(self):
        current_value_4 = None
        count_4=0
        dev_ui = QtWidgets.QMainWindow()
        for angle in range(70, 110, 1):
            self.set_servo_angle(4, angle)
            if angle == 70:
                 time.sleep(3)
            else:
                pot_val_inc_10 = pot_channel[3] + 15
                pot_val_dec_10 = pot_channel[3] - 15

                if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                    print("Servo is ok.")
                else:
                    QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 4 is not working properly.")
                time.sleep(0.2)

        # Loop from 110 degrees to 70 degrees
        for angle in range(110, 70, -1):
            self.set_servo_angle(4, angle)
            pot_val_inc_10 = pot_channel[3] + 15
            pot_val_dec_10 = pot_channel[3] - 15

            if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                print("Servo is ok.")
            else:
                QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 4 is not working properly.")
            time.sleep(0.2)
        self.set_servo_angle(4, 90)

    ######################
    ###     FIFTH      ###
    ######################
    def loopFifth(self):
        current_value_5 = None
        count_5=0
        dev_ui = QtWidgets.QMainWindow()
        for angle in range(90, 180, 1):
            self.set_servo_angle(5, angle)
            if angle == 90:
                 time.sleep(3)
            else:
                pot_val_inc_10 = pot_channel[4] + 15
                pot_val_dec_10 = pot_channel[4] - 15

                if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                    print("Servo is ok.")
                else:
                    QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 5 is not working properly.")
                time.sleep(0.2)

        # Loop from 180 degrees to 0 degrees
        for angle in range(180, 90, -1):
            self.set_servo_angle(5, angle)
            pot_val_inc_10 = pot_channel[4] + 15
            pot_val_dec_10 = pot_channel[4] - 15

            if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                print("Servo is ok.")
            else:
                QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 5 is not working properly.")
            time.sleep(0.2)
        self.set_servo_angle(5, 140)
            

    ######################
    ###     SIXTH      ###
    ######################
    def loopSixth(self):
        current_value_6 = None
        count_6=0
        dev_ui = QtWidgets.QMainWindow()
        for angle in range(0, 90, 1):
            self.set_servo_angle(6, angle)
            if angle == 0:
                time.sleep(3)
            else:
                pot_val_inc_10 = pot_channel[5] + 15
                pot_val_dec_10 = pot_channel[5] - 15

                if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                    print("Servo is ok.")
                else:
                    QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 6 is not working properly.")
                time.sleep(0.2)

        for angle in range(89, 0, -1):
            self.set_servo_angle(6, angle)

            pot_val_inc_10 = pot_channel[5] + 15
            pot_val_dec_10 = pot_channel[5] - 15

            if angle >= pot_val_dec_10 and angle <= pot_val_inc_10:
                print("Servo is ok.")
            else:
                QMessageBox.warning(dev_ui, 'Error', f"Servo at Channel 6 is not working properly.")
            time.sleep(0.2)
        self.set_servo_angle(6, 0)
          
    
                       


class GetData(QThread):
    #Signal to update the values of voltage,camera, and motor driver 
    ValuesUpdate = pyqtSignal(str,str,str)
    
    def stop(self):
        self.ThreadActive = False
        self.quit()
        
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
             self.get_values()
             
    def read_sensors(self):
        global pot_channel,Potentiometer1,Potentiometer2,Potentiometer3,Potentiometer4,Potentiometer5,Potentiometer6
        
     
        try:
                # read the sensor values from the Arduino
                data = ser.readline().decode().rstrip().split(delimeter)
                
                voltage1 = float(data[0]) if data[0] else None
                

                Potentiometer1 = round(float(data[1])) if data[1] else None
                Potentiometer2 = round(float(data[2])) if data[2] else None
                Potentiometer3 = round(float(data[3])) if data[3] else None
                Potentiometer4 = round(float(data[4])) if data[4] else None
                Potentiometer5 = round(float(data[5])) if data[5] else None
                Potentiometer6 = round(float(data[6])) if data[6] else None
                
                pot_channel[0]=Potentiometer1
                pot_channel[1]=Potentiometer2
                pot_channel[2]=Potentiometer3
                pot_channel[3]=Potentiometer4
                pot_channel[4]=Potentiometer5
                pot_channel[5]=Potentiometer6
                
                # return a dictionary with the sensor and device values
                return {
                    'voltage1': voltage1,
                    'Potentiometer1': Potentiometer1,
                    'Potentiometer2': Potentiometer2,
                    'Potentiometer3': Potentiometer3,
                    'Potentiometer4': Potentiometer4,
                    'Potentiometer5': Potentiometer5,
                    'Potentiometer6': Potentiometer6
                }
        except Exception as E:
                print(E)

    def get_values(self):
        global driver
        while True:
            check_camera = subprocess.check_output('lsusb')
            if b'Intel Myriad VPU' in check_camera:
                cam_val="ACTIVE"
            else:
                cam_val="INACTIVE"
            if driver:
                driver_mode="ACTIVE"
            else:
                driver_mode="INACTIVE" 
				
		    # read the sensor and device values from the Arduino
            data = self.read_sensors()
            if data is not None:
                v1 = str(data['voltage1'])
                
                print(f"Voltage1: {data['voltage1']}V,"
		              f"Pot1: {data['Potentiometer1']}, Pot2: {data['Potentiometer2']}, "
		              f"Pot3: {data['Potentiometer3']}, Pot4: {data['Potentiometer4']}, "
		              f"Pot5: {data['Potentiometer5']}, Pot6: {data['Potentiometer6']}")
            else:
                v1 = '-'  # or some other default value
                
		
		    # print the sensor and device values
            self.ValuesUpdate.emit(v1,driver_mode,cam_val)
            time.sleep(0.1)  # wait 0.1 second before repeating
		
            
def DisplayNow():
        dev_ui.show()
        dev_ui.StartUpdate()



if __name__ == "__main__":
    import sys
    import threading
    app = QtWidgets.QApplication(sys.argv)
    dev_ui = Ui_DevWindow()
    DisplayNow()

    sys.exit(app.exec_())

