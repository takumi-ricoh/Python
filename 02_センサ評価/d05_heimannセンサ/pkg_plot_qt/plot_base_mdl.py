# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:17:46 2018

@author: takumi
"""
import numpy as np
from PyQt5.QtGui import QColor as qc
import pyqtgraph as pg

#%%時系列グラフの親クラス
class Time_Plot():

    def __init__(self, plt, pool):
        
        self.plt  = plt
        self.pool = pool
              
    def get_value(self):
        value = self.pool.get_value()
        return value
    
    def init_line(self,keys,legend):
        
        #初期グラフ生成
        self.keys  = keys
        self.mylines = []      
        for i,key in enumerate(self.keys):
            self.mylines.append(self.plt.plot(name=legend[i],pen=(i,10)))

    def update(self):
        #print("start update")
        data = self.get_value()
        
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            
            #ここはselfを付ける必要がある。
            self.sec = data[key[0]][key[1]][key[2]]["sec"]
            self.val = data[key[0]][key[1]][key[2]][key[3]]

            #print(self.sec)
            #ラインを更新
            self.myline = self.mylines[idx]
            self.myline.setData(self.sec, self.val)
            
            #print("lineupdate")
                                
#%%時系列グラフの親クラス
class Dist_Plot():

    def __init__(self, plt, pool):

        self.plt  = plt
        self.pool = pool      

    def get_value(self):
        value = self.pool.get_value()
        return value

    def init_line(self, keys, pos, legend):
        self.keys = keys
        self.pos  = pos
        self.mylines = []        
        for i,key in enumerate(self.keys):
            self.mylines.append(self.plt.plot(self.pos, np.zeros_like(self.pos),symbol="o",name=legend[i]))
            
        #plt.show(block=False)
        
    def update(self):

        data = self.get_value()
        #キーの数だけアップデート           
        for idx,key in enumerate(self.keys):
            #           #空データのば愛、エラーになるので、例外にしておく
            #dataの最終行の温度分布
            self.dist = data[key[0]][key[1]][key[2]].iloc[-1][1:]
            #ラインを更新
            self.myline = self.mylines[idx]
            self.myline.setData(self.pos,list(self.dist))

