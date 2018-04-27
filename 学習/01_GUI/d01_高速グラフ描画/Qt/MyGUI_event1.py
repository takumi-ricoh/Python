# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 19:35:01 2017

@author: p000495138
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class EventTest01(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        WiNum = QLCDNumber(self)
        Stool = QSlider(Qt.Horizontal, self)
        BoxLay = QVBoxLayout()
        BoxLay.addWidget(WiNum)
        BoxLay.addWidget(Stool)
        self.setLayout(BoxLay)
        Stool.valueChanged.connect(WiNum.display)
        self.setGeometry(500, 500, 300, 200)
        self.setWindowTitle('EventTest')
        self.show()

if __name__ == '__main__':
    app = 0
    app = QApplication(sys.argv)
    win = EventTest01()
    sys.exit(app.exec_())
