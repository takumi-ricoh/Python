# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:14:30 2017

@author: p000495138
"""

from scipy import optimize
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close("all")
#%%calcfunction
def calc(v,tdie,S0=1.13982E-13,B0=-1.43386E-5,B1=4.33569E-5,B2=-1.69223E-6,A1=0,A2=0,C=0):
    s = S0*(1+A1*(tdie-25)+A2*((tdie-25)**2))
    vos = B0 + B1*(tdie-25) + B2*((tdie-25)**2)
    fvobj = (v/10**6-vos) + C*(v/10**6-vos)**2
    tdet_K1 =(tdie+273.15)**4 + fvobj/s
    if (tdet_K1<0).any():
        tdet_K2 = tdet_K1*0
    else:    
        tdet_K2 =( tdet_K1 )**(1/4)
    tdet_C = tdet_K2 - 273.15
    return tdet_C

#%%read function
def readdata(file):
    data=[]
    with open(file,"r") as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    data = pd.DataFrame(data[1:],dtype=float,columns=["microV","Tdie_C","IR_C"])
    data.median()
    return data

#%% class optimize
class Opt:
    def __init__(self,data):
        #制約条件(min,max)
        self.data = data
        bounds_S0=tuple(np.array([2.98E-17, 2.98E-13])*1E13)
        bounds_B0=tuple(np.array([-5.12E-3, 5.12E-3])*1E3)
        bounds_B1=tuple(np.array([-2.00E-5, 2.00E-5])*1E5)
        bounds_B2=tuple(np.array([-3.12E-7, 3.12E-7])*1E7)
        bounds_A1=tuple(np.array([-1.25E-1, 1.25E-1])*1E1)
        bounds_A2=tuple(np.array([-1.90E-3, 1.90E-3])*1E3)
        bounds_C=tuple(np.array([-9.77E+1, 9.77E+1])*1E-1)
        self.bounds=(bounds_S0,bounds_B0,bounds_B1,bounds_B2,bounds_A1,bounds_A2,bounds_C)

        #データ
    def cost(self,x1,data):
        #最適化変数(スケーリングが重要!!)
        S0 = x1[0]/1E13
        B0 = x1[1]/1E3
        B1 = x1[2]/1E5
        B2 = x1[3]/1E7
        A1 = x1[4]/1E1
        A2 = x1[5]/1E3
        C  = x1[6]/1E-1
        #データ
        v    = np.array(data["microV"])
        tdie = np.array(data["Tdie_C"])
        tref = np.array(data["IR_C"])
        #最適化                
        h = calc(v,tdie,S0,B0,B1,B2,A1,A2,C)
        err = h - tref
        L = np.sum(err**2)
        return L

    def opt(self,data,method="TNC",bounds=None):
        self.method = method
        if bounds==True:
            bounds=bounds
        self.opt = optimize.minimize(self.cost, [1,0,0,0,0,0,0],method=method,args=(data),tol=1e-5,bounds=self.bounds)
        self.S0 = self.opt["x"][0]/1E13
        self.B0 = self.opt["x"][1]/1E3
        self.B1 = self.opt["x"][2]/1E5
        self.B2 = self.opt["x"][3]/1E7
        self.A1 = self.opt["x"][4]/1E1
        self.A2 = self.opt["x"][5]/1E3
        self.C  = self.opt["x"][6]/1E-1

    def set_manual(self,cof):
        self.S0 = cof[0]
        self.B0 = cof[1]
        self.B1 = cof[2]
        self.B2 = cof[3]
        self.A1 = cof[4]
        self.A2 = cof[5]
        self.C  = cof[6]
        
        S0a = cof[0]*1E13
        B0a = cof[1]*1E3
        B1a = cof[2]*1E5
        B2a = cof[3]*1E7
        A1a = cof[4]*1E1
        A2a = cof[5]*1E3
        Ca  = cof[6]*1E-1
        self.opt = pd.DataFrame([S0a,B0a,B1a,B2a,A1a,A2a,Ca],columns=["x"])

#%%read
calibfile = "TMP007_calibdata_170425.csv"
validfile = "checkdata1.csv"

calibdata = readdata(calibfile)
validdata = readdata(validfile)

#%%optimizer
"""最適化"""
methods=["Nelder-Mead","Powell","CG","BFGS","L-BFGS-B","TNC","SLSQP"]

f = Opt(calibdata)
f.opt(f.data,method=methods[6],bounds=True)

#EaxyCal手動設定
cof = [1.13982E-13,-1.43386E-5,4.33569E-5,-1.69223E-6,0,0,0,0,0] #普通の
#cof = [1.235E-13  ,0          ,1.52E-5   ,-3E-7      ,0,0,0,0,0] #sweepbased
#f.set_manual(cof)

#%%精度のチェック
"""学習データ"""
h1 = calc(calibdata["microV"],calibdata["Tdie_C"],f.S0,f.B0,f.B1,f.B2,f.A1,f.A2,f.C)
calibdata["pred"] = h1
calibdata["err"] = calibdata["pred"] - calibdata["IR_C"]

"""検証データ"""
h2 = calc(validdata["microV"],validdata["Tdie_C"],f.S0,f.B0,f.B1,f.B2,f.A1,f.A2,f.C)
validdata["pred"] = h2
validdata["err"] = validdata["pred"] - validdata["IR_C"]

"電圧上下限"
vlim = np.zeros([3000,2])
vlim[:,0]=5.12*1000
vlim[:,1]=-5.12*1000

"""plot"""
fig1, axes = plt.subplots(nrows=2,ncols=2)
calibdata.plot(y=["IR_C","pred"],ax=axes[0,0],grid=True,title="training")
calibdata.plot(y="err",ax=axes[1,0],grid=True,title="trainerr",ylim=[-10,10])
validdata.plot(y=["IR_C","pred"],ax=axes[0,1],grid=True,title="validation")
validdata.plot(y="err",ax=axes[1,1],grid=True,title="validerr",ylim=[-10,10])
plt.tight_layout()

#%% MinMax check
"""係数の最大最小チェック"""
fig2, axes2 = plt.subplots()
plt.plot(f.bounds,)
plt.plot(f.opt["x"])
plt.ylim([-12,12])
plt.grid(True)
plt.legend(["lower_limit","upper_limit","coeff"])

#%% 電圧のチェック
"""電圧の最大チェック"""
plt.figure(3)
plt.subplot(121)
plt.plot(np.array(calibdata["microV"]))
plt.plot(vlim)
plt.legend(["volt","upperlim","lowerlim"])
plt.grid(True)
plt.title("training")

plt.subplot(122)
plt.plot(np.array(validdata["microV"]))
plt.plot(vlim)
plt.legend(["volt","upperlim","lowerlim"])
plt.grid(True)
plt.title("validation")


