# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 11:35:35 2016

@author: p000495138
"""

import pandas as pd #ファイルI/O
import os.path #パス設定
import glob
import numpy as np
import matplotlib.pyplot as plt

plt.close()

#ファイルリスト
filedir      = os.chdir(r"D:\実験結果\03 NC標準計測器\d04 アルミブロックサーモグラフィ\パイプ")
filelist     = glob.glob('*.xls') 
file_num     = len(filelist) #

title = ['0s','10s','20s','30s','40s','50s','60s','100s','150s','200s','250s','300s','350s',
         '400s','450s','500s','550s','600s','650s','700s','750s']

#title = ['E140deg','E138deg']
title = ["pipe"]

#ファイルを全部読みだす
datas        = []
for i in range(file_num):
    book    = filelist[i]
    EXL     = pd.ExcelFile(book)
    temppd1 = EXL.parse(0) #pdとして読む
    temppd2 = temppd1.ix[8:,2:] #データ範囲切り出し
    tempnp  = np.array(temppd2,float) #np化
    datas.append(tempnp)

"""
#生データを表示
plt.figure(0)
for i in range(file_num):
    plt.subplot(4,6,i+1)
    plt.imshow(datas[i],vmin=20,vmax=150)
    plt.pcolor(datas[i])
    plt.tick_params(labelbottom='off')
    plt.tick_params(labelleft  ='off')
"""

#周辺温度を除去
datas2        = []
for i in range(file_num):
    temp = datas[i][5:25,60:180]
    #temp = datas[i][7:110,7:147]
    datas2.append(temp)

#各画像毎に平均温度からの偏差を計算 
datas3 = []
for i in range(file_num):
    ave  = np.average(datas2[i])
    temp = datas2[i]-ave
    print(np.max(temp))
    datas3.append(temp)

#偏差データを表示
plt.figure(1)
for i in range(file_num):
    plt.subplot(2,1,i+1)
    plt.imshow(datas3[i],vmin=-10,vmax=10)
    plt.tick_params(labelbottom='off')
    plt.tick_params(labelleft  ='off')
    plt.colorbar()
    plt.title(title[i],fontsize=10)

#偏差データの等高線表示
plt.figure(2)
for i in range(file_num):
    plt.subplot(2,1,i+1)
    CS = plt.contour(datas3[i],vmin=-10,vmax=10)
    plt.tick_params(labelbottom='off')
    plt.tick_params(labelleft  ='off')
    plt.title(title[i],fontsize=10)

#切り出しの枠を表示
waku = datas[0].copy()
#waku[7:110,7]=  0
#waku[7:110,147]=  0
#waku[7,7:147]=  0
#waku[110,7:147]=  0
waku[5:25,60]=  0
waku[5:25,180]=  0
waku[5,60:180]=  0
waku[25,60:180]=  0
plt.figure(3)
plt.imshow(waku,vmin=20,vmax=300)
plt.title(filelist[0])