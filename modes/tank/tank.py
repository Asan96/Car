import sys
import subprocess
import queue

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIcon, QPalette
from ui.tankWindow import Ui_tankWindow
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from ui.connectDialog import Ui_dialog_connect
from modes.tank.mqtt import mqtt_send, connect_mqtt
from modes.camera import ImgServer, open_camera_client, close_camera_client
import threading
from datetime import datetime
from __init__ import camera_background_path, pyfile_path
from interface import _write, _read
from modes.tank.code import Code

"""
主窗口
"""

isKeyboard = False
gapWord = ":"
q = queue.Queue()

class TankWindow(QtWidgets.QMainWindow, Ui_tankWindow):
    def __init__(self):
        super(TankWindow, self).__init__()
        self.setupUi(self)
        self.avoid.clicked.connect(self.avoid_follow)
        self.travel.clicked.connect(self.avoid_follow)
        self.follow.clicked.connect(self.avoid_follow)
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

        self.background = QtGui.QPixmap(camera_background_path)
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
        self.loginWindow = DialogConnect()
        self.actionLogin.triggered.connect(self.loginDialog)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # 文字图片水平排列
        root = QFileInfo(__file__).absolutePath()
        self.actionLogin.setIcon(QIcon(root+'/icon/connect.ico'))
        self.actionChange.setIcon(QIcon(root+'/icon/change.ico'))
        self.actionInfo.setIcon(QIcon(root+'/icon/info.ico'))
        self.loginWindow.btn_connect.clicked.connect(self.login_status)
        self._lyt = QtWidgets.QVBoxLayout()
        self._code = Code()
        self._lyt.addWidget(self._code)
        self.CodeWidget.setLayout(self._lyt)

        self.btnRunLocal.clicked.connect(self.run_local)
        self.btnRunStop.clicked.connect(self.run_stop)
        self.btnRunDevice.clicked.connect(self.run_device)
        self.btnCodeImport.clicked.connect(self.code_import)
        self.btnCodeSave.clicked.connect(self.code_save)

        self.tabMenuWidget.setStyleSheet("QTabWidget::pane{border: 1px;background-color:white;position: absolute;}"
                                         "QTabWidget::tab-bar{subcontrol-position:left;alignment: center;}"
                                         "QTabBar::tab{min-width:249px;min-height:35px;"
                                         "font-weight:bold;font-family:'微软雅黑'}"
                                         "QTabBar::tab:selected {color: white;background-color:#5FB878;border-right:1px solid gray}"
                                         "QTabBar::tab:!selected{color: white;background-color:#393D49;border-right:1px solid gray}"
                                         "QTabBar::tab:hover{color: #FF6633;}")
        self.tabMenuWidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)
        self.tabMenuWidget.setPalette(palette)
        # self.follow.setStyleSheet("QCheckBox::indicator{width: 50px;height: 30px;}"
        #                           "QCheckBox::indicator::unchecked {image:url(:/tank/icon/checkbox_checked.png);}"
        #                           "QCheckBox::indicator::checked { image:url(:/tank/icon/checkbox_unchecked.png);}")

    '''代码编辑器'''
    # 本地运行 需安装 Python3
    def run_local(self):
        global q
        _write(pyfile_path, self._code.text())
        try:
            sub = subprocess.Popen("python " + pyfile_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            try:
                sub = subprocess.Popen("python3 " + pyfile_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                self.CodeConsoleText.setText('未检测到Python运行环境！'+str(e))
                return
        q.put(sub)
        sub.wait()
        output = sub.stdout.read().decode(encoding='utf-8') if sub.stdout else ''
        error = sub.stderr.read().decode(encoding='utf-8') if sub.stderr else ''
        console = output + error
        self.CodeConsoleText.setText(console)

    # 终止运行
    def run_stop(self):
        global q
        while not q.empty():
            sub = q.get()
            sub.kill()

    # 设备运行
    def run_device(self):
        cmd = 'code'+gapWord+self._code.text()
        mqtt_send(cmd)

    # 导入代码文件
    def code_import(self):
        file_path = QFileDialog.getOpenFileName(self, caption="打开Python文件", filter="Python files(*.py)")[0]
        if file_path:
            content = _read(file_path)
            self._code.setText(content)

    # 保存代码文件
    def code_save(self):
        file_path = QFileDialog.getSaveFileName(self, "保存文件", "C:/Users/Administrator/Desktop","Python files(*.py)")[0]
        if file_path:
            _write(file_path, self._code.text())



    # 小车连接
    def login_status(self):
        mac_id = self.loginWindow.input_macId.text()
        if mac_id[4:6] == '03' and mac_id.isdigit():
            result = connect_mqtt(mac_id)
            if result['ret'] is True:
                self.actionStatus.setText(self.loginWindow.input_macId.text())
                QMessageBox.information(self, "连接状态", "连接成功！", QMessageBox.Yes, QMessageBox.Yes)
                self.loginWindow.close()
            else:
                QMessageBox.information(self, "连接状态", result['msg'], QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "警告", "请输入格式正确的设备id！", QMessageBox.Yes, QMessageBox.Yes)



    def loginDialog(self):
        self.loginWindow.show()

    # mqtt 报错提示

    def send(self, msg):
        result = mqtt_send(msg)
        if not result['ret']:
            QMessageBox.warning(self, "警告",result['msg'], QMessageBox.Yes, QMessageBox.Yes)

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
        self.send(msg)

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
        self.send(command)

    # 检测键盘回车按键，函数名字不能改，这是重写键盘事件
    def keyPressEvent(self, event):
        key_dic = {65: 'car_right', 87: 'car_forward', 68: 'car_left', 83: 'car_backward', 69: 'car_stop',
                   81: 'car_rotate'}
        # 这里event.key（）显示的是按键的编码
        if isKeyboard and event.key() in key_dic.keys():
            self.send(key_dic[event.key()])

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
        self.send(command)
        self.input_composite_text.setText('')
        self.input_send_text.setText('')

    def video(self):
        str_type = self.sender().objectName().split('_')[-1]
        print(str_type)
        if str_type == 'close':
            close_camera_client()
            self.video_pannel.setPixmap(self.background)
            return
        cameraThread = threading.Thread(target=self.thread_camera, args=(self.video_pannel, str_type))
        cameraThread.start()


"""
    连接小车
"""


class DialogConnect(QtWidgets.QDialog, Ui_dialog_connect):
    def __init__(self):
        super(DialogConnect, self).__init__()
        self.setupUi(self)
        self.btn_clear.clicked.connect(self.clear_mac_input)

    # 连接输入框清空
    def clear_mac_input(self):
        self.input_macId.setText('')


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = TankWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
