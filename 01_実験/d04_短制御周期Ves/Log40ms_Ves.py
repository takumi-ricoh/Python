# -*- coding: utf-8 -*-
"""
Created on Thu May 25 13:15:51 2017

@author: p000495138
"""

from PyParts import Log_Parts_Read as rd
from PyParts import Log_Parts_Read_Fuser_Ves as rdf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close()

"""データ分割関数"""
def setdata(file):
        datalist = rd.tolist(file)
        fuslist,tmplist,wavelist = rd.splitdata(datalist)
        return datalist,fuslist,tmplist,wavelist

"""データをまとめる関数"""
def mergedata(tmplist,wavelist):
    
        #温度ログをデータフレーム化
        thistmp = rdf.FuserTmp()
        tmppd = thistmp.toDataframe(tmplist)
        #順番入れ替え
        tmppd = tmppd[["sec","tar_cen","tmp_cen","tar_end","tmp_end",
        "tar_prs","tmp_prs_cen","tmp_prs_end",
        "duty_cen","duty_end",
        "state","mode","motor","FF"]]
    
        #半波ログをデータフレーム化
        thiswave = rdf.FuserWave()
        if len(wavelist) > 0:
            wavepd = thiswave.toDataframe(wavelist)
            wavepd = wavepd[["duty","preduty","flow","time_wave"]]

            #結合
            datapd = pd.concat([tmppd,wavepd],axis=1)

        else:
            datapd = tmppd

        #むだなところを除去
#        flg = np.ones_like(datapd["tar_cen"])
#        tar_diff = np.r_[0,np.diff(datapd["tar_cen"])]
#        for (ind,x) in enumerate(datapd["tar_cen"]):
#            if tar_diff[ind] < 1:
#                flg[ind] = 0
#            else:
#                break
#        datapd = datapd[flg==1]

        #タイムスタンプ修正＆時刻割当
        t=[0]
        count = 0
        timestep  = np.diff(datapd["sec"]) 
        for (ind,x) in enumerate(timestep):
            if x>0: #普通の場合
                count = count + x
            elif x<=0:
                count = count + timestep[ind-1]
            else: 
                count = count + timestep[ind-5]
                
            t.append(count)
        
        datapd["sec"] = t
        
#        #キー変換
#        keyA = {"0":"FFoff","1":"FFon"}
#        keyB = {"0":"制御無し","1":"非回転加熱","2":"回転加熱","3":"リロード後回転","4":"印刷前","5":"印刷中",
#                "6":"印刷後","7":"印刷準備","8":"Ready待機","11":"停止"}
#        keyC = {"1":"ON/OFF","2":"PID","3":"PID+FF"}
#        keyD = {1:"等速",3:"中速",4:"低速"}
#        
#        for idx,i in datapd.iterrows():
#            i["FF"] = keyA.get(i["FF"]) #getを使うと例外にならない
#            i["state"] = keyB.get(i["state"])
#            i["mode"] = keyC.get(i["mode"])
#            i["motor"] = keyD.get(i["motor"])
        
        return datapd
#%% 実行
"""実行"""
filelist=[
r"D:\実験結果\13 40ms(Vesta)\Data\d01_vesta_40ms_増量100_減量100_PID修正__普通紙A4T連続50枚×3回.txt",        
r"D:\実験結果\13 40ms(Vesta)\Data\d02_vesta_40ms_増量100_減量100_PID修正__普通紙A4T連続50枚×3回_FF-10per.txt",        
r"D:\実験結果\13 40ms(Vesta)\Data\d03_vesta_40ms_増量100_減量100_PID修正__普通紙A4T連続50枚×3回_FF-50per.txt",        
r"D:\実験結果\13 40ms(Vesta)\Data\d04_vesta_40ms_増量100_減量100_PID修正__普通紙A4T連続50枚×3回_FF-30per.txt",
r"D:\実験結果\13 40ms(Vesta)\Data\d04_vesta_40ms_増量100_減量100_PID修正__普通紙A4T連続50枚×3回_FF-30per_2回目.txt",        
r"D:\実験結果\13 40ms(Vesta)\Data\d05_vesta_def_普通紙A4T連続50枚×3回.txt",
r"D:\実験結果\13 40ms(Vesta)\Data\d06_vesta_40ms_増量100_減量100_PIDdef__普通紙A4T連続50枚×3回_FF-30per.txt",
     ]
file=filelist[4]
savename = file + "_res.csv"
#savename = file.split("_")[1] + "_res.csv"

#読み出し
datalist,fuslist,tmplist,wavelist = setdata(file)

#まとめる
datapd = mergedata(tmplist,wavelist)

#セーブ
#datapd.to_csv(savename)

#%% プロット
"""プロット"""
datapd["FF"]=datapd["FF"]*30
#datapd["dduty"] = datapd["duty"] - datapd["preduty"]
fig0 , ax0 = plt.subplots(nrows=2,ncols=1)
ax0[0].set_ylabel("℃")
#ax0[0,1].set_ylabel("℃")
ax0[1].set_ylabel("-")
#ax0[1,1].set_ylabel("%")
a=datapd.plot(x="sec",y=["tar_cen","tmp_cen"],ax=ax0[0],grid=True,ylim=[120,175],xlim=[0,800])
#b=datapd.plot(x="sec",y=["tar_end","tmp_end"],ax=ax0[0,1],grid=True,ylim=[20,200],xlim=[0,1000])
c=datapd.plot(x="sec",y=["duty_cen","FF"],ax=ax0[1],grid=True,xlim=[0,800])
#d=datapd.plot(x="sec",y=["dduty","flow"],ax=ax0[1,1],grid=True)
fig0.tight_layout()


fig1 , ax1 = plt.subplots(nrows=2,ncols=1)
ax1[0].set_ylabel("℃")
#ax0[0,1].set_ylabel("℃")
ax1[1].set_ylabel("-")
#ax0[1,1].set_ylabel("%")
a=datapd.plot(x="sec",y=["tar_cen","tmp_cen"],ax=ax1[0],grid=True,ylim=[130,170],xlim=[325,475])
#b=datapd.plot(x="sec",y=["tar_end","tmp_end"],ax=ax0[0,1],grid=True,ylim=[20,200],xlim=[0,1000])
c=datapd.plot(x="sec",y=["duty_cen","FF"],ax=ax1[1],grid=True,xlim=[325,475])
#d=datapd.plot(x="sec",y=["dduty","flow"],ax=ax0[1,1],grid=True)
fig1.tight_layout()