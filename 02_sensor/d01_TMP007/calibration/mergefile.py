# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:24:30 2017

@author: p000495138
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

filename1 = "c01_pi30_gap5mm_checkmode1.csv" #センサー
filename2 = "pi30_gap5mm_checkmode1.CSV"     #実温度

#%% センサデータ
sensor=[]
with open(filename1,"r") as f1:
    reader1 = csv.reader(f1)
    for i in reader1:
        sensor.append(i)
sensor = np.array(sensor,dtype=float)
    
#%% NRデータ
temp=[]
nr=[] #triger,temp
#read
with open(filename2,"r") as f2:
    reader2 = csv.reader(f2)
    for i in reader2:
        temp.append(i)
    for i in temp[62:-3]:
        nr.append(i[2:4])
nr = np.array(nr,dtype=float)
#pick
nr2=[]
for idx,i in enumerate(nr[1:]):
    if (nr[idx-1,0]<0.5)&(nr[idx,0]>1):
        nr2.append(nr[idx,1])
nr2 = np.array(nr2,dtype=float)    

#%% 合成
res = np.c_[sensor,nr2]  

#%% リサンプリング
from scipy.interpolate import interp1d
t = np.linspace(1,2000,2000)
f_die = interp1d(res[:,0],res[:,1],kind='linear')
f_det = interp1d(res[:,0],res[:,2],kind='linear')
f_volt = interp1d(res[:,0],res[:,3],kind='linear')
f_obj = interp1d(res[:,0],res[:,4],kind='linear')

h_die = f_die(t)
h_det = f_det(t)
h_volt = f_volt(t)
h_obj = f_obj(t)

res2=np.c_[t,h_die,h_det,h_volt,h_obj]