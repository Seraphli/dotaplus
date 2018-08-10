import sys
import warnings
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


from gui.select import Ui_Form

warnings.filterwarnings("ignore")

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
        path = os.path.abspath('./miniheroes')
        # self.elder_titan_Btn.setPixmap(QPixmap(path+'/ancient_apparition.png'))
        # self.undying_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/undying.png'))
        # self.abaddon_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/abaddon.png'))
        # self.shredder_Btn.setPixmap(QPixmap('/Users/houxiao/workspace/python/dotaplus/gui/res/miniheroes/shredder.png'))
        # print(self.omniknight_Btn.text())

        layouts = [self.strLayout_1, self.strLayout_2, self.agiLayout_1, self.agiLayout_2, self.intLayout_1, self.intLayout_2]
        for layout in layouts:
            for i in range(layout.count()):
                btn = layout.itemAt(i).widget()
                if type(btn)==QLabel:
                    btn.setPixmap(QPixmap(path+f'/{btn.text()}.png'))
                    print(btn.objectName()[:-4])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = selectWindow()
    sys.exit(app.exec())