import sys
from PyQt5 import QtWidgets, QtGui
from mode import ModeDialog


def main():
    app = QtWidgets.QApplication(sys.argv)
    mode_dilog = ModeDialog()
    mode_dilog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()