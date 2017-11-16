#################上NOK、下NOK#######

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:17:50 2016

@author: p000495138
"""

"""
実行ファイル
機能：サンプリング毎に温度換算し、csv出力する
"""

#インポート
import tkinter.filedialog as tkfd # ダイアログボックス
import pandas as pd #ファイルI/O
import os.path #パス設定
import numpy as np


"""【関数】"""

#ファイル名取得
def getname():
    fTyp=[('ファイル','*.csv')]
    iDir='D:\実験結果\03 NC標準計測器\d02 視野角\芝浦従来'; #初期ディレクトリ
    filename_full = tkfd.askopenfilename(filetypes=fTyp,initialdir=iDir)#フォルダ含む
    filename = os.path.basename(filename_full) #ファイル名のみ抽出
    return filename,filename_full

#ディレクトリ名取得
def getdirname():
    fTyp=[('ファイル','*.csv')]
    iDir='D:\実験結果\03 NC標準計測器\d02 視野角\芝浦従来'; #初期ディレクトリ
    dirname_full = tkfd.askdirectory(initialdir=iDir)#フォルダ含む
    dirname      = os.path.basename(dirname_full) #ディレクトリ名のみ抽出
    return dirname_full

#実験データ読み出し
def read_expdata(filename):       
    col_names = [ 'c{0:02d}'.format(i) for i in range(20) ]#そのままだとエラーになるので列数指定
    pd_data = pd.read_csv(filename,encoding = "ISO-8859-1",names=col_names);#Pandasでcsvを読む
    [size01,size02] = pd_data.shape #データサイズ取得
    num_data = pd_data.ix[63:(size01-4),'c02':'c05']     #数値部分の切り出し
    exp_data = num_data.as_matrix().astype(float) #array
    return exp_data
    del([pd_data,num_data])

#csvデータ読み出し
def read_csv(filename):       
    csvdata = np.loadtxt(filename,delimiter=",") 
    return csvdata
    
#RtoV
def r_to_v(r,rpu):
    vcc = 3.3
    v = vcc * r/(r+rpu)
    return v

#実験データのリードダイアログ    
def read_dialog():
    print("Select Exp data")
    filename, filename_full = getname()
    exp_data = read_expdata(filename)
    return exp_data,filename

#テーブルデータのリードダイアログ
def table_dialog():
    print("Select Table data")        
    tablename, tablename_full =getname()    #ファイル名&フルパス
    table_data = read_csv(tablename_full)   #リードはフルパスで行う
    return table_data

"""【クラス】"""

class DefExpData:       #データ定義
    def __init__(self,exp_data):
        self.exp_data  = exp_data
        self.legend_data()

    def legend_data(self):
        size = len(self.exp_data)
        self.t                = np.linspace(0.0,size*1.0,size)
        self.Vdet             = self.exp_data[:,0]; #検知
        self.Vcomp            = self.exp_data[:,1]; #補償
        self.Vshutter         = self.exp_data[:,2]; #シャッター
#        self.Vcc              = self.exp_data[:,2]; #
        self.Vthermo          = self.exp_data[:,3]; #放射温度計

class DefTableData:       #データ定義
    def __init__(self,table_data):
        self.table_data  = table_data
        self.legend_Rtable()

        #抵抗 → 電圧変換
        self.Vcomp_table = r_to_v(self.Rcomp_table, 100)
        self.Vdet_table  = r_to_v(self.Rdet_table, 100)     
        
        Vcomp_table2 = self.Vcomp_table.reshape(len(self.Vcomp_table),1) @ np.ones([1,self.Vdet_table.shape[1]])
        self.Vdif_table  = (Vcomp_table2 - self.Vdet_table)*1000

    def legend_Rtable(self):
        self.Rcomp_table            = self.table_data[1:,1 ]; #ニップ前\
        self.Tcomp_table            = self.table_data[1:,0 ]; #ニップ前
        self.Rdet_table             = self.table_data[1:,2:]; #ニップ前\
        self.Tdet_table             = self.table_data[0 ,2:]; #ニップ前\  

