#################上NOK、下NOK#######

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:17:50 2016

@author: p000495138
"""

##メモ
#中央6111/端部6112

#インポート
import tkinter
import tkinter.filedialog as tkfd # ダイアログボックス
import pandas as pd #ファイルI/O
import os.path #パス設定
import numpy as np #行列計算
from scipy.stats import norm #数値計算(正規分布近似用)
from scipy import signal,interpolate
import matplotlib.pyplot as plt #グラフ
import seaborn as sns #グラフ(見た目をリッチに)
import pickle #グラフ保存

####各種設定####
plt.close('all') #グラフを消す
sns.set_style("whitegrid") #seabornのセッティング
#日本語フォントの設定
from matplotlib.font_manager import FontProperties # 日本語を使うために必要
fp = FontProperties(fname=r"C:\Windows\Fonts/HGRSMP.ttf") # フォントファイルの場所を指定


####ファイル選択ダイアログ(tkinter)####
tk=tkinter.Tk()
tk.withdraw() #ショウウィンドウ

fTyp=[('ファイル','*.csv')];
iDir='C:/Users/p000495138/Desktop/サーモパイル実機評価/01_MetisC1_eDOM/02_日セラ_確認'; #初期ディレクトリ
filename_full=tkfd.askopenfilename(filetypes=fTyp,initialdir=iDir)#フォルダ含む
filename=os.path.basename(filename_full) #ファイル名のみ抽出


####ファイル読み出し(pandas → numpy)####
col_names = [ 'c{0:02d}'.format(i) for i in range(20) ]#そのままだとエラーになるので列数指定
data0_pd = pd.read_csv(filename,encoding = "ISO-8859-1",names=col_names);#エンコード指定
[size01,size02] = data0_pd.shape #データサイズ取得
data1_pd=data0_pd.ix[52:(size01-4),'c02':'c17']#数値部分の切り出し
exp_data1 = data1_pd.as_matrix().astype(float) #array型データ/かつ数値に変換
[size1,size2] = exp_data1.shape #データサイズ取得


#割当
dt = 0.005
t=np.linspace(0,size1*dt,size1) #時刻
data = exp_data1[:,0]           #ON/OFF信号
count=exp_data1[:,0].copy()*0       #カウンタ初期値

#カウンタ
for i in range(1,size1):
    if data[i]-data[i-1]>2:
        count[i]=count[i]        
    else:
#         None
        count[i]=count[i-1] + dt
#         None

#カウンタが最大となる時刻を抽出する。最大はsが0となる1個前
ind1=np.array(np.where(count==0)) #Numpy配列にする
ind2=ind1[:,1:] #ひとつ目の要素を削除
ind3=ind2-1 #一つ前の時刻
time_pick = t[ind3] #抽出
time_pick2 = time_pick - time_pick[0,0]

#クリップボードにコピーするためにlistにする
res_list = list(time_pick2[0,:])


#time_res = t[count==0]
#data_res = s[s==0]
#plt.plot(time_res, data_res,'-o')

        
#plt.plot(t,data,'-*')




#
#####---------結果の保存---------####
#writedata=np.array([t, Near_C1,   Near_C2,   Near_C, Tobj_C, Tamb_C, Tnok_C, T_NIP_F79,   T_NIP_F449,  T_NIP_F449*0,  T_Pres,\
#                       Near_E1,   Near_E1*0, Near_E, Tobj_E, Tamb_E, Tnok_E, T_NIP_F1065, T_NIP_F1250, T_NIP_F1435 ,  T_Pres,\
#                       Vcc]);
#writedata=writedata.T #転置                      
#writedata_pd = pd.DataFrame(writedata) #データフレーム化
#writedata_pd.columns= ['t','Near_C1','Near_C2','Near_C','Tobj_C','Tamb_C','Tnok_C','T_NIP_F79','T_NIP_F449','T_NIP_F449*0','T_Pres',\
#                     'Near_E1','-','Near_E','Tobj_E','Tamb_E','Tnok_E','T_NIP_F1065','T_NIP_F1250','T_NIP_F1435' ,'T_Pres',\
#                     'Vcc']; #データフレームの列に名前をつける
#
#writename = filename + "_res.CSV" #保存名
#writedata_pd.to_csv(writename); #ｃｓｖ保存