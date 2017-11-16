# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 14:17:52 2016

@author: p000495138
"""

"""
実行ファイル
機能　：　2Dの実験条件の場合、複数データ毎に平均温度(or 電圧)を計算し、
　　　　　 実験条件の表に入れて、csv出力
"""

import os
import glob
import numpy as np

import Parts_ReadData as da
import Parts_CalcTemp as ca
import Parts_Save as sa


#ファイルリスト
#filedir      = os.chdir(r"D:\実験結果\03 NC標準計測器\d03 視野角(スリット)\02_TH08による計測\三菱従来_y方向2")
print("Select datadir")
filedir = os.chdir(da.getdirname())
filelist_csv = glob.glob('*.csv') 
file_num     = len(filelist_csv) #

#テーブル読み出し
table_data = da.table_dialog()

#角度計算
r       = 25/2
z_range = np.arange(31, 20, -1)
z_range = z_range #上書き       
y_range = np.array([5,3,1,0])
deg_list = np.zeros([len(z_range),len(y_range)])
for i in range(len(z_range)):
    for j in range(len(y_range)):
        deg_list[i,j] = np.rad2deg(np.arcsin(r/z_range[i]) - np.arctan(y_range[j]/z_range[i]))

#実行
Vdet_list=[]
Vcomp_list=[]
Tdet_list=[]
Tcomp_list=[]

for i in range(file_num):
    #ファイル数だけ読み出し
    file  = da.read_expdata(filelist_csv[i])#読み出し
    exp   = da.DefExpData(file)       #データ定義
    ta    = da.DefTableData(table_data)

    #電圧換算
    Vdif  = exp.Vdet
    Vcomp = exp.Vcomp
    
    #温度換算
    ft      = ca.Calc_Temp(Vdif, Vcomp, ta.Vdif_table, ta.Vcomp_table, ta.Tdet_table, ta.Tcomp_table)
    Tdet    = ft.calc_Tdet()
    Tcomp   = ft.calc_Tcomp()    
    
    #平均値
    Vdet_ave   = np.average(Vdif)
    Vcomp_ave  = np.average(Vcomp)
    Tdet_ave   = np.average(Tdet)
    Tcomp_ave  = np.average(Tcomp)
    #list保存
    Vdet_list.append(Vdet_ave)
    Vcomp_list.append(Vcomp_ave)        
    Tdet_list.append(Tdet_ave)
    Tcomp_list.append(Tcomp_ave)    


Tdet_list  = np.array(Tdet_list[0:]).reshape(11,4).T
Tcomp_list = np.array(Tcomp_list[0:]).reshape(11,4).T
Vdet_list  = np.array(Vdet_list[0:]).reshape(11,4).T
Vcomp_list = np.array(Vcomp_list[0:]).reshape(11,4).T

#保存
save_data   = np.r_[Tdet_list,Tcomp_list]
#save_data   = np.array([Vdet_list,Vcomp_list])
save_legend = ["res"]*8
#save_legend = ['Vdet_ave','Vcomp_ave']
save_name   = "Average.CSV" #保存名
sa.save_csv(save_data,save_legend,save_name)
