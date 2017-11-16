# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:57:40 2016

@author: p000495138
"""

import pandas as pd
import numpy as np
import glob
import os

filename = "d09_10_SP変更16_強制ROM確認_ver183_不定形連続_低速_初期低温.txt"
savename = filename + "_res.CSV" #保存名
saveMTname = filename + "_MTres.CSV"
saveFeedname = filename + "_Feedres.CSV"

#ファイル読み出し
f=open(filename,"r")
data = f.readlines()
f.close

#del data[11577]
#del data[13906]
#del data[15351]
#del data[20891]
#del data[10069]

"""大きく抽出"""
temp_M = []
temp_T =[]
for ind,x in enumerate(data):
    #Mode(main/sub)を分割
    M = x.split("=")
    temp_M.append(M)
    #温度を分割
    T = x.split(" ")
    temp_T.append(T)

"""データ１．温度/dutyなど"""
data1=[]
fusstop_flag = 0
cpm_flag = 0
for ind,x in enumerate(data):
    
    #強制停止を確認する
    if "FusPrtForceStopStart" in x:
        fusstop_flag = 1
    if "FusPrtForceStopFinsh" in x:
        fusstop_flag = 0
    if "FusPrtForceStopStart" in x:
        fusstop_flag = 1
        
    #CPMダウン
    if "CpmChg-0" in x:
        cpm_flag = 0
    if "CpmChg-1" in x:
        cpm_flag = 1
    if "CpmChg-2" in x:
        cpm_flag = 2
    if "CpmChg-3" in x:
        cpm_flag = 3
        
    key = "Mode(main / sub) "
    if key in temp_M[ind]:
        time_stamp  = int(temp_T[ind+1][0])/1000
        cen_tar     = temp_T[ind+1][10]
        cen_cur     = temp_T[ind+1][6]
        cen_duty    = temp_T[ind+1][14]
        end_tar     = temp_T[ind+2][12]
        end_cur     = temp_T[ind+2][8]
        end_duty    = temp_T[ind+2][16]
        if "Now" in end_duty :
            end_duty = cen_duty
        mode_main   = temp_M[ind][1].split("/")[0].split(" ")[1]        
        mode_sub    = temp_M[ind][1].split("/")[1].split(" ")[1]
        fus_stop    = fusstop_flag
        cpm         = cpm_flag
        data1.append([time_stamp,cen_tar,cen_cur,cen_duty,end_tar,end_cur,end_duty,mode_main,mode_sub,fus_stop,cpm,ind])

#アレイ化
data1_1     = np.float16(np.array(data1))
time_stamp  = data1_1[:,0]
cen_tar     = data1_1[:,1]
cen_cur     = data1_1[:,2]
cen_duty    = data1_1[:,3]
end_tar     = data1_1[:,4]
end_cur     = data1_1[:,5]
end_duty    = data1_1[:,6]
mode_main   = data1_1[:,7]
mode_sub    = data1_1[:,8]
fus_stop    = data1_1[:,9]
cpm         = data1_1[:,10]
ind1        = data1_1[:,11]

#タイムスタンプ修正＆時刻割当
t=[0]
count = 0
timestep  = np.diff(time_stamp) 
for (ind,x) in enumerate(timestep):
    if x>0:
        count = count + x
    else:
        count = count + timestep[ind-1]
    t.append(count)
t=np.array(t)
data1_1[:,0]=t

"""データ2．モータ"""
data2=[]
a=[]
MTdict = {"MainMT[1]spd[0]":178,"MainMT[1]spd[1]":160,"MainMT[1]spd[2]":130,"MainMT[1]spd[3]":90}
for ind,x in enumerate(data):
    if "MainMT[1]" in x:
        #時刻は、ind1のうち、indより小さい最大のものを取得する
        index1      = max(ind1[ind1<ind])
        a.append(index1)
        index2      = np.where(ind1==index1)
        index3      = index2[0][0] #タプルから数値を取り出す
        t2          = t[index3]
        mtspd       = MTdict[x.split()[0]]#splitで引数無しだと改行除去される        
        end_cur2    = end_cur[index3]
        data2.append([t2,mtspd,end_cur2])
data2_1        = np.float16(np.array(data2))
t2             = data2_1[:,0]
mtspd          = data2_1[:,1]    
end_cur2       = data2_1[:,1]    

"""データ3．給紙"""
data3=[]
for ind,x in enumerate(data):
    if "PAP:FeedStart" in x:
        index1   = max(ind1[ind1<ind])
        index2   = np.where(ind1==index1)   
        index3      = index2[0][0] #タプルから数値を取り出す        
        t3       = t[index3]
        feed     = x.split()[0] #splitで引数無しだと改行除去される
        if str(0) in feed:
            feed = 0
        else:
            feed = 1
        end_cur3 = end_cur[index3]
        data3.append([t3,feed,end_cur3])
data3_1     = np.float16(np.array(data3))
t3          = data3_1[:,0]
feed        = data3_1[:,1]    
end_cur3    = data3_1[:,2]


data_legend = ["sec","cen_tar","cen_cur","cen_duty","end_tar","end_cur","end_duty","Mode_main","Mode_sub","fus_stop","cpm","ind"]

#データフレーム化と保存
save_data = pd.DataFrame(np.array(data1_1))
save_data.columns = data_legend        
save_data.to_csv(savename,index=False)

MainMT_data = pd.DataFrame(data2_1)
#MainMT_data.to_csv(saveMTname,index=False)

Feed_data = pd.DataFrame(data3_1)
#Feed_data.to_csv(saveFeedname,index=False)
