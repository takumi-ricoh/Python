# -*- coding: utf-8 -*-
"""
係数をフィッティングする
"""
import matplotlib.pyplot as plt
from scipy import optimize
import glob
import csv
import numpy as np
import pandas as pd
from numba.decorators import jit

#温度ドロップ係数
DROP  = (-0.0210843,-0.003312229,3.047559429)
DROP2 = (-0.037, 0.8204)
DROPFLG  = True
SAMPLING = 1

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

#%%ファイル読み込み
filelist   = glob.glob("データ\*.CSV")
filelist.sort() 
dataobjs = []
wid = [210,60,297,148,210,210,210,210,210,210,210,210,210,210,210,210,210,210]
for idx,file in enumerate(filelist):
    dataobj = Data(file,wid[idx])
    dataobjs.append(dataobj)

#%%a,b最適化
class Optimize_ab():

    def __init__(self,data):
        self.data = data
        self.methods = ["Nelder-Mead","Powell","CG","BFGS","Newton-CG","L-BFGS-B","TNC","COBYLA",
                        "SLSQP","trust-constr","dogleg","trust-ncg","trust-exact","trust-krylov"]
        #self.bounds = ((0.8,0.9999),(0,20))

    #最適化
    def calc_opt(self,tar,coef2):
        self.opt = optimize.minimize(self._calc_cost, [0.95,5], method=self.methods[0],tol=1e-10,args=(tar,coef2))
        #$self.opt = optimize.basinhopping(self._calc_cost,[0,0])
        self.a = 0.95 + self.opt["x"][0]/100
        self.b = 5 + self.opt["x"][1]
        self.L = self.opt["fun"]

    #誤差計算
    def _calc_cost(self,coef,tar,coef2):  
        #データ高速化のためnumpy化しておく
        CLRtmp   = np.array(self.data["CLRtmp"])
        NCmean   = np.array(self.data["NCmean"])
        dropcoef = np.array(self.data["dropcoef"])
        flg      = np.array(self.data["flg"])
        sts      = np.array(self.data["stscounter"])        
        #初期値
        h =  CLRtmp.copy()        

        #予測計算
        a= 0.95 + coef[0]/100
        b= 5 + coef[1]
        c=coef2
        h = self._calc_h(h,a,b,dropcoef,flg,sts,c,NCmean)
        
        #★誤差1
        err = h - CLRtmp
        L1  = sum(err**2)

        #★誤差2(係数範囲1)
        if tar[0] < b/(1-a) < tar[1]:
            L2 = 0
        else:
            L2=L1*10
        
        #★誤差3(マイナス制限)
        if min(err)>0:
            L3 = 0
        else:
            L3=L1*1000
    
        L = L1 + L2 + L3*0   
        
        return L
    
    #高速化   
    @jit
    def _calc_h(self,h,a,b,dropcoef,flg,sts,c,NCmean):
        #高速化計算
        for idx,i in enumerate(h):
            if idx>0:           
                #もしstscounterが切り替わったら真値にする(=何もしない)
                if sts[idx] != sts[idx-1]:
                    continue
                 
                #基本計算
                h[idx] = a*h[idx-1] + b + c*NCmean[idx-1]
                
                #もしドロップ領域なら、、、
                if DROPFLG == True:
                    if flg[idx] == 3:
                        h[idx] = h[idx-1] + dropcoef[idx-1]

        return h


#%% ★★★　全体最適化すラス　★★★
class Optimize_all():
    
    def __init__(self,dataobjs):
        
        self.fit = {"fit0":[],"fit1":[],"fit2":[]}

        #とりあえず全部をインスタンス化
        for dataobj in dataobjs:
            df = dataobj.data
    
            #通紙前データ
            data0 = df[df["flg"]==0]
            fit0 = Optimize_ab(data0)
            self.fit["fit0"].append(fit0)   
            
            #通紙中データ
            data1 = df[df["flg"]==1]
            fit1 = Optimize_ab(data1)
            self.fit["fit1"].append(fit1)   
            
            #通紙後データ
            data2 = df[(df["flg"]==2) | (df["flg"]==3)]
            fit2 = Optimize_ab(data2)
            self.fit["fit2"].append(fit2)    

    
    def calc_opt1(self,key,tar,opt):
        self.opt = optimize.minimize(self._calc_cost, [0], method="Nelder-Mead",tol=1e-10,args=(fitobjs,tar,True))
        
    def _calc_cost(coef2,fitobjs,tar,opt=False):   
        L = []
        for fit in fitobjs:
            fit.calc_opt(tar,coef2)    
            L.append(fit.L)
        return sum(L)
    
#%% ★★★　個別フィッティング　★★★

    target = (10,100) #飽和温度制約
    target = (10,300) #飽和温度制約
    target = (20,60) #飽和温度制約

    
#すべてのインスタンスを準備する
fitobjs = {"fit0":[], "fit1":[], "fit2":[]}
for dataobj in dataobjs:
    dataobj.coef = {}
    
    df = dataobj.data
    
    #通紙前データ
    data0 = df[df["flg"]==0]
    fit0 = Fit(data0)
    fitobjs["fit0"].append(fit0)   
    
    #通紙中データ
    data1 = df[df["flg"]==1]
    fit1 = Fit(data1)
    fitobjs["fit1"].append(fit1)   

    #通紙後データ
    data2 = df[(df["flg"]==2) | (df["flg"]==3)]
    fit2 = Fit(data2)
    fitobjs["fit2"].append(fit2)    

