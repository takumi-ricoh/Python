# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""


import matplotlib.pyplot as plt
from plot_base_mdl import Time_Plot
from plot_base_mdl import Dist_Plot

#%%プロッタ
class Plotter():
    
    def __init__(self, param):
        self.pos = param["senPos"]
        plt.close()
    
        #グラフ生成
        self.fig, self.ax = plt.subplots(2,2)
    
        #グラフ初期化
        self.sensor  = SensorPlots(self.fig, self.ax[0,0])
        #self.machine = MachinePlots(self.fig, self.ax[0,1]) 
        #self.dist    = DistPlots(self.fig, self.ax[1,1], self.pos)     
    
#%%センサ時系列    
class SensorPlots(Time_Plot):
        
    def __init__(self, fig, ax,):
        self.fig    = fig
        self.ax     = ax
        self.ax.title = "sensor"

        #super().__init__(self.fig, self.ax,)
        

#%%マシンログ時系列    
class MachinePlots(Time_Plot):
        
    def __init__(self, fig, ax,):
        self.fig    = fig
        self.ax     = ax
        self.ax.title = "machinelog"

        super().__init__(self.fig, self.ax,)
        
#%%センサ温度分布    
class DistPlots(Dist_Plot):
        
    def __init__(self, fig, ax, pos):
        self.fig    = fig
        self.ax     = ax
        self.pos    = pos
        self.ax.title = "machinelog"

        super().__init__(self.fig, self.ax, self.pos)
        

#%%テスト用

a=Plotter(plotter_param)

#if __name__ == '__main__':
#    plotter = Plotter