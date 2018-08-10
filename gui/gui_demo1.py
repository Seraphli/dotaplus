import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from gui.demo1 import Ui_MainWindow
# import ban_pick


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mywindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            Qt.WindowCloseButtonHint |  # 使能关闭按钮
                            Qt.WindowStaysOnTopHint)  # 总是最前显示

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mywindow()
    sys.exit(app.exec())