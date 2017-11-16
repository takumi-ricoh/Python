# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:11:29 2016

@author: p000495138
"""
import numpy as np
from scipy.optimize import curve_fit

"""抽出"""
def cut(data,Vshutter,dminus,dplus):
    res = []
    for i in range(len(Vshutter)):
        if (Vshutter[i-1]>2)&(Vshutter[i]<2):
            temp = data[i-dminus:i+dplus,:]
            res.append(temp)
        else:
            None
    return res

"""フィルタ"""
#移動平均
def move_average(data,n):
    s = np.ones(n)/n
    res = np.convolve(data,s)
    res = res[:-(n-1)]
    return res

#正規化(0～1)
def normalize(data):
    temp      = (data-np.min(data))
    data_norm = temp/np.max(temp)    
    return data_norm

#一次遅れフィルタ
def primary_delay(data,ts,tau):
    #ts: sampling period[ms]
    #tau: time constant[ms]
    res = [data[0]]
    temp = data[0]
    for i in range(len(data)-1):
        temp = (temp + data[i] * ts/tau) / (1 + ts/tau)
        res.append(temp)
    return np.array(res)

#むだ時間
def lag(data,ts,lag):
    c=list(data)#リストにする
    # ts:sampling period[ms]
    # lag[ms]
    lag_num = int(lag/ts) #移動量を計算
    res=c[0:lag_num] #頭部分を抽出
    for i in range(lag_num+1,len(data)+1):
        res.append(c[i-lag_num])    
    return np.array(res)

"""近似"""
#sigmoid
def call_sigmoid(x,y):
    initial = np.array([0.0, 0.0, 0.0, 0.0])
    
    def hyp_sigmoid(x,a,b,c,d):
        temp = a/(1+np.exp(-b*(x-c)))+d
        return temp        
        
    print("大きさ")
    print(np.shape(x))
    print(np.shape(y))
    param, cov = curve_fit(hyp_sigmoid, x, y, p0=initial)
    hyp = hyp_sigmoid(x, param[0], param[1], param[2], param[3])
    return hyp 

#speed
def call_speed(x,y):
    initial = np.array([0.0, 0.0])    
    
    def hyp_speed(x,a,b):
        temp = np.zeros(len(x))
        temp[x>a] = y[x>a]
        return temp        
    
    param, cov = curve_fit(hyp_speed, x, y, p0=initial)
    hyp = hyp_speed(x, param[0], param[1])
    return hyp 

"""積算"""
#ベクトル出力
def sen_sum(y,n):
    ysum = []
    temp = y[0]
    for i in range(n):
        ysum.append(temp)
        temp = temp + y[i]
    return ysum

