# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:31:40 2018

@author: p000495138
"""

import numpy as np
from numba.decorators import jit
DROPFLG  = True

#%%係数の計算
class Validate():
    
    def __init__(self,data):
        #元のデータ
        self.data          = data
        self.CLRtmp        = np.array(data["CLRtmp"]) 
        self.dropcoef      = np.array(data["dropcoef"])
        self.sts           = np.array(data["stscounter"])
        self.flg           = np.array(data["flg"])
        self.NCmean        = np.array(data["NCmean"])
          
    #温度計算(特別に係数を使う場合)
    def set_coef(self,coef):
        self.coef = coef
    
    #温度計算
    def calc(self): 
        h = self.CLRtmp.copy()
        pred = self._calc_h(h, self.coef, self.dropcoef, self.flg, self.sts)
        return pred
    
    #高速化   
    #@jit
    def _calc_h(self,h,coef,dropcoef,flg,sts):
        #高速化計算
        for idx,i in enumerate(h):
            
            #係数設定
            if self.flg[idx] == 0:
                a=self.coef["a0"]
                b=self.coef["b0"]            
                c=self.coef["c0"]
            if self.flg[idx] == 1:
                a=self.coef["a1"]
                b=self.coef["b1"] 
                c=self.coef["c1"]
            if self.flg[idx] > 1:
                a=self.coef["a2"]
                b=self.coef["b2"]
                c=self.coef["c2"]
            
            #計算部分
            if idx>0:                            
                #はじめの領域はあってないので真値とする
                if flg[idx] == 0:
                    continue
                
                #基本計算
                h[idx] = a*h[idx-1] + b + c*self.NCmean[idx-1]

                #もしドロップ領域なら、、、
                if DROPFLG == True:
                    if flg[idx] == 3:
                        h[idx] = h[idx-1] + dropcoef[idx-1]  

                #特殊対応1：data1:前の誤差を加える)
                if (flg[idx] == flg[idx-1] == 1):
                    if sts[idx] != sts[idx-1]:
                        er = h[idx-1] - self.CLRtmp[idx-1]
                        h[idx] = self.CLRtmp[idx] + er
                #特殊対応2：data2：前の誤差を加える)
                if (flg[idx]==3)&(flg[idx-1]==2):
                    if sts[idx] != sts[idx-1]:
                        er = h[idx-1] - self.CLRtmp[idx-1]
                        h[idx] = self.CLRtmp[idx] + er

        return h
