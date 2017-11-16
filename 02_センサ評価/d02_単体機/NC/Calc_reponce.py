# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 10:22:55 2016

@author: p000495138
"""
"""
1.実温度から想定されるセンサ応答を計算する
2.初期温度毎に誤差を計算する
"""
from progressbar import ProgressBar , Percentage, Bar #進捗バー

import Parts_ReadData as rd
import Parts_DataProcess as dp
import Parts_CalcTemp as ct
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.interpolate as interp

"""関数"""
#検知電圧計算
def calc_vdif(tdet,tcomp,Vdif_table,Tcomp_table,Tdet_table):

    #初期化
    Vdif_cand = []
    row_size,col_size     = Vdif_table.shape
    
    #step1 1列毎に検知電圧テーブルの候補を出す
    for i in range(col_size):
        fc   = interp.interp1d(Tcomp_table,Vdif_table[:,i])
        temp = fc(tcomp)               
        Vdif_cand.append(temp)

    #step2　検知電圧候補 vs 検知温度のマッピング
    ft = interp.interp1d(Tdet_table,Vdif_cand) #                    
  
#    print([i,tdet])
    #step3 検知温度の計算
    vdet = ft(tdet)
#    vdet.append( ft(tdet) )    
    return vdet

#補償電圧計算
def calc_vcomp(tcomp,Vcomp_table,Tcomp_table):
    #step1 補償→補償温度のマッピング
    fc = interp.interp1d(Tcomp_table,Vcomp_table)
    #step2 温度計算
    vcomp = fc(tcomp)
    return vcomp

"""クラス"""
class Resp_Est():
    def __init__(self):#準備
        os.chdir(r"F:\03 NC標準計測器\p01 NCセンサ計算用マクロ")
        self.data      = np.loadtxt('data.csv')#実温度データ
        #self.Tcomp_est = self.data[0:60].mean() #補償温度推定値
        table_data = rd.table_dialog() #テーブル読み出し
        self.Table = rd.DefTableData(table_data) #テーブル定義
                
    def res_est(self,initial,tau,lag):#実行 
    
        self.shifted = self.shift_temp(self.data, initial) #初期温度修正
        #print("initial")
        #print(initial)
        #print("shifted")
        #print(shifted)
        
        #もし495を超えていたら495にする。
        self.shifted[self.shifted>495] = 495
#        print(len(self.data))
#        print(len(shifted))
    
        tau = tau
        lag = lag

            
        if initial <=125:
            self.Tcomp_est = initial 
            
        else:
            self.Tcomp_est = 125

        #step1：実温度　→　理想センサ応答(電圧)
        Vdif_est  = self.calc_Vdif(self.shifted)
        vcomp_est = calc_vcomp(self.Tcomp_est,self.Table.Vcomp_table,self.Table.Tcomp_table)
        #print("Vdif_est")
        #print(Vdif_est)
        #print("vcomp_est")
        #print(vcomp_est)
  
        #検算     
        #print("Tdet_est2")
        #Tdet_est2 = self.calc_Tdet(Vdif_est)
        #print(Tdet_est2)
        
        #step2：理想センサ応答 → 遅れ応答(電圧)
        Vdif_delay  = self.calc_delay(Vdif_est, tau, lag)        
        
        #step3：遅れ応答(電圧) → 遅れ応答(温度)
        Tdet_est  = self.calc_Tdet(Vdif_delay)
        #print("Tdetest")
        #print(Tdet_est)

        return Tdet_est

    def calc_err(self,T, Tref, thresh):
    
        """メモ
        補償温度＞対象温度の計算がそもそもできない。
        
        
        """
        err_array     = T - Tref
        #print("err_array")
        #print(err_array)
        #print("T")
        #print(T)
        #print("Tref")
        #print(Tref)
        
        if (np.max(Tref) - Tref[T > thresh][0]) > 10: #NC遮断時に対象温度が飽和していないかのチェック
            #飽和してなければ普通に誤差を計算
            err_point = np.abs(err_array[T > thresh][0])
        else:
            #飽和してたら-10にする。        
            err_point = -10
        
        return err_point

        
    "ライブラリ関数"
    #温度 → 電圧　換算 (逆算は特殊なので特別に)
    def calc_Vdif(self, data):  
        Vdif_Est = np.zeros_like(data) #dataと同じ要素の0配列で初期化
        for i in range(len(data)):
            Vdif_Est[i] = calc_vdif(data[i],self.Tcomp_est, self.Table.Vdif_table,self.Table.Tcomp_table,self.Table.Tdet_table)
        return Vdif_Est

    #電圧 → 温度　換算
    def calc_Tdet(self, Vdif_est):
        ctclass = ct.Calc_Temp(Vdif_est, 0, self.Table.Vdif_table, self.Table.Vcomp_table, self.Table.Tdet_table, self.Table.Tcomp_table)
        ctclass.Tcomp = np.ones(len(Vdif_est)) * self.Tcomp_est #ベクトル化同じものを並べる
        Tdet_Est = ctclass.calc_Tdet_byTcomp()
        return Tdet_Est

    #初期温度をinitialにする
    def shift_temp(self,data,initial):
        shift_data = data - (np.average(data[0:10]) - initial)
        return shift_data

    #遅れを計算する
    def calc_delay(self,data,tau,lag):
        temp1  = dp.primary_delay(data, 5, tau)
        temp2  = dp.lag(temp1, 5, lag)
        return temp2
        
        
"""計算内容"""
if __name__ ==  '__main__':
    print('実行')    

#芝浦
    tau = 870 #ms
    lag = 120  #ms
    Shiba = Resp_Est() 
    result = []
    #進捗
    progress=0
    p1=ProgressBar(sidgets=[Percentage(),Bar()], maxval=100).start()   
    myrange = np.arange(5,230,5)
    for i in myrange:#初期温度水準
        #進捗
        progress=progress + 100*1/(len(myrange)+1)
        p1.update(progress)
        #計算
        Est_temp = Shiba.res_est(i, tau, lag)
        Err = Shiba.calc_err(Est_temp, Shiba.shifted, 250)
        result.append([i,Err])
        #波形保存
        if i==100:
            np.savetxt('ShibaEst.csv',Est_temp,fmt="%0.3f",delimiter=",")    
    Shiba_res = np.array(result)
    np.savetxt('Shiba.csv',Shiba_res,fmt="%0.3f",delimiter=",")
    p1.finish()

#芝浦NEw
    tau = 470 #ms
    lag = 50  #ms
    ShibaNew = Resp_Est() 
    result = []
    #進捗
    progress=0
    p2=ProgressBar(sidgets=[Percentage(),Bar()], maxval=100).start()
    myrange = np.arange(5,230,5)
    for i in myrange:#初期温度水準
        #進捗
        progress=progress + 100*1/(len(myrange)+1)
        p3.update(progress)
        #計算
        Est_temp = ShibaNew.res_est(i, tau, lag)
        Err = ShibaNew.calc_err(Est_temp, ShibaNew.shifted, 250)
        result.append([i,Err])
        #波形保存
        if i==100:
            np.savetxt('ShibaNewEst.csv',Est_temp,fmt="%0.3f",delimiter=",")    
    ShibaNew_res = np.array(result)
    np.savetxt('ShibaNew.csv',ShibaNew_res,fmt="%0.3f",delimiter=",")
    p2.finish()

#三菱
    tau = 525 #ms
    lag = 39  #ms
    Mitsu = Resp_Est() 
    result = []
    #進捗
    progress=0
    p3=ProgressBar(sidgets=[Percentage(),Bar()], maxval=100).start()   
    myrange = np.arange(5,230,5)
    for i in myrange:#初期温度水準
        #進捗
        progress=progress + 100*1/(len(myrange)+1)
        p3.update(progress)
        #計算
        Est_temp = Mitsu.res_est(i, tau, lag)
        Err = Mitsu.calc_err(Est_temp, Mitsu.shifted, 250)
        result.append([i,Err])
        #波形保存
        if i==100:
            np.savetxt('MitsuEst.csv',Est_temp,fmt="%0.3f",delimiter=",")  
    Mitsu_res = np.array(result)
    np.savetxt('Mitsu.csv',Mitsu_res,fmt="%0.3f",delimiter=",")    
    p3.finish()




#step1：実温度→理想センサ応答(電圧)

#step2：理想センサ応答 → 遅れ応答(電圧)

#step3：遅れ応答(電圧) → 遅れ応答(温度)




#
#class Calc():
#    def __init__(self,tau,lag):
#        self.tau = tau
#        self.lag = lag
#        self.initial = np.arange(0,200,5)
#        self.data = np.loadtxt("data.csv")
#        self.t=np.linspace(0,0.005*len(self.data),len(self.data))
#
#        result1=[]
#        result2=[]
#
#        for i in self.initial:
#            data2 = self.shift_temp(self.data,i)            
#            temp1  = dp.primary_delay(data2, 5, self.tau)
#            temp2  = dp.lag(temp1, 5, lag)
#            err1    = temp2 - data2
#            err2    = np.abs(err1[temp2 > 250][0])
#            data3   = data2[temp2 > 250][0] - np.max(data2)
#            result1.append(err2)
#            result2.append(data3)            
#       
#        self.result = [result1,result2]
#             
#    def shift_temp(self,data,initial):
#        shift_data = data - (np.average(data[0:10]) - initial)
#        return shift_data
#
#shiba    = Calc(860,120)
#shibanew = Calc(460,50)
#mitsu    = Calc(620,20)
#nok       = Calc(130,30)
#
#shiba_err    = shiba.result
#shibanew_err = shibanew.result
#mitsu_err    = mitsu.result
#nok_err      = nok.result

"""
個別に計算する場合
class Calc():
    def __init__(self,tau,lag):
        self.data = np.loadtxt("data.csv")
        self.t=np.linspace(0,0.005*len(self.data),len(self.data))
        res1 = dp.primary_delay(self.data,5,tau)
        self.res2 = dp.lag(res1,5,lag)
        self.err  = self.res2 - self.data

