# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 13:57:05 2017

@author: p000495138
"""

import sys
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QWid
import datetime

class Example(QWid.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):               
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')    
        self.show()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.time_draw)
        timer.start(1000) #msec       
       

    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")
        self.statusBar().showMessage(daystr)

def main():
    app = QWid.QApplication.instance()
    if app is None:
        app = QWid.QApplication(()) 
        #app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
