# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""


import matplotlib.pyplot as plt
import plot_series_mdl as s


class Plotter():
    
    def __init__(self, param):
        plt.close()
    
        #グラフ生成
        self.fig, self.ax = plt.subplots(2,2)
    
        #グラフ初期化
        self.sensor  = s.SensorSeries(self.fig, self.ax[0,0])
        self.machine = s.MachineSeries(self.fig, self.ax[0,1]) 
    
    
