import sys
from PyQt5 import QtWidgets, QtGui
from ui.tankWindow import Ui_tankWindow
from PyQt5.QtWidgets import QMessageBox
from ui.connectDialog import Ui_dialog_connect
from modes.tank.mqtt import mqtt_send, connect_mqtt
from modes.camera import ImgServer, open_camera_client, close_camera_client
import threading
from datetime import datetime

"""
主窗口
"""

isKeyboard = False
gapWord = ":"


class TankWindow(QtWidgets.QMainWindow, Ui_tankWindow):
    def __init__(self):
        super(TankWindow, self).__init__()
        self.setupUi(self)
        self.avoid.clicked.connect(self.avoid_follow)
        self.travel.clicked.connect(self.avoid_follow)
        self.keyboard_control.clicked.connect(self.keyboard_move)
        self.car_backward.clicked.connect(self.car_move)
        self.car_forward.clicked.connect(self.car_move)
        self.car_left.clicked.connect(self.car_move)
        self.car_right.clicked.connect(self.car_move)
        self.car_rotate.clicked.connect(self.car_move)
        self.car_stop.clicked.connect(self.car_move)
        self.car_cam_down.clicked.connect(self.car_move)
        self.car_cam_up.clicked.connect(self.car_move)
        self.car_cam_left.clicked.connect(self.car_move)
        self.car_cam_right.clicked.connect(self.car_move)

        self.background = QtGui.QPixmap('./static/image/camera_background.jpg')
        self.video_pannel.setPixmap(self.background)
        self.origin_camera.setPixmap(self.background)

        self.camera_switch.clicked.connect(self.control_camera)
        self.voice_chat.clicked.connect(self.voice)
        self.voice_control.clicked.connect(self.voice)
        self.voice_text_composite.clicked.connect(self.voice)
        self.voice_audio_play.clicked.connect(self.voice)
        self.voice_audio_start.clicked.connect(self.voice)
        self.voice_audio_stop.clicked.connect(self.voice)
        self.voice_text_chat.clicked.connect(self.voice)
        self.camera_origin.clicked.connect(self.video)
        self.camera_face.clicked.connect(self.video)
        self.camera_eyes.clicked.connect(self.video)
        self.camera_close.clicked.connect(self.video)

    """
        行动控制界面
    """

    # 避障 跟随
    def avoid_follow(self):
        checkObj = self.sender()
        name = checkObj.objectName()
        msg = name + '_off'
        if checkObj.isChecked():
            msg = name+'_on'
        mqtt_send(msg)

    # 键盘控制
    def keyboard_move(self):
        global isKeyboard
        isKeyboard = False
        if self.keyboard_control.isChecked():
            print('键盘控制开启')
            isKeyboard = True

    # 小车行动控制及摄像头控制
    def car_move(self):
        command = self.sender().objectName()
        mqtt_send(command)

    # 检测键盘回车按键，函数名字不能改，这是重写键盘事件
    def keyPressEvent(self, event):
        key_dic = {65: 'car_right', 87: 'car_forward', 68: 'car_left', 83: 'car_backward', 69: 'car_stop',
                   81: 'car_rotate'}
        # 这里event.key（）显示的是按键的编码
        if isKeyboard and event.key() in key_dic.keys():
            mqtt_send(key_dic[event.key()])

    # 图像传输服务端打开
    def thread_camera(self, pannel=None, type='origin'):
        if not pannel:
            return
        open_camera_client()
        server = ImgServer(type)
        imgObj = server.img_data()
        try:
            img = imgObj.__next__()
        except StopIteration as e:
            return
        while str(img):
            image = QtGui.QImage(img.data, img.shape[1], img.shape[0], 3 * img.shape[1], QtGui.QImage.Format_RGB888)
            pannel.setPixmap(QtGui.QPixmap.fromImage(image))
            try:
                img = imgObj.send(img)
            except StopIteration as e:
                break

    # 控制界面摄像头画面
    def control_camera(self):
        if self.sender().isChecked():
            camThread = threading.Thread(target=self.thread_camera, args=(self.origin_camera, 'origin'))
            camThread.start()
        else:
            close_camera_client()
            self.origin_camera.setPixmap(self.background)

    """
    语音技术界面
    """
    def voice(self):
        command = self.sender().objectName()
        if command == 'voice_text_composite':
            text = self.input_composite_text.text()
            command = command + gapWord + text
            if len(text) >= 200:
                QMessageBox.warning(self, "警告", "合成文字请在200字以内！", QMessageBox.Yes, QMessageBox.Yes)
                self.input_composite_text.setText('')
                return
        elif command == 'voice_text_chat':
            text = self.input_send_text.text()
            self.voice_chat_list.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'    '+text)
            command = command+gapWord+text
            if len(text) >= 50:
                QMessageBox.warning(self, "警告", "文字对话内容请在50字以内！", QMessageBox.Yes, QMessageBox.Yes)
                return
        mqtt_send(command)
        self.input_composite_text.setText('')
        self.input_send_text.setText('')

    def video(self):
        type = self.sender().objectName().split('_')[-1]
        if type == 'close':
            close_camera_client()
            self.video_pannel.setPixmap(self.background)
            return
        cameraThread = threading.Thread(target=self.thread_camera, args=(self.video_pannel, type))
        cameraThread.start()


"""
    连接小车
"""


class DialogConnect(QtWidgets.QDialog, Ui_dialog_connect):
    def __init__(self):
        super(DialogConnect, self).__init__()
        self.setupUi(self)
        self.btn_connect.clicked.connect(self.connect_car)
        self.btn_clear.clicked.connect(self.clear_mac_input)
        self.main = TankWindow()

    # 小车连接
    def connect_car(self):
        mac_id = self.input_macId.text()
        if mac_id[4:6] == '03' and mac_id.isdigit():
            result = connect_mqtt(mac_id)
            if result['ret'] is True:
                QMessageBox.information(self, "连接状态", "连接成功！", QMessageBox.Yes, QMessageBox.Yes)
                self.close()
                self.main.show()
            else:
                QMessageBox.information(self, "连接状态", result['msg'], QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "警告", "请输入格式正确的设备id！", QMessageBox.Yes, QMessageBox.Yes)

    # 连接输入框清空
    def clear_mac_input(self):
        self.input_macId.setText('')


def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog_connect = DialogConnect()
    dialog_connect.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