#フィッティングする






    
    fit0.calc_opt(target)    
    dataobj.coef["a0"] = fit0.a
    dataobj.coef["b0"] = fit0.b    
    dataobj.data0 = data0



    fit1.calc_opt(target)    
    
    
    dataobj.coef["a1"] = fit1.a
    dataobj.coef["b1"] = fit1.b
    dataobj.data1 = data1



    #fit2 = Fit([dataobj.data2[-1]])
    fit2.calc_opt(target)    
    dataobj.coef["a2"] = fit2.a
    dataobj.coef["b2"] = fit2.b  
    dataobj.data2 = data2

#温度低下は一つの係数にする
data2_com = pd.concat([data.data2 for data in dataobjs])
fit2_com = Fit(data2_com)
target = (20,60)
fit2_com.calc_opt(target)
for dataobj in dataobjs:
    dataobj.coef["a2x"] = fit2_com.a
    dataobj.coef["b2x"] = fit2_com.b

#%%係数の計算
class Validate():
    
    def __init__(self,data,dropOpt=False):
        #元のデータ
        self.data          = data
        self.CLRtmp        = np.array(data["CLRtmp"]) 
        self.dropcoef      = np.array(data["dropcoef"])
        self.sts           = np.array(data["stscounter"])
        self.flg           = np.array(data["flg"])
        self.dropOpt       = dropOpt
          
    #温度計算(特別に係数を使う場合)
    def set_coef(self,coef):
        self.coef = coef
    
    #温度計算
    def calc(self,indiv=True): 
        h = self.CLRtmp.copy()
        pred = self._calc_h(h, self.coef, self.dropcoef, self.flg, self.sts, indiv)
        return pred
    
    #高速化   
    #@jit
    def _calc_h(self,h,coef,dropcoef,flg,sts,indiv):
        #高速化計算
        for idx,i in enumerate(h):
            
            #係数設定
            if self.flg[idx] == 0:
                a=self.coef["a0"]
                b=self.coef["b0"]            
            if self.flg[idx] == 1:
                a=self.coef["a1"]
                b=self.coef["b1"]       
            if self.flg[idx] > 1:
                if indiv == False:
                    a=self.coef["a2x"]
                    b=self.coef["b2x"]                  
                else:
                    a=self.coef["a2"]
                    b=self.coef["b2"]                  
            
            #計算部分
            if idx>0:                            
                #はじめの領域はあってないので真値とする
                if flg[idx] == 0:
                    continue
                
                #基本計算
                h[idx] = a*h[idx-1]+b

                #もしドロップ領域なら、、、
                if DROPFLG == True:
                    if flg[idx] == 3:
                        h[idx] = h[idx-1] + dropcoef[idx-1]  

                #特殊対応1：data1:前の誤差を加える)
                if (flg[idx] == flg[idx-1] == 1):
                    if sts[idx] != sts[idx-1]:
                        er = h[idx-1] - self.CLRtmp[idx-1]
                        h[idx] = self.CLRtmp[idx] + er
                #特殊対応2：data2：前の誤差を加える)
                if (flg[idx]==3)&(flg[idx-1]==2):
                    if sts[idx] != sts[idx-1]:
                        er = h[idx-1] - self.CLRtmp[idx-1]
                        h[idx] = self.CLRtmp[idx] + er

        return h

#%%バリデーション結果計算
                
for dataobj in dataobjs:

    coef  = dataobj.coef
    coef0 = dataobjs[0].coef#共通係数

    #全データ
    data = dataobj.data.copy()
    valid = Validate(data)
    valid.set_coef(coef)   
    data["h"] = valid.calc()
    data["hx"] = valid.calc(False)
    valid.set_coef(coef0) 
    data["h2"] = valid.calc()   
    data["h2x"] = valid.calc(False)   
    dataobj.data = data   

    #通紙前データ
    data0  = dataobj.data0.copy()
    valid0 = Validate(data0)
    valid0.set_coef(coef)   
    data0["h"] = valid0.calc()
    valid0.set_coef(coef0) 
    data0["h2"] = valid0.calc()
    dataobj.data0 = data0    

    #通紙中データ
    data1  = dataobj.data1.copy()
    valid1 = Validate(data1)
    valid1.set_coef(coef)   
    data1["h"] = valid1.calc()
    valid1.set_coef(coef0) 
    data1["h2"] = valid1.calc()
    dataobj.data1 = data1   

    #待機データ
    data2  = dataobj.data2.copy()
    valid2 = Validate(data2)
    valid2.set_coef(coef)   
    data2["h"] = valid2.calc()
    data2["hx"] = valid2.calc(False)
    valid2.set_coef(coef0) 
    data2["h2"] = valid2.calc()    
    data2["h2x"] = valid2.calc(False)    
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
data   = result["data"]
title  = result["filename"]
key    = ["CLRtmp","h2x"]

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
