# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""
from pyqtgraph.Qt import QtCore, QtGui
from pkg_plot_qt import plot_base_mdl as base_p
#%%プロッタ
class Plotter():

    def __init__(self, pltcanvas, pool, CFG):

        self.canvas   = pltcanvas
        self.datapool = pool
        self.plots = {}
        self.InitPlot()
    
    #初期化
    def InitPlot(self):
        
        #プロットアイテムの登録
        for key,item in Plotter.CFG.items():
            
            #レイアウト
            row     = item['pos'][0]
            column  = item['pos'][1]            
            layout = self.canvas.addPlot(row,column)

            #プロットの種類を指定して、プロット生成
            if item['kind'] == 'timeseries':
                plt = TimePlots(layout, item, pool)
            if item['kind'] == 'distribution':
                plt = DistPlots(layout, item, pool)

            #登録
            self.plots[key] = plt
            
            
    #スタート
    def start(self):
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.plots["PLOT"].update)
        self.timer.start(10)    #10msごとにupdateを呼び出し

    #ストップ
    def stop(self):
        self.timer.stop()

#%%センサ時系列    
class TimePlots(base_p.Time_Plot):
        
    def __init__(self, plt, cfg, pool):
        
        #共通部分
        super().__init__(plt, pool)

        #初期設定
        self.plt.setTitle(cfg["title"])
        self.plt.setLabel("bottom",text="time")
        self.plt.setLabel("left",text="temperature")        
        self.plt.showGrid(x=True,y=True)
        self.plt.setYRange(0,300) 
        self.plt.addLegend() 

        #グラフの初期化
        self.init_line(cfg['keys'], cfg['legend'])

#%%センサ温度分布    
class DistPlots(base_p.Dist_Plot):
        
    def __init__(self, plt):

        super().__init__(plt)

        self.plt.setTitle(cfg["title"])
       