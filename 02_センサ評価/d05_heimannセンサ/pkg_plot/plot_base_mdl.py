# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:17:46 2018

@author: takumi
"""

import matplotlib.pyplot as plt
import numpy as np

#%%時系列グラフの親クラス
class Time_Plot():

    def __init__(self, fig, ax):

        #初期設定
        self.ax.set_xlabel("time")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        self.fig.canvas.draw()
        #self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)
    
    def init_line(self,keys):
        self.keys  = keys
        self.lines = []        
        for i in self.keys:
            self.lines.append(self.ax.plot(0,0,".-")[0])

    def update(self,data):
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            sec = data[key[0]][key[1]]["sec"]
            val = data[key[0]][key[1]][key[2]]
            
            line = self.lines[idx]
            line.set_data(sec, val)
            self.ax.draw_artist(line)

    def draw_update(self):
        #ライン更新
        self.fig.canvas.restore_region(self.bg)
        self.fig.canvas.draw()
        #画面の更新
        self.fig.canvas.update()
        self.fig.canvas.flush_events()


#%%時系列グラフの親クラス
class Dist_Plot():

    def __init__(self, fig, ax, pos):

        #初期設定
        self.ax.set_xlabel("pos[mm]")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        self.fig.canvas.draw()
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        
        #ポジション
        self.pos = pos

    def init_line(self, keys):
        """
        ex) keys=["objs","ambs"]
        """
        self.keys = keys
        self.lines = []        
        for i in self.keys:
            tmp =  self.ax.plot(self.pos, np.zeros_like(self.pos), ".-")[0]
            self.lines.append(tmp)
        
    def update(self,data):
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            line = self.lines[idx]

            #dataの最終行の温度分布
            dist = data[key].iloc[-1,:]
            
            line.set_data(self.pos, dist)
            self.ax.draw_artist(line)

    def draw_update(self):
        #ライン更新
        self.fig.canvas.restore_region(self.bg)
        self.fig.canvas.draw()
        #画面の更新
        self.fig.canvas.update()
        self.fig.canvas.flush_events()