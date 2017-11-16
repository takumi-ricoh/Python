# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 18:08:34 2017

@author: p000495138
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import scipy.interpolate as interp

#温湿度センサ / 相対湿度テーブル
humid_table = np.loadtxt("humid_table.csv",delimiter=",")
humid_table_humid = humid_table[1:,1:]
humid_table_temp  = humid_table[0,1:]
humid_table_vout  = humid_table[1:,0]

#温湿度センサ / 温度テーブル
vth_table = np.loadtxt("vth_table2.csv",delimiter=",")
vth_table_temp = vth_table[:,0]
vth_table_vth  = vth_table[:,1]
f1 = interp.interp1d(vth_table_vth, vth_table_temp, bounds_error=False)

#データ
filename = "d05_Chimay50ppm_LL_マイペHH調湿_ガイド板無し_非TEC_50枚連続.CSV" 
data = []
with open(filename,"r") as f:
    reader = csv.reader(f)
    for i in reader:
        data.append(i)
data = np.array(data[63:-5])
nr_temperature  = np.float32(data[:,2])
nr_vout         = np.float32(data[:,3])
nr_vth          = np.float32(data[:,4])

#温湿度センサ温度計算
humid_temp = f1(nr_vth) 
#humid_temp = -35.269*nr_vth + 79.355

#温湿度センサ湿度計算
humid_temp2 = humid_temp // 5 * 5 #5℃ピッチ切り捨て
nr_vout2  = nr_vout // 0.05 * 0.05 #0.05vピッチ切り捨て

#相対湿度計算
#インデックス
temp_idx = np.searchsorted(humid_table_temp,humid_temp2)
humid_idx = np.searchsorted(humid_table_vout,nr_vout)
#45℃以上の場合
temp_idx2=temp_idx.copy()
temp_idx2[temp_idx==9] = 8 #エラー回避
 
#結果
humid = humid_table_humid[humid_idx,temp_idx2]
humid[temp_idx==9]=0 #50℃超えは0にする

#絶対湿度計算
a=7.5*humid_temp2/(humid_temp2+273.3)
humid_absolute = 217*(6.11*10**a)/(humid_temp2+273.15)*humid*0.01

#プロット
plt.plot(humid)
plt.plot(humid_temp)
plt.plot(humid_temp2)
plt.plot(humid_absolute)
plt.grid(True)
plt.legend(["humid","humid_temp","humid_temp2","humid_absolute"])

#保存
t=np.linspace(0,0.1*(len(humid)-1),len(humid))
pddata = np.array([t,nr_temperature,humid,humid_absolute,humid_temp,nr_vout]).T
column = ["t","temp","humid","humid_absolute","humid_temp","nr_vout"]
savedata = pd.DataFrame(pddata,columns=column)
savename = filename + "_res.csv"
savedata.to_csv(savename)