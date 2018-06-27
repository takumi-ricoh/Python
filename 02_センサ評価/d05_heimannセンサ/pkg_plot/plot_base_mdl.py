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
        
        self.fig = fig
        self.ax  = ax
        
        #初期設定
        self.ax.set_xlabel("time")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        self.fig.canvas.draw() 
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)
    
    def init_line(self,keys):
        self.keys  = keys
        self.mylines = []        
        for i in self.keys:
            self.mylines.append(self.ax.plot([1,2,3],[4,5,6],"-")[0])

    def update(self,data):
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            #print(data[key[0]][key[1]][key[2]])
            self.sec = data[key[0]][key[1]]["sec"]
            self.val = data[key[0]][key[1]][key[2]]
#            
            self.myline = self.mylines[idx]
            self.myline.set_data(self.sec, self.val)
            
            #self.ax.set_xlim(0,self.sec[-1]+1)
            
            self.ax.draw_artist(self.myline)

        return self.sec, self.val
        #print("line_updated")

    def draw_update(self):
        #ライン更新
        self.fig.canvas.restore_region(self.bg)
        self.fig.canvas.draw()
        #画面の更新
        self.fig.canvas.update()
        self.fig.canvas.flush_events()
        
        print("draw_updated")


#%%時系列グラフの親クラス
class Dist_Plot():

    def __init__(self, fig, ax, pos):

        self.fig = fig
        self.ax  = ax        
        
        #初期設定
        self.ax.set_xlabel("pos[mm]")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        #self.fig.canvas.draw()
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