shiba    = Calc(860,120)
shibanew = Calc(460,50)
mitsu    = Calc(620,20)
nok       = Calc(130,30)

plt.subplot(211)
plt.title('response')
plt.plot(shiba.t,shiba.data,'k')
plt.plot(shiba.t,shiba.res2,'b')
plt.plot(shibanew.t,shibanew.res2,'g')
plt.plot(mitsu.t,mitsu.res2,'darkred')
plt.plot(nok.t,nok.res2,'b--')
plt.legend(['data','shiba','shibanew','mitsu','nok'])
plt.xlabel('sec')
plt.ylabel('deg')
plt.grid(True)

plt.subplot(212)
plt.title('error')
plt.plot(shiba.t,shiba.err,'b')
plt.plot(shibanew.t,shibanew.err,'g')
plt.plot(mitsu.t,mitsu.err,'darkred')
plt.plot(nok.t,nok.err,'b--')
plt.legend(['data','shiba','shibanew','mitsu','nok'])
plt.xlabel('sec')
plt.ylabel('deg')
plt.grid(True)

#250を超えたときの温度
T1 = shiba.err[shiba.res2>250][0]
T2 = shibanew.err[shibanew.res2>250][0]
T3 = mitsu.err[mitsu.res2>250][0]
T4 = nok.err[nok.res2>250][0]
print(T1)
print(T2)
print(T3)
print(T4)
"""