# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:22:30 2016

@author: p000495138
"""

"""
機能　：　NCセンサの検知・補償温度を計算する
入力　：　センサ電圧、電圧テーブル
出力　：　温度
"""

import numpy as np #行列計算
from scipy import interpolate

"""関数"""

#マッピング関数
def mapping(data1,data2):
    temp = interpolate.interp1d(data1,data2)
    return temp

#検知温度計算
def calc_tdet(vdet,vcomp,Vdet_table,Vcomp_table,Tdet_table):

    #初期化
    Vdet_cand = []
    tdet = []
    row_size,col_size     = Vdet_table.shape
    
    #step1 1列毎に検知電圧テーブルの候補を出す
    for i in range(col_size):
        fc   = mapping(Vcomp_table,Vdet_table[:,i])
        temp = fc(vcomp)               
        Vdet_cand.append(temp)

    #step2　検知電圧候補 vs 検知温度のマッピング
    ft = mapping(Vdet_cand,Tdet_table) #                    
    
    #step3 検知温度の計算
#    tdet.append( ft(vdet) )    
    tdet = ft(vdet)
    return tdet

#補償温度計算
def calc_tcomp(vcomp,Vcomp_table,Tcomp_table):
    #step1 補償→補償温度のマッピング
    fc = mapping(Vcomp_table,Tcomp_table)
    #step2 温度計算
    Tcomp = fc(vcomp)
    return Tcomp


"""クラス"""
class Calc_Temp():
    def __init__(self,Vdet,Vcomp,Vdet_table,Vcomp_table,Tdet_table,Tcomp_table):
        self.Vdet  = Vdet
        self.Vcomp =Vcomp
        self.Vdet_table   = Vdet_table
        self.Vcomp_table  = Vcomp_table
        self.Tdet_table   = Tdet_table
        self.Tcomp_table  = Tcomp_table        
        
    def calc_Tdet(self): #検知電圧による方法
        size = len(self.Vdet)
        temp = []
        for i in range(size):
            temp.append( calc_tdet(self.Vdet[i],self.Vcomp[i],self.Vdet_table,self.Vcomp_table,self.Tdet_table) )
        self.Tdet = np.array(temp)
        return self.Tdet

    def calc_Tdet_byTcomp(self): #検知電圧による方法(補償温度を使う方法)
        size = len(self.Vdet)
        temp = []
        for i in range(size):
            temp.append( calc_tdet(self.Vdet[i],self.Tcomp[i],self.Vdet_table,self.Tcomp_table,self.Tdet_table) )
        self.Tdet = np.array(temp)
        return self.Tdet

    def calc_Tcomp(self): #検知電圧による方法
        size = len(self.Vcomp)
        temp = []
        for i in range(size):
            temp.append( calc_tcomp(self.Vcomp[i],self.Vcomp_table,self.Tcomp_table) )
        self.Tcomp = np.array(temp)
        return self.Tcomp

