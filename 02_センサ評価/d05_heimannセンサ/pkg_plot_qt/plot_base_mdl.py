# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:17:46 2018

@author: takumi
"""
import numpy as np

#%%時系列グラフの親クラス
class Time_Plot():

    def __init__(self, plt, pool):
        
        self.plt  = plt
        self.pool = pool
              
    def get_value(self, pool):
        value = pool.get_value()
        return value
    
    def init_line(self,keys,legend):
        
        #初期グラフ生成
        self.keys  = keys
        self.mylines = []      
        for i,key in enumerate(self.keys):
            self.mylines.append(self.plt.plot, sname=legend[i])

    def update(self):
        
        data = self.get_value(self.pool)
        
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            
            #ここはselfを付ける必要がある。
            self.sec = data[key[0]][key[1]][key[2]]["sec"]
            self.val = data[key[0]][key[1]][key[2]][key[3]]

            #ラインを更新
            self.myline = self.mylines[idx]
            self.myline.setData(self.sec, self.val)
                                
#%%時系列グラフの親クラス
class Dist_Plot():

    def __init__(self, plt, pool):

        self.fig = fig
        self.ax  = ax        
        
        #初期設定
        self.ax.set_xlabel("pos[mm]")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        self.fig.canvas.draw() 
        #self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def init_line(self, keys, pos):
        self.keys = keys
        self.pos  = pos
        self.mylines = []        
        for key in self.keys:
            self.line =  self.ax.plot(self.pos, np.zeros_like(self.pos), ".-")[0]
            self.mylines.append(self.line)
            
        #plt.show(block=False)
        
    def update(self,data):
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            #空データのば愛、エラーになるので、例外にしておく
            try:
                #dataの最終行の温度分布
                self.dist = data[key[0]][key[1]].iloc[-1][1:]
                #ラインを更新
                self.mylines[idx].set_data(self.pos,list(self.dist))
                #高速化
                #self.ax.draw_artist(self.ax.patch)
                #self.ax.draw_artist(self.mylines[idx])
            except:
                pass

        self._draw_update()
            
    def _draw_update(self):
        
        #self.fig.canvas.restore_region(self.bg)
        #ライン更新
        #self.fig.canvas.update()
        self.fig.canvas.draw()

        #画面の更新
        self.fig.canvas.flush_events()