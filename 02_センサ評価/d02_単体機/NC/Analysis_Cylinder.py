# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 17:11:10 2016

@author: p000495138
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import Parts_ReadData as da
import Parts_CalcTemp as ca
import Parts_Save as sa
import Parts_DataProcess as dp
import Parts_Cylinder as cy

plt.close()

"""------------クラス定義------------"""
#スリット実験のデータ読み出し
class Slit():
        
    def __init__(self,filedir):
        
        self.sensor_slit_gap = 14 #mm
        self.move_range  = np.arange(0,22,0.5)        
        self.theta_range = np.rad2deg(np.arctan(self.move_range/self.sensor_slit_gap))
        
        os.chdir(filedir)
        filelist_csv = glob.glob('*.csv') 
        file_num     = len(filelist_csv) #        
        
        #実行
        self.Vdet_list=[]
        self.Vcomp_list=[]
        
        for i in range(file_num):
        #ファイル数だけ読み出し
            file  = da.read_expdata(filelist_csv[i])#読み出し
            exp   = da.DefExpData(file)       #データ定義
    
        #電圧換算
            Vdet  = exp.Vdet #実は差分
            Vcomp = exp.Vcomp
        
        #平均値
            Vdet_ave   = np.average(Vdet)
            Vcomp_ave  = np.average(Vcomp)
            
        #list保存
            self.Vdet_list.append(Vdet_ave)
            self.Vcomp_list.append(Vcomp_ave)
        
        #array保存
        self.Vdet_list_np = np.array(self.Vdet_list)

        #近似
        self.Vdet_hyp = dp.call_sigmoid(self.theta_range, self.Vdet_list_np[:-1])
        #正規化
        self.Vdet_hyp_norm = dp.normalize(self.Vdet_hyp)

        #積算
        self.Vdet_hyp_norm_sum = dp.sen_sum(self.Vdet_hyp_norm,len(self.Vdet_hyp_norm))
        #正規化(normalizeが使えないことに注意)
        self.Vdet_hyp_norm_sum_norm  = self.Vdet_hyp_norm_sum / np.max(self.Vdet_hyp_norm_sum)

        #片側見えてる想定
        self.Vdet_hyp_norm_sum2 = self.Vdet_hyp_norm_sum + self.Vdet_hyp_norm_sum[-1]
        #正規化(normalizeが使えないことに注意)
        self.Vdet_hyp_norm_sum2_norm  = self.Vdet_hyp_norm_sum2 / np.max(self.Vdet_hyp_norm_sum2)

#円筒にスリット形状を適用した場合の予測特性
class CalcCylinder():
        
    def __init__(self,data,z_range):
        self.Vdet_norm = data.Vdet_hyp_norm #Slitの結果を渡す
        
        self.r       = 15
        self.z_range = np.arange(30.5, 21, -1)
        self.z_range = z_range #上書き       
        self.y_range = np.array([7,5,3,1,0])
    
        self.data    = data

        gap, self.edge_plus, self.edge_minus = cy.calc_edge_ang(self.r, self.z_range, self.y_range)

        #角度単位
        self.edge_plus  = np.rad2deg(self.edge_plus)
        self.edge_minus = np.rad2deg(self.edge_minus)
        
        self.summery()        
        
    def summery(self):
        self.n_plus    = self.edge_plus.copy()
        self.n_minus   = self.edge_minus.copy()        
        self.sum_plus  = self.edge_plus.copy()
        self.sum_minus = self.edge_minus.copy()        
        self.sum_all   = self.edge_plus.copy()
        self.deg_list  = self.edge_plus.copy()        

        #積算値の計算
        for j in range(len(self.y_range)):
            for i in range(len(self.z_range)):
                
                #エッジより小さい範囲にある個数を決める
                self.n_plus[i,j]   = np.int(len(self.data.theta_range[self.data.theta_range < self.edge_plus[i,j]]))
                self.n_minus[i,j]  = np.int(len(self.data.theta_range[self.data.theta_range < self.edge_minus[i,j]]))
                
                #積算
                self.sum_plus[i,j]   = dp.sen_sum(self.Vdet_norm, np.int(self.n_plus[i,j]))[-1]
                self.sum_minus[i,j]  = dp.sen_sum(self.Vdet_norm, np.int(self.n_minus[i,j]))[-1]
                
                self.deg_list[i,j]   = np.rad2deg(np.arcsin(self.r/self.z_range[i]) - np.arctan(self.y_range[j]/self.z_range[i]))
        
        self.sum_all   = self.sum_plus + self.sum_minus                 
        
        #正規化(normalizeが使えないことに注意)
        self.sum_all_norm = self.sum_all / np.max(self.sum_all)

