# -*- coding: utf-8 -*-
"""
係数をフィッティングする
"""
import matplotlib.pyplot as plt
import pandas as pd
import glob

import DaiFit_mdl_reader as r
import DaiFit_mdl_optimizer as op
import DaiFit_mdl_validation as v
import numpy as np


#%%ファイル読み込み
filelist   = glob.glob("データ\*.CSV")
filelist.sort() 
dataobjs = []
wid = [210,60,297,148,210,210,210,210,210,210,210,210,210,210,210,210,210,210]
for idx,file in enumerate(filelist):
    dataobj = r.Data(file,wid[idx])
    dataobjs.append(dataobj)

dataobjs  = r.data_splitter(dataobjs)
datas0    = [dataobj.data0 for dataobj in dataobjs]
datas1    = [dataobj.data1 for dataobj in dataobjs]
datas2    = [dataobj.data2 for dataobj in dataobjs]

#%%最適化(個別)
Opt0 = op.Optim(datas0, (0,100),  (0,) )
Opt1 = op.Optim(datas1, (0,300),  () )
Opt2 = op.Optim(datas2, (0,100),  () )
#最適化
Opt0.calc_a() #個別
Opt1.calc_b() #ｃは合計
Opt2.calc_a() #個別

#%%係数を格納
for idx,dataobj in enumerate(dataobjs):
    
    #個別
    coef={"a0":0,"b0":0,"c0":0,"a1":0,"b1":0,"c1":0,"a2":0,"b2":0,"c2":0,}
    #データ0
    coef["a0"] = Opt0.costobjs[idx].a
    coef["b0"] = Opt0.costobjs[idx].b
    coef["c0"] = Opt0.costobjs[idx].c
    #データ1
    coef["a1"] = Opt1.costobjs[idx].a
    coef["b1"] = Opt1.costobjs[idx].b
    coef["c1"] = Opt1.costobjs[idx].c
    #データ2        
    coef["a2"] = Opt2.costobjs[idx].a
    coef["b2"] = Opt2.costobjs[idx].b
    coef["c2"] = Opt2.costobjs[idx].c

    dataobj.coef = coef
#%%バリデーション結果計算
                
for dataobj in dataobjs:

    coef  = dataobj.coef
    coef0 = dataobjs[0].coef#共通係数

    #全データ
    data = dataobj.data.copy()
    valid = v.Validate(data)
    valid.set_coef(coef)   
    data["h"] = valid.calc()    
    valid.set_coef(coef0) 
    data["h2"] = valid.calc()   
    dataobj.data = data   

    #通紙前データ
    data0  = dataobj.data0.copy()
    valid0 = v.Validate(data0)
    valid0.set_coef(coef)   
    data0["h"] = valid0.calc()
    valid0.set_coef(coef0) 
    data0["h2"] = valid0.calc()
    dataobj.data0 = data0    

    #通紙中データ
    data1  = dataobj.data1.copy()
    valid1 = v.Validate(data1)
    valid1.set_coef(coef)   
    data1["h"] = valid1.calc()
    valid1.set_coef(coef0) 
    data1["h2"] = valid1.calc()
    dataobj.data1 = data1   

    #待機データ
    data2  = dataobj.data2.copy()
    valid2 = v.Validate(data2)
    valid2.set_coef(coef)   
    data2["h"] = valid2.calc()
    valid2.set_coef(coef0) 
    data2["h2"] = valid2.calc()    
    dataobj.data2 = data2   

#%%結果まとめ
result = {"data":[],"data0":[],"data1":[],"data2":[],"coef":[],"filename":[],"CLRdiff":[],"NCmean":[]}
for dataobj in dataobjs:
    result["data"].append(dataobj.data)
    result["data0"].append(dataobj.data0)
    result["data1"].append(dataobj.data1)
    result["data2"].append(dataobj.data2)
    result["coef"].append(dataobj.coef)
    result["filename"].append(dataobj.filename)
    result["CLRdiff"].append(dataobj.data["diff"])
    result["NCmean"].append(dataobj.data["NCmean"])

coefs = pd.DataFrame(result["coef"])

#%% プロット
def plotter(data,cols,rows,key,title):
    fig, axes = plt.subplots(ncols=cols, nrows=rows, figsize=(20, 15))
    for idx,dataframe in enumerate(data):
        dataframe.plot(x="sec",y=key,
                       grid=True,
                       title=title[idx][4:-4],
                       ax = axes.ravel()[idx],
                       xlim=[0,1500],
                       ylim=[0,180])
        axes.ravel()[idx].title.set_size(8)
        fig.tight_layout(pad=1, w_pad=0.5, h_pad=3)

#%% プロット(計算結果)
plt.close('all')
#plotter(データ, 行, 列, キー, 凡例)

#データ種類
data   = result["data1"]
title  = result["filename"]
key    = ["CLRtmp","h","h2","NCmean"]

#紙幅
d = [data[1] ,data[3] ,data[0], data[2]]
t = [title[1],title[3],title[0],title[2]]
plotter(d,4,2,key,t)

#紙長さ
d = [data[4] ,data[5] ,data[0], data[6]]
t = [title[4],title[5],title[0],title[6]]
plotter(d,4,2,key,t)

#設定温度
d = [data[7] ,data[0] ,data[8], data[9]]
t = [title[7],title[0],title[8],title[9]]
plotter(d,4,2,key,t)

#間欠
d = [data[11] ,data[10] ,data[0], data[12]]
t = [title[11],title[10],title[0],title[12]]
plotter(d,4,2,key,t)

#間欠同士の比較
d = [data[13] ,data[11],data[14],data[17]]
t = [title[13],title[11],title[14],title[17]]
plotter(d,4,2,key,t)

#線速
d = [data[0],data[16],data[15]]
t = [title[0],title[16],title[15]]
plotter(d,4,2,key,t)


#%%誤差まとめ

#通紙中の最大誤差
worst_err={"all":[],"rising":[],"descenting":[]}
for dataobj in dataobjs:

    #全体
    err = dataobj.data["h2"] - dataobj.data["CLRtmp"]
    err = err[dataobj.data["sec"] < 800]
    err_pick = err[dataobj.data["flg"]==1]
    worst_index = np.argmax(np.abs(err_pick))
    worst_err["all"].append(err_pick[worst_index])
    
    #上昇のみ
    err = dataobj.data1["h2"] - dataobj.data1["CLRtmp"]
    err = err[dataobj.data1["sec"] < 800]
    err_pick = err[dataobj.data1["flg"]==1]
    worst_index = np.argmax(np.abs(err_pick))
    worst_err["rising"].append(err_pick[worst_index])

    #下降のみ
    err = dataobj.data2["h2"] - dataobj.data2["CLRtmp"]
    err = err[dataobj.data2["sec"] < 800]
    err_pick = err[dataobj.data2["flg"]>1.5]
    worst_index = np.argmax(np.abs(err_pick))
    worst_err["descenting"].append(err_pick[worst_index])

worst_err = pd.DataFrame(worst_err)