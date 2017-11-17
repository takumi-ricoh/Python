# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:04:34 2017

@author: p000495138
"""


import numpy as np #行列計算
from scipy import interpolate,stats
from scipy import optimize as op
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import csv
import re

plt.close("all")
#%% マッピング関数
def mapping(data1,data2):
    temp = interpolate.interp1d(data1,data2,bounds_error=False,fill_value=max(data2))
    return temp

#%% 補償温度計算
def calc_temp(v,vtable,ttable):
    #step1 補償→補償温度のマッピング
    fc = mapping(vtable,ttable)
    #step2 温度計算
    temp = fc(v)
    return temp

#%% RtoV(使わない)
def r_to_v(r,rpu):
    vcc = 3.3
    v = vcc * r/(r+rpu)
    return v
    
#%% テーブルデータ読み出し
def read_table(tablename):
    tablename_full = tablename    #ファイル名&フルパス
    table_data = np.loadtxt(tablename_full,delimiter=",")    #リードはフルパスで行う
    return table_data

#%% 実験データ読み出し
def read_expdata(filename):       

    #ファイルを開く
    with open(filename,"r",encoding="cp932") as f:
        dat = [k for k in csv.reader(f)]
    #データ部分抽出
    a = [ i[2::] for i in dat[62:-3] ]
    #numpy配列
    exp_data = np.float32(a)
    return exp_data

#%% ファイル読み出し順
def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

#%%一次遅れフィルタ
def primary_delay(data,ts,tau):
    #ts: sampling period[ms]
    #tau: time constant[ms]
    res = [data[0]]
    temp = data[0]
    for i in range(len(data)-1):
        temp = (temp + data[i] * ts/tau) / (1 + ts/tau)
        res.append(temp)
    return np.array(res)

#%% データ定義クラス
class DataRead:
    def __init__(self):
        self.dir = r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ"         
        self.table = []

    def settable(self,tablename):
        print(tablename)
        self.table = read_table(tablename)

    def setdir(self):
        os.chdir(self.dir)

    def settboj(self,tobj):
        self.tobj = tobj

    def fileread(self,column):
        self.filelist = sorted(glob.glob("*.csv"),key=numericalSort)
        
        self.datalist =[]
        for idx,i in enumerate(self.filelist):
            exp_data = read_expdata(i)
            size = len(exp_data)
            t = np.linspace(0.0,size*0.1,size)
            ir    = exp_data[:,column[0]]
            vdet  = exp_data[:,column[1]]
            vcomp = exp_data[:,column[2]]
            tdet  = calc_temp(vdet,self.table[:,1],self.table[:,0])
            tcomp = calc_temp(vcomp,self.table[:,1],self.table[:,0])
            df = pd.DataFrame(np.array([t,ir,vdet,vcomp,tdet,tcomp]).T,columns=["t","ir","vdet","vcomp","tdet","tcomp"])
            self.datalist.append(df)

#%% フィッティングクラス
class Fitting: #DataReadオブジェクトを読む
    def __init__(self,data):
        self.filelist = data.filelist            
        self.datalist = data.datalist    
        self.opt1 = []#最適化結果1    
        self.opt2 = []#最適化結果2   
        self.fitres = []#最適化結果   
        
    def fit1(self):
        for idx,da in enumerate(self.datalist):
            #最適化
            opt = op.minimize(self.costfunc1,np.array([1,1,1]),method="Powell",args=(da["t"],da["ir"],da["tdet"]))
            self.opt1.append(opt)

    def set_gapcase(self,num):
        self.case = num

    def set_tobj(self,tobj):
        self.tobj = tobj
        
    def set_tamb(self,tamb):                
        self.tamb = tamb
        
    #%%結果をまとめる
    def calc_res(self,opt):
        for idx,da in enumerate(self.datalist):        
            gain = opt[idx]['x'][0]
            tau  = opt[idx]['x'][1]
            lag  = opt[idx]['x'][2]
            
            #フィッティング波形
            fitform = self.appro(da["t"],da["ir"],da["tdet"],gain,tau,lag)
            #オフセット計算
            offset = np.average((da["ir"] - fitform)[-10:-1])#後ろから10個の平均
            #温度概算
            tdet_def = np.average(fitform[0:10])     #初期検知温度
            tdet_last = np.average(fitform[-10:-1])  #最終検知温度
            tcomp_def = np.average(da["tcomp"][0:10])     #初期補償温度
            tcomp_last = np.average(da["tcomp"][-10:-1])     #最終補償温度   
            #gapデータ
            gap = self.readgap(self.case, self.filelist[idx])
            #データフレームに追加
            da["fitform"] = fitform
            #保存
            self.fitres.append([tau,offset,tdet_def,tdet_last,tcomp_def,tcomp_last,gap,self.tobj[idx],self.tamb[idx]])
            
        columns=["tau","offset","tdet_def2","tdet_last","tcomp_def","tcomp_last","gap","tobj","tamb"]
        self.summary = pd.DataFrame(self.fitres,columns=columns)

    #%% 近似する関数
    def appro(self,t,ir,tdet,gain,tau,lag):
        res = []
        init_temp = np.average(tdet[0:10])
        #近似式
        for i in t:
            if i >= lag:
                temp = init_temp + gain*(1-np.exp(-(i-lag)/tau))
            else:
                temp = init_temp 
            res.append(temp)  
        return res
            
    #%% 評価関数(2乗誤差)
    def costfunc1(self,param,t,ir,tdet):
        #最適化する引数
        gain=param[0]
        tau=param[1]
        lag=param[2]
        #計算値
        res = self.appro(t,ir,tdet,gain,tau,lag)
        err = tdet - res
        #評価関数
        cost = np.sum(err**2) #最小化したいもの
        return cost

    #%%ファイル名からGap抽出
    def readgap(self,case,filename):
         if case == 1:
             a=filename.split(".")
             b=a[0].split("_")
             c=b[1].split("p")
             d=(225-int(c[1]))/10
             return d
         elif case == 2:
             a=filename.split(".")
             b=a[0].split("_")
             c=b[2].split("p")
             d=(225-int(c[1]))/10
             return d
         elif case == 3:
             a=filename.split(".")
             b=a[0].split("_")
             c=b[2].split("(")
             d=c[0].split("p")
             e=(int(d[1])-69)/10
             return e

#%% データ分割クラス
class DataSplit():
    def __init__(self,summary):
        self.sum = summary #データフレーム
        
    def temp_split(self):   
        d_cold120 = self.sum[(self.sum["tamb"] == "cold" )&(self.sum["tobj"] == 120)]
        d_cold170 = self.sum[(self.sum["tamb"] == "cold" )&(self.sum["tobj"] == 170)]        
        d_cold210 = self.sum[(self.sum["tamb"] == "cold" )&(self.sum["tobj"] == 210)]
        d_hot120 = self.sum[(self.sum["tamb"] == "hot" )&(self.sum["tobj"] == 120)]        
        d_hot170 = self.sum[(self.sum["tamb"] == "hot" )&(self.sum["tobj"] == 170)]
        d_hot210 = self.sum[(self.sum["tamb"] == "hot" )&(self.sum["tobj"] == 210)]
        #データセット
        self.temp_splitset  = [d_cold120,d_cold170,d_cold210,d_hot120,d_hot170,d_hot210]
        self.temp_splitname = ["cold/120","cold/170","cold/210","hot/120","hot/170","hot/210"]        
        self.temp_splitaxes = [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1]]        

    def gap_split1(self):   
        gap03 = self.sum[self.sum["gap"] == 0.3]
        gap05 = self.sum[self.sum["gap"] == 0.5]
        gap07 = self.sum[self.sum["gap"] == 0.7]
        gap09 = self.sum[self.sum["gap"] == 0.9]
        gap13 = self.sum[self.sum["gap"] == 1.3]
        gap17 = self.sum[self.sum["gap"] == 1.7]
        self.gap1_splitset  = [gap03,gap05,gap07,gap09,gap13,gap17]
        self.gap1_splitname = ["gap0.3mm","gap0.5mm","gap0.7mm","gap0.9mm","gap1.3mm","gap1.7mm",]        
        self.gap1_splitaxes = [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1]]        

    def gap_split2(self):   
        gap05 = self.sum[(0.4 <= self.sum["gap"])&(self.sum["gap"] <= 0.6)]
        gap09 = self.sum[(0.8 <= self.sum["gap"])&(self.sum["gap"] <= 1.0)]
        gap13 = self.sum[(1.2 <= self.sum["gap"])&(self.sum["gap"] <= 1.4)]

        self.gap2_splitset  = [gap05,gap09,gap13]
        self.gap2_splitname = ["gap0.5mm","gap0.9mm","gap1.3mm"]        
        self.gap2_splitaxes = [[0,0],[0,1],[1,0]]        

    def diff_split(self):   
        diff1 = self.sum[(0 <= self.sum["diff"])&(self.sum["diff"] <= 20)]
        diff2 = self.sum[(70 <= self.sum["diff"])&(self.sum["diff"] <= 80)]
        diff3 = self.sum[(100 <= self.sum["diff"])&(self.sum["diff"] <= 130)]

        self.diff_splitset  = [diff1,diff2,diff3]
        self.diff_splitname = ["0<dif<20","70<dif<80","100<dif<130"]        
        self.diff_splitaxes = [[0,0],[0,1],[1,0]]        

#%% 近似
def data_regress(data,key1,key2,name):
    slope, intercept, r_value, _, _ = stats.linregress(data[key1],data[key2])
    x = data[key1]
    y = slope*x + intercept
    data[name] = y

    return slope,intercept

#%%
"""以下実行"""


#%% データ1（横付き1)
side1 = DataRead()
side1.dir = r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\d03_横付き冷間状態"
side1.setdir()
side1.settable(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\芝浦2素子換算表.csv")
side1.fileread([0,2,3])

#フィッティング
side1_fit = Fitting(side1)
side1_fit.fit1()

side1_fit.set_gapcase(1) #モード3データ追加
side1_fit.set_tobj([70]*6+[120]*5+[170]*8+[210]*7) #対象温度データ追加
side1_fit.set_tamb(["cold"]*len(side1.filelist)) #雰囲気温度データ追加
side1_fit.calc_res(side1_fit.opt1)
side1_fit.summary["diff"] = side1_fit.summary["tdet_last"] - side1_fit.summary["tcomp_last"]

#%% データ2（横付き2)
side2 = DataRead()
side2.dir = r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\d06_横付き熱間データ"
side2.setdir()
side2.settable(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\芝浦2素子換算表.csv")
side2.fileread([0,2,3])

#フィッティング
side2_fit = Fitting(side2)
side2_fit.fit1()
side2_fit.set_gapcase(2) #モード3データ追加
side2_fit.set_tobj([120]*11+[170]*14+[210]*14) #対象温度データ追加
side2_fit.set_tamb(["hot"]*len(side2.filelist))#雰囲気温度データ追加
side2_fit.calc_res(side2_fit.opt1)

#差分計算
side2_fit.summary["diff"] = side2_fit.summary["tdet_last"] - side2_fit.summary["tcomp_last"]


#%% データ1+2(結合)
side_summary = side1_fit.summary.append(side2_fit.summary)

#分割
side_split = DataSplit(side_summary)
side_split.temp_split()#温度で分割
side_split.gap_split2()#温度で分割
side_split.diff_split()#温度差分で分割

#近似
cof1_side=[]
for data in side_split.temp_splitset:
    slope,intercept = data_regress(data,"gap","offset","reg_side")
    cof1_side.append([slope,intercept])
cof1_side=np.array(cof1_side)

cof2_side=[]
for data in side_split.gap2_splitset:
    slope,intercept = data_regress(data,"diff","offset","reg_side")    
    cof2_side.append([slope,intercept])
cof2_side=np.array(cof2_side)

cof3_side=[]
for data in side_split.diff_splitset:
    slope,intercept = data_regress(data,"gap","offset","reg_side") 
    cof3_side.append([slope,intercept])
cof3_side=np.array(cof3_side)

#%%データ3（上付き)
up = DataRead()
up.dir = r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\d07_上付き補償振り"
up.setdir()
up.settable(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\芝浦2素子換算表.csv")
up.fileread([0,3,4])

#フィッティング
up_fit = Fitting(up)
up_fit.fit1()
up_fit.set_gapcase(3) #モード3
up_fit.set_tobj(([120]*11+[170]*11+[210]*11)*3) #対象温度
up_fit.set_tamb(["cold"]*33 + ["warm"]*33 +["hot"]*33)
up_fit.calc_res(up_fit.opt1)
#差分計算
up_fit.summary["diff"] = up_fit.summary["tdet_last"] - up_fit.summary["tcomp_last"]

#分割
up_split = DataSplit(up_fit.summary)
up_split.temp_split()#温度で分割
up_split.gap_split1()#温度で分割
up_split.diff_split()#温度差分で分割

#近似
cof1_up=[]
for data in up_split.temp_splitset:
    slope,intercept = data_regress(data,"gap","offset","reg_up")
    cof1_up.append([slope,intercept])
cof1_up=np.array(cof1_up)

cof2_up=[]
for data in up_split.gap1_splitset:
    slope,intercept = data_regress(data,"diff","offset","reg_up")    
    cof2_up.append([slope,intercept])
cof2_up=np.array(cof2_up)

cof3_up=[]
for data in up_split.diff_splitset:
    slope,intercept = data_regress(data,"gap","offset","reg_up") 
    cof3_up.append([slope,intercept])
cof3_up=np.array(cof3_up)  

#%%データ4 検証用データ
valid = DataRead()
valid.dir = r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\検証データd01_横付き上げ下げ"
valid.setdir()
valid.settable(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\芝浦2素子換算表.csv")
valid.fileread([0,1,2])

def calc_val(valid):
    gaplist = [0.5,0.7,1.0,0.3]            
    for idx,i in enumerate(valid.datalist):
        data = valid.datalist[idx]  
        gap  = gaplist[idx]

        #時定数成分計算
        tau = 1.57*gap + 0.72
        assume1 = primary_delay(data["ir"],0.1,tau)
    
        #オフセット計算
        slope = 0.3642*gap - 0.0075
        inter = -5.0554*gap - 0.995
        offset = (data["tdet"]-data["tcomp"])*slope-inter
        assume2 = assume1 - offset
        
        #初期温度補正
        initerr = np.average(assume2[0:10] - data["tdet"][0:10])
        assume3 = assume2 - initerr

        data["assume1"] = assume1
        data["assume2"] = assume2
        data["assume3"] = assume3
        
        err = assume3 - data["tdet"]
        data["err"] = err
    
#まとめて計算する
calc_val(valid)

#プロット()
plt.figure(0)
data=valid.datalist[2]
ax=data.plot(x="t",y=["ir","assume1","assume3","tdet"],xlim=[0,100],ylim=[0,350],grid=True,)
ax.set_xlabel("sec")
ax.set_ylabel("deg")
ax.set_title("gap1.0mm")

plt.figure(2)
data=valid.datalist[2]
ax1=data.plot(x="t",y=["ir","tdet","tcomp"],xlim=[0,1200],ylim=[0,400],grid=True,)
ax1.set_xlabel("sec")
ax1.set_ylabel("deg")
ax1.set_title("gap1.0mm")
ax2=ax1.twinx()
data.plot(x="t",y="err",xlim=[0,1200],ylim=[-20,20],ax=ax2,grid=True,c="k")
ax2.set_ylabel("err")

#%%データ5 Gimlet暴走推定データ
#gimlet = DataRead()
#gimlet.dir = r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\暴走見積もりd00_Gimlet"
#gimlet.setdir()
#gimlet.settable(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\芝浦2素子換算表.csv")
#gimlet.fileread([0,1,2])
#
#gimlet_temp = gimlet.datalist[0]["ir"].to_frame()
#gimlet_cold = gimlet.datalist[0]["ir"].to_frame()
#gimlet_hot  = gimlet.datalist[0]["ir"].to_frame()
#gaplist = np.linspace(0,2,21)
#
##熱間補正
#ir_init_cold = gimlet_cold["ir"][0:10].mean()    
#ir_init_hot  = 190
#gimlet_hot["ir"] = gimlet_hot["ir"]+(ir_init_hot-ir_init_cold)
#
##応答波形推定
#for gap in gaplist:
#
#    #時定数成分計算
#    #tau  = 1.57*gap + 0.72 #横付き
#    tau  = 1.55*gap + 0.67 #横付き
#    ir2_cold = primary_delay(gimlet_cold["ir"],0.1,tau)
#    ir2_hot  = primary_delay(gimlet_hot["ir"],0.1,tau)
#    
#    #オフセット特性計算
#    slope = 0.3642*gap - 0.0075 #横付き
#    inter = -5.0554*gap - 0.995 #横付き
#
#    #補償温度推定値 = ir
#    tcomp_pred_cold = ir_init_cold
#    tcomp_pred_hot  = ir_init_hot
#    
#    #検知温度推定式
#    tdet_pred_cold = 1/(1+slope)*(ir2_cold + slope * tcomp_pred_cold - inter)
#    tdet_pred_hot  = 1/(1+slope)*(ir2_hot + slope  * tcomp_pred_hot - inter) #設定温度最大とする
#       
#    #マージ
#    cname = "gap="+str(gap)
#    gimlet_temp[cname]   = ir2_cold #時定数のみ
#    gimlet_cold[cname]   = tdet_pred_cold
#    gimlet_hot[cname]    = tdet_pred_hot

#%%
"""以下プロット"""
#%%　グラフ1 (gap vs オフセット)
#upset      = up_split.temp_splitset
#upset_name = up_split.temp_splitname
#upset_ax   = up_split.temp_splitaxes
#
#sideset      = side_split.temp_splitset
#sideset_name = side_split.temp_splitname
#sideset_ax   = side_split.temp_splitaxes
#
##プロット
#fig1, axes1 = plt.subplots(nrows=3, ncols=2,figsize=(8,8))        
#upset[0].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[0,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#upset[1].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[1,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#upset[2].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[2,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#upset[3].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[0,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#upset[4].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[1,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#upset[5].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[2,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#sideset[0].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[0,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#sideset[1].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[1,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#sideset[2].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[2,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#sideset[3].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[0,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#sideset[4].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[1,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#sideset[5].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[2,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#upset[0].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[0,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#upset[1].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[1,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#upset[2].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[2,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#upset[3].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[0,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#upset[4].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[1,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#upset[5].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[2,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#sideset[0].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[0,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#sideset[1].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[1,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#sideset[2].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[2,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#sideset[3].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[0,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#sideset[4].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[1,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#sideset[5].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[2,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#fig1.tight_layout()

#%%　グラフ1 (gap vs オフセット)
#upset      = up_split.gap1_splitset
#upset_name = up_split.gap1_splitname
#upset_ax   = up_split.gap1_splitaxes
#
#sideset      = side_split.gap2_splitset
#sideset_name = side_split.gap2_splitname
#sideset_ax   = side_split.gap2_splitaxes

#プロット
#fig1, axes1 = plt.subplots(nrows=3, ncols=2,figsize=(8,8))        
#upset[0].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[0,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#upset[1].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[1,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#upset[2].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[2,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#upset[3].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[0,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#upset[4].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[1,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#upset[5].plot(x="gap",y="offset",kind="scatter",c="c",ax=axes1[2,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#sideset[0].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[0,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#sideset[1].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[1,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#sideset[2].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[2,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#sideset[3].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[0,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#sideset[4].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[1,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#sideset[5].plot(x="gap",y="offset",kind="scatter",c="m",ax=axes1[2,1],s=20,grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#upset[0].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[0,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#upset[1].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[1,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#upset[2].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[2,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#upset[3].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[0,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#upset[4].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[1,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#upset[5].plot(x="gap",y="reg_up",kind="line",c="c",ax=axes1[2,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#sideset[0].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[0,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/120")
#sideset[1].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[1,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/170")
#sideset[2].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[2,0],grid=True,xlim=[0,2],ylim=[-10,80],title="cold/210")
#sideset[3].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[0,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/120")
#sideset[4].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[1,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/170")
#sideset[5].plot(x="gap",y="reg_side",kind="line",c="m",ax=axes1[2,1],grid=True,xlim=[0,2],ylim=[-10,80],title="hot/210")
#fig1.tight_layout()



#
#
#upset_reg[0].plot(x="gap", y="offset", kind="scatter",c="m",ax=axes1[0,0],s=20,grid=True,xlim=[0,2],ylim=[-10,80])
#
#plot1 = Myplot()
#plot1.setparam([0,2],[-10,80],"gap[mm]","offset","c","m",["up"]*len(upset))
#plot1.setfigure(3,2)
#plot1.plot(upset,upset_ax,"gap","offset")


#data_up_fit.summary.to_csv("data_side.csv")




#
##%% フィッティングクラス
#class DataFit:
#    
#
#
#
#table=read_table()
#
#templist1=[]
#os.chdir(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\d03_横付き冷間状態")
#filelist1 = glob.glob("*.csv")
#for i in filelist1:
#    filename = i
#    exp_data = read_expdata(i)
#    size = len(exp_data)
#    t = np.linspace(0.0,size*0.1,size)
#    ir    = exp_data[:,0]
#    vdet  = exp_data[:,2]
#    vcomp = exp_data[:,3]
#    
#    tdet  = calc_temp(vdet,table[:,1],table[:,0])
#    tcomp = calc_temp(vcomp,table[:,1],table[:,0])
#    templist1.append(np.array([t,ir,vdet,vcomp,tdet,tcomp]).T)
#
#templist2=[]    
#os.chdir(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\d06_横付き熱間データ")
#filelist2 = glob.glob("*.csv")
#for i in filelist2:
#    filename = i    
#    exp_data = read_expdata(i)
#    size = len(exp_data)
#    t = np.linspace(0.0,size*0.1,size)
#    ir    = exp_data[:,0]
#    vdet  = exp_data[:,2]
#    vcomp = exp_data[:,3]
#
#    tdet  = calc_temp(vdet,table[:,1],table[:,0])
#    tcomp = calc_temp(vcomp,table[:,1],table[:,0])
#    templist2.append(np.array([t,ir,vdet,vcomp,tdet,tcomp]).T)
#    
#templist3=[]    
#os.chdir(r"E:\09 非接触サーミスタ距離依存\d07_芝浦2素子まとめ\d07_上付き補償振り")
#filelist3 = sorted(glob.glob("*.csv"),key=numericalSort)
#for i in filelist3:
#    filename = i    
#    exp_data = read_expdata(i)
#    size = len(exp_data)
#    t = np.linspace(0.0,size*0.1,size)
#    ir    = exp_data[:,0]
#    vdet  = exp_data[:,3]
#    vcomp = exp_data[:,4]
#
#    tdet  = calc_temp(vdet,table[:,1],table[:,0])
#    tcomp = calc_temp(vcomp,table[:,1],table[:,0])    
#    templist3.append(np.array([t,ir,vdet,vcomp,tdet,tcomp]).T)
#    
#
##%% フィッティング
##データ1
#fitdata1=[]
##plt.figure(1)
#for idx,i in enumerate(templist1):
#    #データ展開
#    t  = i[:,0]
#    ir = i[:,1]
#    tdet = i[:,4]
#    tcomp = i[:,5]    
#    #最適化
#    opt = op.minimize(costfunc,np.array([1,1,1]),method="Powell",args=(t,ir,tdet))
#    gain=opt['x'][0]
#    tau=opt['x'][1]
#    lag=opt['x'][2]
#    #フィッティング波形
#    fitform = appro(t,ir,tdet,gain,tau,lag)
#    #オフセット
#    offset = np.average((ir - fitform)[-10:-1])#後ろから10個の平均
#    #温度概算
#    tdet_def = np.average(fitform[0:10])     #初期検知温度
#    tdet_last = np.average(fitform[-10:-1])  #最終検知温度
#    tcomp_def = np.average(tcomp[0:10])     #初期補償温度
#    tcomp_last = np.average(tcomp[-10:-1])     #最終補償温度   
#    #保存
#    fitdata1.append([tau,offset,tdet_def,tdet_last,tcomp_def,tcomp_last])
#    #プロット
##    plt.subplot(10,10,idx+1)
##    plt.plot(t,tdet)
##    plt.plot(t,fitform)
##データ2
#fitdata2=[]
##plt.figure(2)
#for idx,i in enumerate(templist2):
#    #データ展開
#    t  = i[:,0]
#    ir = i[:,1]
#    tdet = i[:,4]
#    tcomp = i[:,5]    
#    #最適化
#    opt = op.minimize(costfunc,np.array([1,1,1]),method="Powell",args=(t,ir,tdet))
#    gain=opt['x'][0]
#    tau=opt['x'][1]
#    lag=opt['x'][2]
#    #フィッティング波形
#    fitform = appro(t,ir,tdet,gain,tau,lag)
#    #オフセット
#    offset = np.average((ir - fitform)[-10:-1])#後ろから10個の平均
#    #温度概算
#    tdet_def = np.average(fitform[0:10])     #初期検知温度
#    tdet_last = np.average(fitform[-10:-1])  #最終検知温度
#    tcomp_def = np.average(tcomp[0:10])     #初期補償温度
#    tcomp_last = np.average(tcomp[-10:-1])     #最終補償温度   
#    #保存
#    fitdata2.append([tau,offset,tdet_def,tdet_last,tcomp_def,tcomp_last])
#    #プロット
##    plt.subplot(10,10,idx+1)
##    plt.plot(t,tdet)
##    plt.plot(t,fitform)
#
##データ3
#fitdata3=[]
#plt.figure(3)
#for idx,i in enumerate(templist3):
#    #データ展開
#    t  = i[:,0]
#    ir = i[:,1]
#    tdet = i[:,4]
#    tcomp = i[:,5]    
#    #最適化！！！
#    opt = op.minimize(costfunc,np.array([1,1,1]),method="Powell",args=(t,ir,tdet))
#    gain=opt['x'][0]
#    tau=opt['x'][1]
#    lag=opt['x'][2]
#    #フィッティング波形
#    fitform = appro(t,ir,tdet,gain,tau,lag)
#    #オフセット
#    offset = np.average((ir - fitform)[-10:-1])#後ろから10個の平均
#    #温度概算
#    tdet_def = np.average(fitform[0:10])     #初期検知温度
#    tdet_last = np.average(fitform[-10:-1])  #最終検知温度
#    tcomp_def = np.average(tcomp[0:10])     #初期補償温度
#    tcomp_last = np.average(tcomp[-10:-1])     #最終補償温度   
#    #保存
#    fitdata3.append([tau,offset,tdet_def,tdet_last,tcomp_def,tcomp_last])
#    #プロット
#    plt.subplot(9,11,idx+1)
#    plt.plot(t,tdet)
#    plt.plot(t,fitform)   

##%% データ3(だが、時定数を固定する)
#fitdata4=[]
#plt.figure(4)
#
##Gap条件
#gapcond = ["Gap070","Gap072","Gap074","Gap076","Gap078","Gap080","Gap082","Gap084","Gap086","Gap088","Gap090"]
#
##時定数をフィッティング条件
#taulist = np.array(fitdata3)[:,0][11:22]
#
#for idx,i in enumerate(templist3):
#    #データ展開
#    t  = i[:,0]
#    ir = i[:,1]
#    tdet = i[:,4]
#    tcomp = i[:,5]
#    
#    if gapcond[0] in filelist3[idx]:
#        tau=taulist[0]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[1] in filelist3[idx]:
#        tau=taulist[1]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[2] in filelist3[idx]: 
#        tau=taulist[2]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[3] in filelist3[idx]:  
#        tau=taulist[3]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[4] in filelist3[idx]: 
#        tau=taulist[4]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[5] in filelist3[idx]:  
#        tau=taulist[5]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[6] in filelist3[idx]:  
#        tau=taulist[6]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[7] in filelist3[idx]:  
#        tau=taulist[7]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[8] in filelist3[idx]:  
#        tau=taulist[8]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[9] in filelist3[idx]:  
#        tau=taulist[9]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,tau))
#
#    if gapcond[10] in filelist3[idx]:
#        tau=taulist[10]
#        opt = op.minimize(costfunc2,np.array([1,1]),method="Powell",args=(t,ir,tdet,taulist[10]))
#
#    gain=opt['x'][0]
#    lag=opt['x'][1]
#    print(gain)
#    #フィッティング波形
#    fitform = appro(t,ir,tdet,gain,tau,lag)
#    #オフセット
#    offset = np.average((ir - fitform)[-10:-1])#後ろから10個の平均
#    #温度概算
#    tdet_def = np.average(fitform[0:10])     #初期検知温度
#    tdet_last = np.average(fitform[-10:-1])  #最終検知温度
#    tcomp_def = np.average(tcomp[0:10])     #初期補償温度
#    tcomp_last = np.average(tcomp[-10:-1])     #最終補償温度   
#    #保存
#    fitdata4.append([tau,offset,tdet_def,tdet_last,tcomp_def,tcomp_last])
#    #プロット
#    plt.subplot(9,11,idx+1)
#    plt.plot(t,tdet)
#    plt.plot(t,fitform)   
#
#
##最適化

