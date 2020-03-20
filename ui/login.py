# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_modeDialog(object):
    def setupUi(self, modeDialog):
        modeDialog.setObjectName("modeDialog")
        modeDialog.resize(600, 400)
        modeDialog.setStyleSheet("background-color:#F0F0F0;")
        self.scrollArea = QtWidgets.QScrollArea(modeDialog)
        self.scrollArea.setGeometry(QtCore.QRect(30, 60, 541, 271))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 539, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.option_mac = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.option_mac.setGeometry(QtCore.QRect(0, 180, 541, 91))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.option_mac.setFont(font)
        self.option_mac.setStyleSheet("QPushButton:hover{background-color:#8bf0ad;} \n"
"QPushButton{background-color:white;border:2px;text-align:left;padding-left:20px;}\n"
"QPushButton::checked{ background:#59de85;border-color: #11505C;}")
        self.option_mac.setIconSize(QtCore.QSize(64, 64))
        self.option_mac.setCheckable(True)
        self.option_mac.setAutoExclusive(True)
        self.option_mac.setObjectName("option_mac")
        self.option_tank = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.option_tank.setGeometry(QtCore.QRect(0, 90, 541, 91))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.option_tank.setFont(font)
        self.option_tank.setStyleSheet("QPushButton:hover{background-color:#8bf0ad;} \n"
"QPushButton{background-color:white;border:2px;text-align:left;padding-left:20px;}\n"
"QPushButton::checked{ background:#59de85;border-color: #11505C;}")
        self.option_tank.setIconSize(QtCore.QSize(64, 64))
        self.option_tank.setCheckable(True)
        self.option_tank.setAutoExclusive(True)
        self.option_tank.setObjectName("option_tank")
        self.option_pc = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.option_pc.setGeometry(QtCore.QRect(0, 0, 541, 91))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.option_pc.setFont(font)
        self.option_pc.setStyleSheet("QPushButton:hover{background-color:#8bf0ad;} \n"
"QPushButton{background-color:white;border:2px;text-align:left;padding-left:20px;}\n"
"QPushButton::checked{ background:#59de85;border-color: #11505C;}")
        self.option_pc.setIconSize(QtCore.QSize(64, 64))
        self.option_pc.setCheckable(True)
        self.option_pc.setAutoExclusive(True)
        self.option_pc.setObjectName("option_pc")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(modeDialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 541, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btn_enter = QtWidgets.QPushButton(modeDialog)
        self.btn_enter.setGeometry(QtCore.QRect(370, 350, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_enter.setFont(font)
        self.btn_enter.setStyleSheet("QPushButton:hover{background-color:#1E9FFF;color:#F8F8F8} \n"
"QPushButton{background-color:#01AAED;border-radius:5px;color:#F2F2F2}")
        self.btn_enter.setObjectName("btn_enter")
        self.btn_close = QtWidgets.QPushButton(modeDialog)
        self.btn_close.setGeometry(QtCore.QRect(490, 350, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_close.setFont(font)
        self.btn_close.setStyleSheet("QPushButton:hover{background-color:#c2c2c2;color:#F2F2F2} \n"
"QPushButton{background-color:#d2d2d2;border-radius:5px;color:grey}")
        self.btn_close.setObjectName("btn_close")

        self.retranslateUi(modeDialog)
        QtCore.QMetaObject.connectSlotsByName(modeDialog)

    def retranslateUi(self, modeDialog):
        _translate = QtCore.QCoreApplication.translate
        modeDialog.setWindowTitle(_translate("modeDialog", "模式"))
        self.option_mac.setText(_translate("modeDialog", "   麦克纳姆\n"
"   麦克纳姆机器人的多角度行动控制、语音技术、视频处理及编码控制等。"))
        self.option_tank.setText(_translate("modeDialog", "   履带坦克\n"
"   履带坦克机器人的行动控制、语音技术、视频处理及编码控制等。"))
        self.option_pc.setText(_translate("modeDialog", "   PC标准版\n"
"   调用本机的声音、视频设备来进行图像处理、机器学习、自然语言处理等。"))
        self.label.setText(_translate("modeDialog", "请根据需要选择不同的模式来进行功能操作。“确定”进入操作界面，“取消”退出程序。"))
        self.btn_enter.setText(_translate("modeDialog", "确定"))
        self.btn_close.setText(_translate("modeDialog", "取消"))
