# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tankStructionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_structionWidget(object):
    def setupUi(self, structionWidget):
        structionWidget.setObjectName("structionWidget")
        structionWidget.resize(480, 360)
        structionWidget.setMinimumSize(QtCore.QSize(480, 360))
        structionWidget.setMaximumSize(QtCore.QSize(480, 360))
        structionWidget.setStyleSheet("background-color:white;padding-top:20px;font-family:\'微软雅黑\';")
        self.textBrowser = QtWidgets.QTextBrowser(structionWidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 480, 360))
        self.textBrowser.setMinimumSize(QtCore.QSize(480, 360))
        self.textBrowser.setMaximumSize(QtCore.QSize(480, 360))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.textBrowser.setFont(font)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet("border:0px;background-color:#rgb(245, 247, 237);")
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(structionWidget)
        QtCore.QMetaObject.connectSlotsByName(structionWidget)

    def retranslateUi(self, structionWidget):
        _translate = QtCore.QCoreApplication.translate
        structionWidget.setWindowTitle(_translate("structionWidget", "人工智能履带坦克使用说明"))
        self.textBrowser.setHtml(_translate("structionWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'微软雅黑\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; color:#383838;\">1、使用时需连接履带坦克。打开车上的开关，待树莓派启动后，点击登录输入车身的设备号进行连接，听到已连接提示即连接成功，可进行相应的功能操作。</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:13pt; color:#383838;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; color:#383838;\">2、打开键盘控制后，使用键盘的</span><span style=\" font-size:13pt; color:#ff5500;\">W（前进）、A（左转）、S（后退）、D（右转）、Q（旋转）、E（停止）</span><span style=\" font-size:13pt; color:#383838;\">来控制行动。</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:13pt; color:#383838;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; color:#383838;\">3、物体跟随采用的是摄像头对颜色和物体大小的识别。具体使用时，将一个蓝色的物块</span><span style=\" font-size:13pt; color:#ee4c4f;\">（暂时只支持蓝色，物块不要太小）</span><span style=\" font-size:13pt; color:#383838;\">放到小车前方，注意距离不要太近。物体跟随时需将摄像头相关的画面关闭。</span></p></body></html>"))
