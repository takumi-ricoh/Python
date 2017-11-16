# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 10:43:30 2016

@author: p000495138
"""

"""
実行ファイル
機能　：　規定区間を抽出してcsv出力
"""

#import gc
import numpy as np
import os
import Parts_ReadData as da
import Parts_CalcTemp as ca
import Parts_Save as sa
import Parts_DataProcess as dp
import matplotlib.pyplot as plt
import glob

plt.close()
os.chdir(r"F:\03 NC標準計測器\d06 応答速度\d03_温度振り\温度振り")
filelist_csv = glob.glob('*.csv')

for (i,x) in enumerate(filelist_csv):
    print(i,x)

    #実験データ読み出し
    exp_mat = da.read_expdata(x)
    
    if i in [0,1,2,3]:
        table_data = da.read_csv(r"F:\03 NC標準計測器\p01 NCセンサ計算用マクロ\三菱マテリアルセンサver1.1_0℃から500℃版（Metis-C2_中央部）_最終_2.csv")  
    elif i in [4,5,6,7]:
        table_data = da.read_csv(r"F:\03 NC標準計測器\p01 NCセンサ計算用マクロ\芝浦_RD02_typ.csv")  
    elif i in [8,9,10,11]:
        table_data = da.read_csv(r"F:\03 NC標準計測器\p01 NCセンサ計算用マクロ\芝浦_RD01_typ.csv") 
    elif i in [12,13,14,15]:
        table_data = da.read_csv(r"F:\03 NC標準計測器\p01 NCセンサ計算用マクロ\三菱マテリアル_高応答(2015実装用テーブルより).csv")         
#    table_mat = da.DefTableData(table_data)  

    #データ定義
    ex = da.DefExpData(exp_mat)              
    ta = da.DefTableData(table_data)          
    Vdif       = ex.Vcomp - ex.Vdet
    Vdif_moave  = dp.move_average(Vdif,4)*1000

    #カットしてシャッター回数だけリスト化
    cut_data  = dp.cut(np.vstack([ex.Vshutter, Vdif_moave, ex.Vcomp]).T,ex.Vshutter,50,2000)

    #シャッター回数だけ電圧/温度をまとめる
    res_data = []
    for j in range(len(cut_data)): #j：シャッター　回数
         
        
        #対象温度計算
        ft      = ca.Calc_Temp(cut_data[j][:,1], cut_data[j][:,2], ta.Vdif_table, ta.Vcomp_table, ta.Tdet_table, ta.Tcomp_table)
        Tdet    = ft.calc_Tdet()
        Tcomp   = ft.calc_Tcomp()
        
        #正規化
        Shutter_norm = -dp.normalize(cut_data[j][:,0])*100+100#シャッター
        Vdif_norm    = dp.normalize(cut_data[j][:,1])*100#Vdif
        Tdet_norm    = dp.normalize(Tdet)*100
        Tcomp_norm   = dp.normalize(Tcomp)*100     
        
        res_data.append(np.c_[Shutter_norm, Vdif_norm, Tdet_norm, Tcomp])        
        
#        cut_data[j] = np.c_[cut_data[j], Tdet, Tcomp] #加える

    #平均値
    res_data_ave = np.average(res_data,axis=0)

    #保存
    save_data   = np.c_[res_data_ave].T
    save_legend = ['Shutter_norm' , 'Vdif_norm','Tdif_norm','Tcomp']
    save_name   = x + "_res.CSV" #保存名
    sa.save_csv(save_data,save_legend,save_name)

##プロット
#t = np.linspace(0,0.005*len(Vdif_norm[0]),len(Vdif_norm[0]))
#mylegend=[]
#for i in range(len(Vdif_norm)):
#    plt.plot(t,Vshutter_norm[i])
#    plt.plot(t,Vdif_norm[i])
#plt.grid(True)
#plt.xlabel("sec")
#plt.ylabel("output")

"""
#save_data   = np.array([Vshutter_ave,Vdif_ave])
save_legend = [["shutter"]+["Vdif"]*1][0]

save_name   = filename + "_res.CSV" #保存名
sa.save_csv(save_data,save_legend,save_name)
"""