# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:31:30 2017

@author: p000495138
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Parts.Log_Parts_Read2 as rd
import Parts.Log_Parts_Read_Fuser as rdf
from multiprocessing import Process
import concurrent.futures

#前回のグラフを消す
plt.close("all")

# %%　ログデータ抽出クラス
class GetContinuousData():
    def __init__(self,shift):
        self.shift = shift
        self.f01 = pd.DataFrame(columns=[])
        self.f06 = pd.DataFrame(columns=[])
        self.f22 = pd.DataFrame(columns=[])
        self.f26 = pd.DataFrame(columns=[])
        self.f27 = pd.DataFrame(columns=[])
        self.f91 = pd.DataFrame(columns=[])
        self.fAll = pd.DataFrame(columns=[])
        
    def getdata(self,file): 
        self.filename      = file
        self.strdata       = self._readfile(self.filename)
        self.fusDataList   = self._getFuserCmd(self.strdata)
        self._list2pd(self.fusDataList)
        self._timeshift(self.shift)
        self._combineAll()

    #ログファイルを読み込む
    def _readfile(self,file): 
        #読出し
        file_handler = rd.Read()#初期化
        strdata = file_handler.readfile(file)
        return strdata

    #Fuserコマンドのデータをリストで受け取る
    def _getFuserCmd(self,data): 
        #fuserコマンド
        fusCmd_handler = rdf.Read_fuser() #初期化
        fusCmd_handler.read_fuser(self.strdata) #抽出して登録
        return fusCmd_handler
    
    #リストデータをデータフレームに変換する    
    def _list2pd(self,data): 
        for idx,i in enumerate(data.f22):
            idx2=str(idx)
            temp = pd.DataFrame(i,columns=["time"+idx2,"TargetTemp"+idx2,"CurentTemp"+idx2,"Sensor"+idx2])
            self.f22 = pd.concat([self.f22,temp],axis=1)

        self.f26 = pd.DataFrame(data.f26,columns= ["time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        self.f27 = pd.DataFrame(data.f27,columns= ["time","kp","ki","Buff0","Tar","dMVn","dMVn_p","dMVn_i","MVn_1","MVn","Heater"])
        self.f06 = pd.DataFrame(data.f06,columns= ["time", "vel"])
        self.f01 = pd.DataFrame(data.f01,columns= ["time", "sts1", "sts2"])
        self.f91 = pd.DataFrame(data.f91,columns= ["time","R_Duty","LO_Duty","CO_Duty","PTN","err"])

    #初期時刻を0にセットする。
    def _timeshift(self,shift): 
        crit = self.f22["time0"][0]

        self.f22["time0"]=self.f22["time0"] - crit
        self.f22["time1"]=self.f22["time1"] - crit
        self.f22["time2"]=self.f22["time2"] - crit
        self.f22["time3"]=self.f22["time3"] - crit
        self.f22["time4"]=self.f22["time4"] - crit
        self.f22["time5"]=self.f22["time5"] - crit
        self.f22["time6"]=self.f22["time6"] - crit
        self.f26["time"]=self.f26["time"] - crit
        self.f27["time"]=self.f27["time"] - crit
        self.f91["time"]=self.f91["time"] - crit
        self.f06["time"]=self.f06["time"] - crit
        self.f01["time"]=self.f01["time"] - crit

    #f06のサンプリングが粗いので矩形データにする
    def _f06adjust(self):
        for idx,i in self.f06.iloc[1:]:
            temp = i
            temp.name = idx+0.5
            self.f06 = self.f06.append(temp)
        


    def _combineAll(self):
        mergedata = [self.f22,self.f26,self.f27,self.f91,self.f06,self.f01]
        self.fAll = pd.concat(mergedata,axis=1,keys=["f22","f26","f27","f91","f06","f01"])


#%%ファイルリスト
def setfilelist():
    filelist = [
    "d15_GriC3_bEU_40ms_dutyと電力の関係確認.txt",
    ]
    return filelist

#%%実行
    
filelist = setfilelist()
#ファイル処理
res=[]
for idx,i in enumerate(filelist):
    obj = GetContinuousData(i)
    obj.getdata(i)
    res.append(obj) 

#できれば並列実行したい
for i in res:
    name = i.filename
    i.fAll.to_csv(name+"_res.csv")

#        #時刻シフト
#        crit = self.f22[0][0,0] - self.shift
#        for i in self.f22:#センサ数だけ        
#            i[:,0] = i[:,0] - crit
#        self.f26[:,0] = self.f26[:,0] - crit
#        self.f27[:,0] = self.f27[:,0] - crit
#        self.f91[:,0] = self.f91[:,0] - crit                                
#        #f06        
#        self.f06[:,0] = self.f06[:,0] - crit
#        temp=[]
#        for idx,i in enumerate(self.f06):
#            if idx>0:
#                temp.append([self.f06[idx,0],self.f06[idx-1,1]])
#            temp.append(self.f06[idx,:])
#        self.f06 = np.array(temp)
##
##        #f01
##        self.f01[:,0]=(np.float32(self.f01[:,0])-crit).astype(str)
##        self.f01_move = self.f01[self.f01[:,2] == ",Move,"]
##        self.f01_perm = self.f01[self.f01[:,2] != ",Move,"]