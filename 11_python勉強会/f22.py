# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:02:46 2020

@author: p000495138
"""


#%%　f22        
def f22(data):
    #分ける
    temp1 = data
    temp2 = temp1.split('|')
    temp3 = temp2[-1].split(',')
    #時刻を計算
    time_str = temp2[2].split(':')
    time = float(time_str[0])*60 + float(time_str[1]) #秒単位換算
    #数値に変換
    Tar = np.float64(temp3[1])
    Cur = np.float64(temp3[3])
    #センサ種類
    Sen = temp2[1]
    #print(Sensor)
    return [time,Tar,Cur]