# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""
from PyQt5 import QMainWindow, QGridLayout
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pkg_plot_qt import plot_base_mdl as base_p

#%%プロッタ
class Plotter():
    """
    グラフを配置する
    """

    def __init__(self, cfg):
        self.pos = cfg.SENPOS        
        

    def InitUI(self):
        
        #ウィンドウ
        self.win = QMainWindow()
        self.plot  = pg.PlotWidget()
        
        #レイアウト
        self.win.setCentoralWidget(self.plot)
        
        #グラフ生成
        self.plt1=self.win.addPlot(0,0) #プロット配置
        self.plt2=self.win.addPlot(0,1) #プロット配置
        self.plt3=self.win.addPlot(1,0) #プロット配置
        self.plt4=self.win.addPlot(1,1) #プロット配置
        
        #グラフ初期化
        self.sensor_plot     = SensorPlots (self.plt1)
        self.machine_plot    = MachinePlots(self.plt2) 
        #self.dist_plt       = DistPlots   (self.plt3)     
    
        #表示開始
        
    def start(self):
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.sensor_plot.update)
        #self.timer.timeout.connect(self.machine_plot.update)
        #self.timer.timeout.connect(self.dist_plt.update())
        self.timer.start(10)    #10msごとにupdateを呼び出し

#%%センサ時系列    
class SensorPlots(base_p.Time_Plot):
        
    def __init__(self, plt):

        super().__init__(plt)

        self.plt.setTitle("sensor")
        

#%%マシンログ時系列    
class MachinePlots(base_p.Time_Plot):
        
    def __init__(self, plt):

        super().__init__(plt)
        
        self.plt.setTitle("machineLog")

        
#%%センサ温度分布    
class DistPlots(base_p.Dist_Plot):
        
    def __init__(self, plt):

        super().__init__(plt)

        self.plt.setTitle("DistPlot")

        