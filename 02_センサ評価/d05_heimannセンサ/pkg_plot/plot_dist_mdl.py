# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 01:42:45 2018

@author: takumi
"""

import matplotlib.pyplot as plt

#%%時系列グラフの親クラス
class Plot_Dist():

    def __init__(self, fig, ax, ylim):

        #初期設定
        self.ax.set_xlabel("time")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        self.fig.canvas.draw()
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)
    
    def draw_update(self):
        #ライン更新
        self.fig.canvas.restore_region(self.bg)
        self.fig.canvas.draw()
        #画面の更新
        self.fig.canvas.update()
        self.fig.canvas.flush_events()