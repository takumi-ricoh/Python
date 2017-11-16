#################上NOK、下NOK#######

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:17:50 2016

@author: p000495138
"""

#インポート
import tkinter.filedialog as tkfd # ダイアログボックス
import pandas as pd #ファイルI/O
import os.path #パス設定
import numpy as np #行列計算
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt #グラフ
from scipy import hamming
from scipy.fftpack import fft

plt.close()

"""各種設定クラス"""
class Setting:
    from matplotlib.font_manager import FontProperties # 日本語を使うために必要
    fp = FontProperties(fname=r"C:\Windows\Fonts/HGRSMP.ttf") # フォントファイルの場所を指定

"""データファイル読み出しクラス"""
class ReadDataFile:
    
    #コンストラクタ
    def __init__(self):
        self.pickdata()
        print('pickOK')
        self.readfile()
        print('readOK')
        self.size1,self.size2 =self.exp_data1.shape
        print('sizeOK')
        self.namedata()
        print('namedataOK')

    #データの割り振り
    def namedata(self):
        self.t=np.linspace(0.0,self.size1*0.001,self.size1)
        self.Vcomp             = self.exp_data1[:,0]; #サーミスタ
        self.Vcc            = self.exp_data1[:,1]; #電源
        self.Vdet              = self.exp_data1[:,2]; #サーモパイル
        self.T               = self.exp_data1[:,3]; #スリーブ

    #ファイル選択
    def pickdata(self):
        fTyp=[('ファイル','*.csv')];
        iDir='E:/仕事/2016/05.SEMITEC NC型サーモパイル'; #初期ディレクトリ
        filename_full=tkfd.askopenfilename(filetypes=fTyp,initialdir=iDir)#フォルダ含む
        self.filename=os.path.basename(filename_full) #ファイル名のみ抽出

    #ファイル読み出し(pandas → numpy)
    def readfile(self):
        col_names = [ 'c{0:02d}'.format(i) for i in range(20) ]#そのままだとエラーになるので列数指定
        data0_pd = pd.read_csv(self.filename,encoding = "ISO-8859-1",names=col_names);#エンコード指定
        [size01,size02] = data0_pd.shape #データサイズ取得
        data1_pd=data0_pd.ix[52:(size01-4),'c02':'c17']#数値部分の切り出し
        self.exp_data1 = data1_pd.as_matrix().astype(float) #arra

#"""テーブル読み出しクラス"""
#class ReadNCTable:    
#    
#    #コンストラクタ
#    def __init__(self):
#        self.readtable()
#        
#    #テーブル読み込み
#    def readtable(self):
#        book = "抵抗テーブル.xlsx"
#        sheet=['Typ','Min','Max']
#        EXL = pd.ExcelFile(book)
#
#        self.Vdet_table_typ,self.Vcomp_table_typ,self.Tdet_table_typ,self.Tcomp_table_typ = self.pick(EXL.parse(sheet[0]))
#        self.Vdet_table_min,self.Vcomp_table_min,self.Tdet_table_min,self.Tcomp_table_min = self.pick(EXL.parse(sheet[1]))
#        self.Vdet_table_max,self.Vcomp_table_max,self.Tdet_table_max,self.Tcomp_table_max = self.pick(EXL.parse(sheet[2]))
#                
#    #テーブルデータの抽出関数
#    def pick(self,Data):
#        Dind = list(range(28)) #行リスト
#        Dcol = list(range(28)) #列リスト
#        Data.index = Dind#インデックスをつける
#        Data.column = Dcol#インデックスをつける
#        
#        Rdet  = np.array(Data.ix[3:,2:].fillna(-1000))#スライスし、nanを-1000に
#        Rcomp = np.array(Data.ix[3:,1].fillna(-1000))#スライスし、nanを-1000に    
#        Tdet  = np.array(Data.ix[1,2:].fillna(-1000))#スライスし、nanを-1000に    
#        Tcomp = np.array(Data.ix[3:,0].fillna(-1000))#スライスし、nanを-1000に        
#        
#        Rpdet  = 99.8;  
#        Rpcomp = 100.7;    
#        
#        Vdet  = 3.33 * Rdet /(Rdet+Rpdet)
#        Vcomp = 3.33 * Rcomp/(Rcomp+Rpcomp)    
#        
#        return Vdet,Vcomp,Tdet,Tcomp

#"""温度計算クラス"""
#class Tcalc:
#    
#    #コンストラクタ
#    def __init__(self,Vdet,Vcomp,Vdet_table,Vcomp_table,Tdet_table,Tcomp_table):
#        #変数セット
#        self.Vdet   = Vdet
#        self.Vcomp  = Vcomp
#        self.Vdet_table = Vdet_table
#        self.Vcomp_table = Vcomp_table
#        self.Tdet_table = Tdet_table
#        self.Tcomp_table = Tcomp_table    
#        #サイズセット
#        self.set_size()
#        #温度計算
#        self.calc_tdet()
#        self.calc_tcomp()
# 
#    #サイズなどのセット   
#    def set_size(self):
#        self.Table_col,self.Table_row = np.shape(self.Vdet_table)
#        self.expsize = len(self.Vdet)          
#
#    #検知温度計算
#    def calc_tdet(self):
#        
#        #step1 補償 → 検知のマッピング
#        fc=[]
#        for i in range(self.Table_row):
#            temp = interpolate.interp1d(self.Vcomp_table,self.Vdet_table[:,i])
#            fc.append(temp)
#    
#        #step2～step4 計測データ毎に温度換算
#        self.Tdet=[]
#    
#        for k in range(self.expsize):
#            #step2 検知出力候補を、補償を内挿して出す。
#            fd=[]
#            for i in range(self.Table_row): #1列ずつ
#                temp  = fc[i](self.Vcomp[k])
#                fd.append(temp) 
#            
#            #step3 検知→温度 のマッピング
#            ft = interpolate.interp1d(fd,self.Tdet_table) #
#                        
#            #step4 検知温度の計算
#            self.Tdet.append( ft(self.Vdet[k]) )
#        
#    #補償温度計算
#    def calc_tcomp(self):
#        #step1 補償→補償温度のマッピング
#        f = interpolate.interp1d(self.Vcomp_table,self.Tcomp_table)
#        
#        #step2 温度計算
#        self.Tcomp = f(self.Vcomp)

"""プロットクラス"""
class MyPlot:
    #コンストラクタ
    def __init__(self,data,Ttrue,calc):
        self.t      = data.t
        self.Ttrue  = Ttrue
        self.Tdet   = calc.Tdet
        self.Tcomp  = calc.Tcomp

    #プロット
    def myplot(self):
        
        self.fig1 = plt.figure() #インスタンス生成
        self.ax1 = self.fig1.add_subplot(221) 
        self.ax2 = self.fig1.add_subplot(223)  
        self.ax3 = self.fig1.add_subplot(222)  
        
        #プロット1
        self.ax1.plot(self.t,self.Ttrue)
        self.ax1.plot(self.t,self.Tdet)
        self.ax1.plot(self.t,self.Tcomp)
        self.setplot(self.ax1,'sec','deg',0,1000,20,350,['Ttrue','Tdet','Tcomp'])

        #プロット2
        self.ax2.plot(self.t,self.Tdet - self.Ttrue)    
        self.setplot(self.ax2,'sec','error',0,1000,-50,50,['Error'])
        
        #fig2 = plt.figure() #インスタンス
        #self.ax3 = fig2.add_subplot(111)
        self.ax3.plot(self.Tcomp, self.Tdet-self.Ttrue)
        self.setplot(self.ax3,'Tcomp','error',20,150,-50,50,['Error'])

    #プロットの設定
    def setplot(self,ax,xlab,ylab,xmin,xmax,ymin,ymax,legend):
        ax.grid(True)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)        
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymin,ymax)
        ax.legend(legend)


"""  実行部分（計算）  """
Setting() #初期セッティング
#table = ReadNCTable() #テーブル読み込み実行
data1  = ReadDataFile() #データ読み込み実行

t=data1.t
Vcomp = data1.Vcomp
Vdet = data1.Vdet
T = data1.T

#移動平均
s = int(0.02/0.001)
fil = np.ones(s)/s
Vdet2 = np.convolve(Vdet,fil)
Vdet3 = Vdet2[s-1::]

plt.subplot(211)
plt.plot(t,Vdet)
plt.plot(t,Vdet3)
plt.grid(True)

plt.subplot(212)
plt.plot(t,T)
plt.grid(True)


#FFT計算
Vdet4=Vdet[0:2**15]
plt.figure(2)
fs = 1000
L  = 10000 #窓関数幅
#窓関数
win = hamming(L)
#フーリエ変換
a=Vdet4*win
spectrum1    = fft(Vdet4 * win)
half_spectrum1 = abs(spectrum1[: L / 2 + 1])


#### 条件1(typ)
##インスタンス生成
#calc1 = Tcalc(data1.Vdet, data1.Vcomp, table.Vdet_table_typ, table.Vcomp_table_typ, table.Tdet_table_typ, table.Tcomp_table_typ) 
#Tdet1  = np.array(calc1.Tdet) #値読み出し
#Tcomp1 = np.array(calc1.Tcomp) #値読み出し


#"""  実行部分(プロット)  """
########プロット
##Ttrue1 = np.mean([data1.T1,data1.T2],axis=0) #値読み出し
#Ttrue1 = data1.T2 #値読み出し
#
#plot1 = MyPlot(data1,Ttrue1,calc1) #インスタンス生成
#plot1.myplot() #値セット
#
##追加
#plot1.ax4 = plot1.fig1.add_subplot(224)
#plot1.ax4.plot(data1.t,calc1.Tdet)
#plot1.ax4.plot(data1.t,calc2.Tdet)
#plot1.ax4.plot(data1.t,calc3.Tdet)
#plot1.ax4.grid(True)
#plot1.ax4.set_xlim(0,1000)
#plot1.ax4.set_ylim(20,350)
#plot1.ax4.set_xlabel('sec')
#plot1.ax4.set_ylabel('deg')
#plot1.ax4.legend(["typ","min","max"])

####---------結果の保存---------####
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