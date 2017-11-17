# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 12:10:23 2017

@author: p000495138
"""

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import sys
 
class PyQtExample(QtWidgets):
 
    def __init__(self):
        super(PyQtExample, self).__init__()
        self.initUi()
 
    def initUi(self):
        self.cmbMode = QtWidgets.QComboBox(self)
        self.cmbMode.addItems(('Item1','Item2','Item3','Item4','Item5'))
        self.cmbMode.move(50,50)
 
        self.chkTblPrefix = QtWidgets.QCheckBox(u'CheckBox Title',self)
        self.chkTblPrefix.move(50,80)
 
        self.btnExec = QtWidgets.QPushButton(u'実行',self)
        self.btnExec.move(50,110)
        self.btnExec.clicked.connect(self.doExecute)
 
        self.btnClear = QtWidgets.QPushButton(u'クリア',self)
        self.btnClear.move(150,110)
        self.btnClear.clicked.connect(self.doClear)
 
        self.txtIn = QtWidgets.QTextEdit(self)
        self.txtIn.move(50,160)
 
        self.txtOut = QtWidgets.QTextEdit(self)
        self.txtOut.move(350,160)
 
        self.setGeometry(200, 200, 700, 400)
        self.show()
 
    def doExecute(self, value):
        self.txtOut.append(self.txtIn.toHtml())
 
    def doClear(self, value):
        self.txtOut.clear()
        self.txtIn.clear()
 
if __name__ == '__main__':
    app=QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        
    example = PyQtExample()
    app.exec_()