#温度推測クラス
class CalcCylinderTemp():
    def __init__(self,data_cal, data_exp):
        self.sum_all_norm = data_cal.sum_all_norm
        self.Vdet_ref   = data_exp.Vdet_list[0,9]
        self.Vcomp_ref  = data_exp.Vcomp_list[0,9]        
        
        self.Vdet_conv = self.sum_all_norm * self.Vdet_ref
        
        #初期化
        self.Tdet_list  = np.zeros(np.shape(self.sum_all_norm))
        self.Tcomp_list = np.zeros(np.shape(self.sum_all_norm))
    
        irange = np.shape(self.sum_all_norm)[0]
        jrange = np.shape(self.sum_all_norm)[1]        
    
        for i in range(irange):
            for j in range(jrange):
                self.Tdet_list[i,j]  = ca.calc_tdet_vdif([self.Vdet_conv[i,j]],[self.Vcomp_ref],table.Vdif_table,table.Vcomp_table,table.Tdet_table)
                self.Tcomp_list[i,j] = ca.calc_tcomp([self.Vcomp_ref],table.Vcomp_table,table.Tcomp_table)

#実際の円筒形状特性
class PipeExpData():
    def __init__(self):
        
         runfile('F:/03 NC標準計測器/p01 NCセンサ計算用マクロ/Run_PIPE.py', wdir='F:/03 NC標準計測器/p01 NCセンサ計算用マクロ')
         self.Vdet_list = Vdet_list        
         self.Vcomp_list = Vcomp_list                
         
         self.Vdet_list_norm  = self.Vdet_list / np.max(self.Vdet_list)
         self.Vcomp_list_norm = self.Vcomp_list / np.max(self.Vcomp_list)
         self.Vdet_list_norm  = self.Vdet_list_norm.T
         self.Vcomp_list_norm = self.Vcomp_list_norm.T

         self.Tdet_list  = Tdet_list        
         self.Tcomp_list = Tcomp_list
         self.Tdet_list  = self.Tdet_list.T
         self.Tcomp_list = self.Tcomp_list.T               
         
         self.deg_list = deg_list        
        
"""------------実行部分------------"""

#芝浦/芝浦New/三菱
data=[]
data.append(Slit(r"F:\03 NC標準計測器\d03 視野角(スリット)\02_TH08による計測\芝浦従来_y方向"))
data.append(Slit(r"F:\03 NC標準計測器\d03 視野角(スリット)\02_TH08による計測\芝浦New_y方向"))
data.append(Slit(r"F:\03 NC標準計測器\d03 視野角(スリット)\02_TH08による計測\三菱従来_y方向2"))

#芝浦/芝浦New/三菱 距離水準を入力のこと
calV=[]
calV.append(CalcCylinder(data[0], np.arange(30.5, 21, -1)))
calV.append(CalcCylinder(data[1], np.arange(30.5, 21, -1)))
calV.append(CalcCylinder(data[2], np.arange(30.5, 21, -1)))

#実測
exp_res=[]
calT=[]
exp_res.append(PipeExpData())
calT.append(CalcCylinderTemp(calV[0], exp_res[0]))

exp_res.append(PipeExpData())
calT.append(CalcCylinderTemp(calV[1], exp_res[1]))

exp_res.append(PipeExpData())
calT.append(CalcCylinderTemp(calV[2], exp_res[2]))

#calとexpの比較
for i in range(3):
    
    plt.figure(i)
    
    plt.subplot(2,2,1)
    plt.plot(calV[i].deg_list, calV[i].sum_all_norm,"-*")
    plt.grid(True)
    plt.xlabel('theta_minus[deg]')
    plt.ylabel('V[-]')
    plt.title('hyp_V')
    plt.ylim([0,1])
    
    plt.subplot(2,2,2)
    plt.plot(exp_res[i].deg_list, exp_res[i].Vdet_list_norm,"-*")
    plt.grid(True)
    plt.xlabel('theta_minus[deg]')
    plt.ylabel('V[-]')
    plt.title('exp_V')
    plt.ylim([0,1])
    
    plt.subplot(2,2,3)
    plt.plot(exp_res[i].deg_list, calT[i].Tdet_list,"-*")
    plt.grid(True)
    plt.xlabel('theta_minus[deg]')
    plt.ylabel('T')
    plt.title('hyp_T')
#    plt.ylim([145,170])
    
    plt.subplot(2,2,4)
    plt.plot(exp_res[i].deg_list, exp_res[i].Tdet_list,"-*")
    plt.grid(True)
    plt.xlabel('theta_minus[deg]')
    plt.ylabel('T')
    plt.title('exp_T')
#    plt.ylim([145,170])