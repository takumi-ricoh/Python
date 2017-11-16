# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 14:17:52 2016

@author: p000495138
"""

"""
実行ファイル
機能：複数データ毎に平均温度(or 電圧)を計算し、csv出力
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

#実行
Vdet_list=[]
Vcomp_list=[]
Tdet_list=[]
Tcomp_list=[]
for i in range(file_num):
    #ファイル数だけ読み出し
    file  = da.read_expdata(filelist_csv[i])#読み出し
    exp   = da.DefExpData(file)       #データ定義
    table = da.DefTableData(table_data)

    #電圧換算
    Vdet  = exp.Vdet
    Vcomp = exp.Vcomp
    
    #温度換算
#    Tdet  = ca.calc_tdet(exp.Vdet,exp.Vcomp,table.Vdet_table,table.Vcomp_table,table.Tdet_table)
#    Tdet  = ca.calc_tdet_vdif(exp.Vdet,exp.Vcomp,table.Vdif_table,table.Vcomp_table,table.Tdet_table)
#    Tcomp = ca.calc_tcomp(exp.Vcomp,table.Vcomp_table,table.Tcomp_table)
    
    #平均値
    Vdet_ave   = np.average(Vdet)
    Vcomp_ave  = np.average(Vcomp)
#    Tdet_ave   = np.average(Tdet)
#    Tcomp_ave  = np.average(Tcomp)
    #list保存
#   Vdet_list.append(Vdet_ave)
    Vcomp_list.append(Vcomp_ave)        
#    Tdet_list.append(Tdet_ave)
#    Tcomp_list.append(Tcomp_ave)    

#保存
#save_data   = np.array([Tdet_list,Tcomp_list])
save_data   = np.array([Vdet_list,Vcomp_list])
save_legend = ['Tdet_ave','Tcomp_ave']
#save_legend = ['Vdet_ave','Vcomp_ave']
save_name   = "Average.CSV" #保存名
sa.save_csv(save_data,save_legend,save_name)
