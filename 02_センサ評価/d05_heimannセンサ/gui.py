# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 17:18:31 2018

@author: p000495138
"""
from PyQt5 import QtWidgets as Qtw
from PyQt5.QtGui import QFont
import pyqtgraph as pg

    
#%% GUI画面
class GUI(Qtw.QMainWindow):

    def __init__(self):

        super().__init__()

        self._set_layout()

    #%% アクションのセッティング
    def set_action(self, adapter):
        print(type(adapter))
        dir(adapter)
        self.startButton.clicked.connect(lambda: adapter.start())
        self.stopButton.clicked.connect(lambda: adapter.stop())

    #%% レイアウト初期化
    def _set_layout(self):
               
        #フォント
        font = QFont("Meiryo UI")
        
        #題名
        self.setWindowTitle('おれおれグラフ生成アプリケーション')
        #メニュー画面
        #self._set_menu()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')     

        #ボタン
        #self.hbox = self._set_button()      
        #self._set_window(self.hbox)
        self.startButton = Qtw.QPushButton("Start")
        self.stopButton = Qtw.QPushButton("Stop")
        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.stopButton) 
        
        
        #プロット流域の設定        
        #self.pltcanvas = self._set_plotArea()          
        self.pltcanvas  = pg.GraphicsLayoutWidget()     
        self.pltcanvas.setBackground((50,50,50))

        #レイアウトの設定        
        #self.vbox = self._set_layouts(self.hbox, self.pltcanvas)
        vbox = Qtw.QVBoxLayout()
        vbox.addLayout(hbox)        
        vbox.addWidget(self.pltcanvas)

        #ウィンドウの設定
        #self._set_window(self.vbox)
        widget = Qtw.QWidget()
        widget.setLayout(vbox)
        #まとめてフォント変更
        widget.setFont(font)
        self.setCentralWidget(widget)
        self.show()

    #%% ファイルメニュー
    def _set_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')        

    #%% ボタンレイアウト
    def _set_button(self):

        #ボタン(Hboxレイアウト)
        self.startButton = Qtw.QPushButton("OK")
        self.stopButton = Qtw.QPushButton("Stop")
        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.startButton)
        hbox.addWidget(self.stopButton)        
        
        return hbox

    #%% プロットレイアウト
    def _set_plotArea(self):
        pltcanvas  = pg.GraphicsLayoutWidget()        
        return pltcanvas

    #%% 全体レイアウト設定
    def _set_layouts(self,hbox,pltcanvas):
        #Vboxレイアウト
        vbox = Qtw.QVBoxLayout()
        vbox.addLayout(hbox)        
        vbox.addWidget(pltcanvas)

        return vbox

    #%% ウィンドウセット
    def _set_window(self,vbox):
        widget = Qtw.QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        #self.setLayout(vbox)
        self.show()
