# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 14:17:52 2016

@author: p000495138
"""

"""
機能　：　通常の温度計算実行、データフォルダにcsvで保存
入力　：　
出力　：　
"""


import numpy as np
import os

import Parts_ReadData as da
import Parts_CalcTemp as ca
import Parts_Save as sa

os.chdir(r"F:\03 NC標準計測器\d01 補償温度\d02_250℃")

#実行
exp_mat,filename   = da.read_dialog()            #ファイル読み出し
table_mat = da.table_dialog()            #ファイル読み出し
ex        = da.DefExpData(exp_mat) #データ定義
ta        = da.DefTableData(table_mat) #データ定義

#Tdet  = ca.calc_tdet(ex.Vdet,ex.Vcomp,ta.Vdet_table,ta.Vcomp_table,ta.Tdet_table)
Tcomp = ca.calc_tcomp(ex.Vcomp,ta.Vcomp_table,ta.Tcomp_table)

#保存
#save_data   = np.array([ex.t,Tdet,Tcomp,ex.Vcc])
save_data   = np.array([ex.t,Tcomp])
#save_legend = ['t','Tdet','Tcomp','Vcc']
save_legend = ['t','Tcomp']
save_name   = filename + "_res.CSV" #保存名
sa.save_csv(save_data,save_legend,save_name)
