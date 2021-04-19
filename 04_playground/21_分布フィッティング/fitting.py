# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:51:39 2019

@author: r00495138
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

#%%データ読み込み
dataset = pd.read_csv("sample.csv")
x = dataset["x"]
y = dataset["y"]

#%%近似関数
def func(x, *params):

    #フィッティングする関数の数
    num_func = int(len(params)/3)
    
    #ガウス関数
    y_list=[]

    for i in range(num_func):
        y = np.zeros_like(x)
        param_range = list(range(3*i,3*(i+1),1))
        amp = params[int(param_range[0])]
        ctr = params[int(param_range[1])]
        wid = params[int(param_range[2])]
        y = y + amp * np.exp(-((x-ctr)/wid)**2)
        y_list.append(y)
        
    #y_listのガウス関数を重ね合わせる
    y_sum = np.zeros_like(x)
    for i in y_list:
        y_sum = y_sum + i
        
    #最後にバックグラウンドを追加
    y_sum = y_sum + params[-1]
    
    return y_sum
    
#%%プロット用関数
def fit_plot(x, *params):
    num_func = int(len(params)/3)
    y_list = []
    for i in range(num_func):
        y = np.zeros_like(x)
        param_range = list(range(3*i,3*(i+1),1))
        amp = params[int(param_range[0])]
        ctr = params[int(param_range[1])]
        wid = params[int(param_range[2])]
        y = y + amp * np.exp(-((x-ctr)/wid)**2) + params[-1]
        y_list.append(y)
    return y_list

#%%実行(初期化)

#[amp,ctr,wid]    
guess = []
guess.append([4500,760,10])
guess.append([7500,775,10])
#guess.append([7500,775,10])

#バックグラウンドの初期値
background = 5

#初期値リストの結合
guess_total = []
for i in guess:
    guess_total.extend(i)
guess_total.append(background)

#%%フィッティング
popt, pcov = curve_fit(func, x, y, p0=guess_total)

#%%結果の確認
fit = func(x, *popt)
plt.scatter(x, y, s=20)
plt.plot(x, fit, ls="-", c="black", lw=1)

y_list = fit_plot(x, *popt)
baseline = np.zeros_like(x) + popt[-1]
for n,i in enumerate(y_list):
    plt.fill_between(x, i, baseline, facecolor=cm.rainbow(n/len(y_list)), alpha=0.6)
