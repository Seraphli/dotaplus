import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from gui.select import Ui_Form

import warnings


class selectWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(selectWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            Qt.WindowCloseButtonHint |  # 使能关闭按钮
                            Qt.WindowStaysOnTopHint)  # 总是最前显示

        self.set_btn_icon()

        self.show()

    def set_btn_icon(self):
        self.elder_titan_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/elder_titan.png'))
        self.undying_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/undying.png'))
        self.abaddon_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/abaddon.png'))
        self.shredder_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/shredder.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = selectWindow()
    sys.exit(app.exec())