# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:57:40 2016

@author: p000495138
"""

import pandas as pd
import numpy as np
import glob
import os

filename = "d05_Chimay50ppm_LL_マイペHH調湿_ガイド板無し_非TEC_50枚連続.txt"
savename = filename + "_res.CSV" #保存名

#ファイル読み出し
data = []
f=open(filename,"rb")
for idx,i in enumerate(f):
    try:
        data.append(i.decode("cp932"))
    except:
        pass
f.close()

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
for ind,x in enumerate(data):
    
    key = "main/sub"
    if key in temp_M[ind]:
        time_stamp  = int(temp_T[ind+1][0])/1000
        cen_tar     = temp_T[ind+1][6]
        cen_cur     = temp_T[ind+1][4]
        cen_duty    = temp_T[ind+1][8]
        end_tar     = temp_T[ind+2][6]
        end_cur     = temp_T[ind+2][4]
        end_duty    = temp_T[ind+2][8]
        if "Now" in end_duty :
            end_duty = cen_duty
        mode_main   = temp_M[ind][1].split("/")[0]#.split(" ")[1]        
        mode_sub    = temp_M[ind][1].split("/")[1]#.split(" ")[1]
        data1.append([time_stamp,cen_tar,cen_cur,cen_duty,end_tar,end_cur,end_duty,mode_main,mode_sub,ind])

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
ind         = data1_1[:,9]

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

data_legend = ["sec","cen_tar","cen_cur","cen_duty","end_tar","end_cur","end_duty","Mode_main","Mode_sub","ind"]

#データフレーム化と保存
save_data = pd.DataFrame(np.array(data1_1))
save_data.columns = data_legend        
save_data.to_csv(savename,index=False)
