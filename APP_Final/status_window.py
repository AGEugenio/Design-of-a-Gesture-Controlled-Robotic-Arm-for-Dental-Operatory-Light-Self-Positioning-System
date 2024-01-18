# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'status_win.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from img import status_icons_rc

class Ui_Status(object):
    def setupUi(self, Status):
        Status.setObjectName("Status")
        Status.resize(800, 480)
        Status.setStyleSheet("#Status{\n"
                                "background-color: rgb(197, 220, 227);}\n"
                                "\n"
                                "#title_label{\n"
                                "background-color: rgb(197, 220, 227);}\n"
                                "\n"
                                "#SPS_lbl{\n"
                                "background-color: rgb(114, 39, 39);\n"
                                "color: rgb(255, 255, 255);\n"
                                "font: 15pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "#light_lbl{\n"
                                "background-color: rgb(191, 168, 45);\n"
                                "color: rgb(255, 255, 255);\n"
                                "font: 15pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "#battery_lbl{\n"
                                "background-color: rgb(38, 112, 50);\n"
                                "color: rgb(255, 255, 255);\n"
                                "font: 15pt \"MS Shell Dlg 2\";}"
                                "#light_icon{\n"
                                "font: 15pt \"MS Shell Dlg 2\";\n"
                                "font-weight: bold;\n"
                                "background-color: rgb(255, 255, 255);\n"
                                "border-bottom-right-radius: 25px;\n"
                                "border-bottom-left-radius: 25px;\n"
                                "}"
                                "#sps_icon{\n"
                                "font: 15pt \"Arial\";\n"
                                "font-weight: bold;\n"
                                "background-color: rgb(255, 255, 255);\n"
                                "border-bottom-right-radius: 25px;\n"
                                "border-bottom-left-radius: 25px;\n"
                                 "}")
        Status.setDocumentMode(False)
        Status.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(Status)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.statusVLayout = QtWidgets.QVBoxLayout()
        self.statusVLayout.setSpacing(0)
        self.statusVLayout.setObjectName("statusVLayout")
        self.statusframe = QtWidgets.QFrame(self.centralwidget)
        self.statusframe.setStyleSheet("\n"
"background-color: rgb(0, 0, 0);")
        self.statusframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.statusframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusframe.setObjectName("statusframe")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.statusframe)
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.back_btn = QtWidgets.QPushButton(self.statusframe)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.back_btn.setFont(font)
        self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.back_btn.setStyleSheet("\n"
"\n"
"QPushButton{\n"
"    font: 9pt \"Arial\";\n"
"    color: rgb(255, 255, 255);}\n"
"QPushButton:hover{ \n"
"    color: rgb(197, 220, 227);\n"
"}\n"
"QPushButton:pressed{ \n"
"    color: rgb(197, 220, 227);\n"
"    }\n"
"")
        self.back_btn.setFlat(True)
        self.back_btn.setObjectName("back_btn")
        self.horizontalLayout_2.addWidget(self.back_btn)
        spacerItem = QtWidgets.QSpacerItem(703, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.statusVLayout.addWidget(self.statusframe)
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(9)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("font: 75 30pt \"Arial\";\n"
"color: rgb(39, 68, 114);")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.statusVLayout.addWidget(self.title_label)
        self.statusGrid = QtWidgets.QGridLayout()
        self.statusGrid.setContentsMargins(-1, -1, -1, 1)
        self.statusGrid.setHorizontalSpacing(10)
        self.statusGrid.setVerticalSpacing(0)
        self.statusGrid.setObjectName("statusGrid")
        self.SPS_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SPS_lbl.sizePolicy().hasHeightForWidth())
        self.SPS_lbl.setSizePolicy(sizePolicy)
        self.SPS_lbl.setStyleSheet("border-bottom-right-radius: 5px;\n"
"font: 15pt \"Arial\";\n"
"border-bottom-left-radius: 5px;")
        self.SPS_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.SPS_lbl.setWordWrap(True)
        self.SPS_lbl.setObjectName("SPS_lbl")
        self.statusGrid.addWidget(self.SPS_lbl, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.statusGrid.addItem(spacerItem1, 1, 4, 1, 1)
        self.battery_icon = QtWidgets.QLabel(self.centralwidget)
        self.battery_icon.setAcceptDrops(False)
        self.battery_icon.setStyleSheet("image: url(:/img/BATTERY.png);\n"
"font: 15pt \"Arial\";;\n"
"font-weight: bold;\n"
"background-color: rgb(255, 255, 255);\n"
"border-bottom-right-radius: 25px;\n"
"border-bottom-left-radius: 25px;\n"
"")
        self.battery_icon.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.battery_icon.setFrameShadow(QtWidgets.QFrame.Plain)
        self.battery_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.battery_icon.setObjectName("battery_icon")
        self.statusGrid.addWidget(self.battery_icon, 1, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.statusGrid.addItem(spacerItem2, 1, 0, 1, 1)
        self.light_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.light_lbl.sizePolicy().hasHeightForWidth())
        self.light_lbl.setSizePolicy(sizePolicy)
        self.light_lbl.setStyleSheet("border-bottom-right-radius: 5px;\n"
"border-bottom-left-radius: 5px;\n"
"font: 15pt \"Arial\";")
        self.light_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.light_lbl.setObjectName("light_lbl")
        self.statusGrid.addWidget(self.light_lbl, 0, 2, 1, 1)
        self.sps_icon = QtWidgets.QLabel(self.centralwidget)
        self.sps_icon.setStyleSheet("image: url(:/img/ON.png);\n"
)
        self.sps_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.sps_icon.setObjectName("sps_icon")
        self.statusGrid.addWidget(self.sps_icon, 1, 1, 1, 1)
        self.battery_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.battery_lbl.sizePolicy().hasHeightForWidth())
        self.battery_lbl.setSizePolicy(sizePolicy)
        self.battery_lbl.setStyleSheet("border-bottom-right-radius: 5px;\n"
"border-bottom-left-radius: 5px;\n"
"font: 15pt \"Arial\";")
        self.battery_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.battery_lbl.setObjectName("battery_lbl")
        self.statusGrid.addWidget(self.battery_lbl, 0, 3, 1, 1)
        self.light_icon = QtWidgets.QLabel(self.centralwidget)
        self.light_icon.setStyleSheet("image: url(:/img/BRIGHT.png);\n")
        self.light_icon.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.light_icon.setWordWrap(False)
        self.light_icon.setObjectName("light_icon")
        self.statusGrid.addWidget(self.light_icon, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.statusGrid.addItem(spacerItem3, 2, 2, 1, 1)
        self.statusGrid.setColumnStretch(1, 2)
        self.statusGrid.setColumnStretch(2, 2)
        self.statusGrid.setColumnStretch(3, 2)
        self.statusGrid.setRowStretch(0, 1)
        self.statusGrid.setRowStretch(1, 8)
        self.statusVLayout.addLayout(self.statusGrid)
        self.statusVLayout.setStretch(1, 1)
        self.statusVLayout.setStretch(2, 8)
        self.verticalLayout_2.addLayout(self.statusVLayout)
        Status.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Status)
        self.statusbar.setObjectName("statusbar")
        Status.setStatusBar(self.statusbar)

        self.retranslateUi(Status)
        QtCore.QMetaObject.connectSlotsByName(Status)

    def retranslateUi(self, Status):
        _translate = QtCore.QCoreApplication.translate
        Status.setWindowTitle(_translate("Status", "Status"))
        self.back_btn.setText(_translate("Status", "<<< BACK"))
        self.title_label.setText(_translate("Status", "STATUS"))
        self.SPS_lbl.setText(_translate("Status", "Self-Positioning System"))
        self.battery_icon.setText(_translate("Status", "99%"))
        self.light_lbl.setText(_translate("Status", "Light"))
        self.sps_icon.setText(_translate("Status", "ON"))
        self.battery_lbl.setText(_translate("Status", "Battery"))
        self.light_icon.setText(_translate("Status", "BRIGHT"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Status = QtWidgets.QMainWindow()
    ui = Ui_Status()
    ui.setupUi(Status)
    Status.show()
    sys.exit(app.exec_())
