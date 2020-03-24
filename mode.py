from PyQt5 import QtWidgets, QtGui
from ui.login import Ui_modeDialog
from PyQt5.QtGui import QIcon
from modes.tank.tank import TankWindow
from PyQt5.QtWidgets import QMessageBox
from interface import reset_config


# 登录页面选择不同模式
class ModeDialog(QtWidgets.QDialog, Ui_modeDialog):
    def __init__(self):
        super(ModeDialog, self).__init__()
        self.setupUi(self)
        self.option_pc.setIcon(QIcon('static/image/logo_pc.png'))
        self.option_tank.setIcon(QIcon('static/image/logo_tank.png'))
        self.option_mac.setIcon(QIcon('static/image/logo_mac.png'))
        self.btn_close.clicked.connect(self.close)
        self.btn_enter.clicked.connect(self.enter_option)
        self.tankWindow = TankWindow()
        self.tankWindow.actionChange.triggered.connect(self.tankToMode)

    # tank页面回到模式选择页面
    def tankToMode(self):
        self.tankWindow.close()
        self.show()

    # 进入不同的选项
    def enter_option(self):
        reset_config()
        self.close()
        if self.option_tank.isChecked():
            self.tankWindow.show()
        elif self.option_mac.isChecked():
            print(222)
        elif self.option_pc.isChecked():
            print(333)