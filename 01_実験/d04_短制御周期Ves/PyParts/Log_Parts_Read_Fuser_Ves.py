# -*- coding: utf-8 -*-
"""
Created on Thu May 25 13:32:39 2017

@author: p000495138
"""
import pandas as pd

# %%
"""温度ログクラス"""
class FuserTmp():
    
    def __init__(self):
        None
        
#%% 通常のログ
    def _read_fuser(self,data):
        data_list=[]
        for idx,line in enumerate(data):
            data_list.append(line.split()[0:16])
        return data_list
    
#%% データフレームに変換    
    def toDataframe(self,data):
        
        self.datalist = self._read_fuser(data)    
        
        column = ["a","FF","state","mode","motor",
          "tar_cen","tar_end","tar_prs",
          "duty_cen","duty_end",
          "tmp_cen","tmp_end","tmp_prs_cen","tmp_prs_end",
          "p","sec"]
        self.datapd = pd.DataFrame(self.datalist,columns=column)
        self.datapd = self.datapd.dropna()#欠損値含む行を除去
        self.datapd = self.datapd.drop(["a","p"],axis=1)
        self.datapd = self.datapd.astype(float)

        return self.datapd
#%%            
"""半波ログクラス"""
class FuserWave():    
    def __init__(self):      
        None
        
#%% 通常のログ
    def _read_wave(self,data):
        data_list = []
        for idx,line in enumerate(data):
            #print(idx)
            duty = line.split()[2]
            preduty = line.split()[4]
            flow = line.split()[5].split(":")[1]
            time = line.split()[6].split(":")[1]
            data_list.append([duty,preduty,flow,time])
        return data_list
    
#%% データフレームに変換    
    def toDataframe(self,data):
        self.data_list = self._read_wave(data)     
        column = ["duty","preduty","flow","time_wave"]
        self.datapd = pd.DataFrame(self.data_list,columns=column)
        self.datapd = self.datapd.dropna()#欠損値含む行を除去
        self.datapd = self.datapd.astype(float)
        return self.datapd