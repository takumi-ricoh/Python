# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:07:39 2017

@author: p000495138
"""

import sys
from PyQt5.QtWidgets import QApplication,QWidget

if __name__ == "__main__":
    app=QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    w=QWidget()
    w.resize(250,150)
    w.move(300,300)
    w.setWindowTitle("Simple")
    w.show()
    
    app.exec_()
    