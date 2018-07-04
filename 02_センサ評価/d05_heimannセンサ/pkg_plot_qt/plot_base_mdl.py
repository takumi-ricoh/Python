# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:17:46 2018

@author: takumi
"""
import numpy as np

#%%時系列グラフの親クラス
class Time_Plot():

    def __init__(self, plt):
        
        self.plt = plt
        
        #初期設定
        self.plt.setLabel("bottom",text="time")
        self.plt.setLabel("left",text="temperature")        
        self.plt.showGrid(x=True,y=True)
        self.plt.setYRange(0,300) 
        
        self.d=[]
      
    def init_line(self,obj,keys):
        
        #データオブジェクトへのリンク
        self.obj = obj
        
        #初期グラフ生成
        self.keys  = keys
        self.mylines = []      
        for key in self.keys:
            self.mylines.append(self.plt.plot(name=key[2]))

        #凡例表示
        self.plt.addLegend()

    def update(self):
        
        data = self.obj.get_value()
        
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            
            #ここはselfを付ける必要がある。
            self.sec = data[key[0]][key[1]]["sec"]
            self.val = data[key[0]][key[1]][key[2]]
            #self.d.append(self.val)

            #ラインを更新
            self.myline = self.mylines[idx]
            self.myline.setData(self.sec, self.val)
                                
#%%時系列グラフの親クラス
class Dist_Plot():

    def __init__(self, fig, ax):

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
        """
        ex) keys=["objs","ambs"]
        """
        self.keys = keys
        self.pos  = pos
        self.mylines = []        
        for key in self.keys:
            self.line =  self.ax.plot(self.pos, np.zeros_like(self.pos), ".-")[0]
            self.mylines.append(self.line)
            
        plt.show(block=False)
        
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