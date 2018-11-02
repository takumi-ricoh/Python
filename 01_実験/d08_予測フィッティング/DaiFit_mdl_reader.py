# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 09:46:07 2018

@author: p000495138
"""

import numpy as np
import pandas as pd
import csv


#温度ドロップ係数
DROP  = (-0.0210843,-0.003312229,3.047559429)
DROP2 = (-0.037, 0.8204)
DROPFLG  = True
SAMPLING = 1


#%%データの分割
def data_splitter(dataobjs):

    for dataobj in dataobjs:
        
        df = dataobj.data
        
        dataobj.data0 = df[df["flg"]==0]
        dataobj.data1 = df[df["flg"]==1]
        dataobj.data2 = df[(df["flg"]==2) | (df["flg"]==3)]
        
    return dataobjs
        
#%%各データの格納
class Data():
    def __init__(self,filename,wid):
        self.filename = filename
        self.wid = wid
        
        #1.★★★一体データ★★★
        self.raw = self._dataTolist(filename)
        self.data = self._set_timer(self.raw) #タイマー振り直し
        self.idxs = self._get_index(self.raw) #インデックス取得
        self.data["diff"] = np.r_[0,np.diff(self.data["CLRtmp"])]
        
        #平均温度
        self.data["NCmean"] = self.data[["NCtmp1","NCtmp2"]].mean(axis=1)
        
        #2.フラグ設定
        self.diff = np.r_[np.diff(self.data["CLRonoff"])]

        #まず普通に設定
        flg = [0]
        for idx,i  in enumerate(self.diff):
            tmp = 0 #何もなければ0
            if flg[-1] ==1 :
                tmp = 1 #前が1なら1                          
            if flg[-1] == 2:
                tmp = 2 #前が2なら2            
                
            if self.diff[idx]>2:
                tmp = 1 #立ち上がったら1  
            if self.diff[idx]<-2:
                tmp = 2 #立ち下がっった2
            flg.append(tmp)
            
        #離間後のオーバーシュート
        flg2_1 = flg.copy()
        for idx,i  in enumerate(flg2_1):
            if 1 in flg[idx-2:idx-1]:
                flg2_1[idx] = 1

        #当接時遅れ
        flg2_2 = flg2_1.copy()
        for idx,i  in enumerate(flg2_2):
            if (flg2_1[idx]==1)and(flg2_1[idx-1]==2):
                flg2_2[idx] = 2
        
        #ここを変えると無視できる
        if DROPFLG==True:
            flg2 = flg2_2
        else:
            flg2 = flg

        #状態変化追加
        sts = [0]
        counter=0
        self.diff = np.r_[np.diff(flg2)]
        for idx,i  in enumerate(self.diff):
            if abs(i)>0.5:
                counter+=1
            sts.append(counter)
        self.data["stscounter"] = sts

        #ドロップ部分追加
        flg3 = flg2.copy()
        for idx,i in enumerate(flg3[5:]):
            if flg2[idx] == 2:#現在は2
                if sum(flg2[idx-5:idx-1]) < 8:
                    flg3[idx] = 3

        self.data["flg"] = flg3
        
            
        #3.ドロップ係数追加
        self.data["dropcoef"]  = DROP[0]*self.data["NCmean"] + DROP[1]*210 + DROP[2]           #加圧端部&紙幅から予測
        self.data["dropcoef2"] = DROP2[0]*(self.data["NCmean"]-self.data["CLRtmp"]) + DROP2[1] #加圧端部&クリロから予測


        #フラグの確認用
        self.data["CLRflg"] = np.int8(self.data["flg"]==1)*100
        
    #生データGET
    def _dataTolist(self,filename):
        self.label = ["TP_Vobj","TP_Vamb","NC_Vdet","NC_Vcomp","NC_Vdif",
                      "TPtmp1","TPtmp2","NCtmp1","NCtmp2","CLRtmp","PAP",
                      "CLRonoff","PAPfeed"]
        with open(filename, 'r',encoding='cp932') as f:
            reader = csv.reader(f)
            raw = [row for row in reader]
        
        #データ型変換+間引き
        mabiki = int(10*SAMPLING)
        raw = np.array(raw[62:-3])[::mabiki]
        raw = pd.DataFrame(raw[:,2:],columns=self.label,dtype=float)

        #先頭を揃える
        diff = np.diff(raw["CLRonoff"])
        idxs = np.where(diff>2)[0]
        raw  = raw.iloc[idxs[0]-300:].reset_index() #開始位置を揃える
        
        return raw
        
    #当接開始のインデックス
    def _get_index(self,data):
        diff = np.diff(data["CLRonoff"])
        idx = np.where(diff>2)[0]
        return idx        

    #時刻設定
    def _set_timer(self,data):
        n = len(data)
        data["sec"] = np.linspace(0, (n-1)*SAMPLING, n)
        return data