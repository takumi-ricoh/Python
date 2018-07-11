# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 17:18:31 2018

@author: p000495138
"""
from PyQt5 import QtWidgets as Qtw
import pyqtgraph as pg
#%% GUI
class GUI(Qtw.QMainWindow):

    def __init__(self):

        super().__init__()

        self.InitUI()

    def InitUI(self):
               
        #題名
        self.setWindowTitle('おれおれグラフ生成アプリケーション')
        #メニュー画面
        self.set_menu()
        #ボタン
        button_box = self.set_button()        
        #ボタンアクションの設定
        self.set_button_action()  
        #プロット流域の設定        
        self.plotArea = self.set_plotArea()          
        #レイアウトの設定        
        self.set_layout(button_box,self.plotArea)
        #ウィンドウの設定
        self.set_window()

    #%% ファイルメニュー
    def set_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')        

    #%% ボタンレイアウト
    def set_button(self):

        #ボタン(Hboxレイアウト)
        self.okButton = Qtw.QPushButton("OK")
        self.stopButton = Qtw.QPushButton("Stop")
        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.stopButton)        
        
        return hbox

    #%% ボタンアクション
    def set_button_action(self):
        self.stopButton.clicked.connect(None)

    #%% プロットレイアウト
    def set_plotArea(self):
        plotlayout  = pg.GraphicsLayoutWidget()        
        return plotlayout

    #%% 全体レイアウト設定
    def set_layut(self,hbox,plotlayout):
        #Vboxレイアウト
        vbox = Qtw.QVBoxLayout()
        vbox.addLayout(hbox)        
        vbox.addWidget(self.plotlayout)

        return vbox

    #%% ウィンドウセット
    def set_window(self,vbox):
        self.setLayout(vbox)
        self.show()

#        #ウィジェット領域
#        wid = Qtw.QWidget()
#        #vboxをセット
#        wid.setLayout(vbox)

        #ウィンドウにセット
#        self.setCentralWidget(wid)
        
        #ウィンドウ表示 