import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from gui.myLabel import myLabel
from gui.banpick import Ui_MainWindow
from gui.gui_select import selectWindow
# import ban_pick


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mywindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            Qt.WindowCloseButtonHint |  # 使能关闭按钮
                            Qt.WindowStaysOnTopHint)  # 总是最前显示

        self.set_pick_btn()
        self.add_action()
        self.show()

    def set_pick_btn(self):
        layouts = [self.mbpLayout, self.ebpLayout]
        for layout in layouts:
            for i in range(1, 6):
                btn = myLabel()
                btn.setText(str(i))
                btn.setName(str(i))
                btn.setMinimumSize(32, 32)
                btn.setMaximumSize(32, 32)
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                # btn.clicked.connect(sw.show)
                layout.addWidget(btn)

    def add_action(self):
        for i in range(self.ebpLayout.count()):
            self.mbpLayout.itemAt(i).widget().clicked.connect(lambda sw = selectWindow(i): sw.show())
            # self.ebpLayout.itemAt(i).widget().clicked.connect(lambda: self.call_sw(i+5))




# def set_clickable():
#     app = QApplication(sys.argv)
#     ex = mywindow()
#     sw = selectWindow(1)
#     for i in range(ex.ebpLayout.count()):
#         ex.mbpLayout.itemAt(i).widget().clicked.connect(sw.show)
#         ex.ebpLayout.itemAt(i).widget().clicked.connect(sw.show)
#     sys.exit(app.exec())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mywindow()
    sys.exit(app.exec())
