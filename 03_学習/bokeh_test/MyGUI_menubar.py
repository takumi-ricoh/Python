# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 13:58:19 2017

@author: p000495138
"""

import sys
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QWid
#import PyQt5.QtWidgets.QMainWindow as QMainWindow
#import PyQt5.QtWidgets.QApplication as QApplication
#import PyQt5.QtWidgets.QStyle as QStyle
#import PyQt5.QtWidgets.QAction as QAction

class Example(QWid.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):               
        exitGUI=QWid.QApplication.style().standardIcon(QWid.QStyle.SP_TitleBarCloseButton)
        exitAction = QWid.QAction(exitGUI, '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QWid.qApp.quit)

        qtInfoGUI=QWid.QApplication.style().standardIcon(QWid.QStyle.SP_TitleBarMenuButton)
        qtInfoAction = QWid.QAction(qtInfoGUI, '&AboutQt', self)        
        qtInfoAction.setShortcut('Ctrl+I')
        qtInfoAction.setStatusTip('Show Qt info')
        qtInfoAction.triggered.connect(QWid.qApp.aboutQt)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Info')
        fileMenu.addAction(qtInfoAction)
        fileMenu.addAction(exitAction)
        menubar.setNativeMenuBar(False) #for mac
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')    
        self.show()
        
def main():
    app = QWid.QApplication.instance()
    if app is None:
        app = QWid.QApplication(()) 
        #app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()   
