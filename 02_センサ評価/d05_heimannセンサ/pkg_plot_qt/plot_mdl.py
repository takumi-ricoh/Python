# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""
from pyqtgraph.Qt import QtCore, QtGui
from pkg_plot_qt import plot_base_mdl as base_p
#%%プロッタ
class Plotter():
    """
    グラフを配置する
    """
    def __init__(self, cfg):
        self.pos = cfg.SENPOS                
        self.InitPlot()
        
    def InitPlot(self):

        #グラフ生成
        self.plt1=self.plotlayout.addPlot(0,0)
        self.plt2=self.plotlayout.addPlot(0,1)
        self.plt3=self.plotlayout.addPlot(1,0)
        self.plt4=self.plotlayout.addPlot(1,1)
        
        #グラフ初期化
        self.sensor_plot     = SensorPlots (self.plt1)
        self.machine_plot    = MachinePlots(self.plt2) 
        #self.dist_plt       = DistPlots   (self.plt3)     
    
    def start(self):
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.sensor_plot.update)
        #self.timer.timeout.connect(self.machine_plot.update)
        #self.timer.timeout.connect(self.dist_plt.update())
        self.timer.start(10)    #10msごとにupdateを呼び出し

    def stop

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
       