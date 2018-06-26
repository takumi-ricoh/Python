# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""


import matplotlib.pyplot as plt
from pkg_plot import plot_base_mdl as base_p

#%%プロッタ
class Plotter():
    
    def __init__(self, param):
        self.pos = param["senPos"]
        plt.close()
    
        #グラフ生成
        self.fig, self.ax = plt.subplots(2,2)
        
    
        #グラフ初期化
        self.sensor  = SensorPlots(self.fig, self.ax[0,0])
        self.machine = MachinePlots(self.fig, self.ax[0,1]) 
        self.dist    = DistPlots(self.fig, self.ax[1,0], self.pos)     
    
        self.fig.tight_layout()
    
#%%センサ時系列    
class SensorPlots(base_p.Time_Plot):
        
    def __init__(self, fig, ax):

        super().__init__(fig, ax)

        self.ax.set_title("sensor")


#%%マシンログ時系列    
class MachinePlots(base_p.Time_Plot):
        
    def __init__(self, fig, ax,):
        
        super().__init__(fig, ax,)
        
        self.ax.set_title("machineLog")

        
        
#%%センサ温度分布    
class DistPlots(base_p.Dist_Plot):
        
    def __init__(self, fig, ax, pos):
        self.fig    = fig
        self.ax     = ax
        self.pos    = pos
        self.ax.set_title("DistPlot")

        super().__init__(self.fig, self.ax, self.pos)
        

#%%テスト用

#a=Plotter(plotter_param)

#if __name__ == '__main__':
#    plotter = Plotter