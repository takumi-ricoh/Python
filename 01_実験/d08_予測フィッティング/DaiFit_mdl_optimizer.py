# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 09:48:31 2018

@author: p000495138
"""
from scipy import optimize
import numpy as np
from numba.decorators import jit
DROPFLG  = True

#%% ★★★　最適化すラス　★★★
class Optim():
    
    def __init__(self,datas,tar,c=()):
        self.datas    = datas
        self.c        = c
        self._set_anc()    
        self.tar      = tar
        self.init1    = [1, 5, 0]
        self.init2    = [10]
        self.costobjs = []
        
    def _set_anc(self):
        self.ancs = []
        for data in self.datas:
            real     = np.array(data["CLRtmp"])
            h        = np.array(data["CLRtmp"])
            sts      = np.array(data["stscounter"])
            NCmean   = np.array(data["NCmean"])
            flg      = np.array(data["flg"])
            dropcoef = np.array(data["dropcoef"])
            self.ancs.append([real,h,sts,NCmean,flg,dropcoef])

    #全部個別計算
    def calc_a(self):
        self.costobjs = []
        for anc in self.ancs:
            costobj_a = Cost(anc,self.tar,self.c)
            opt = optimize.minimize(costobj_a.cost, self.init1, method="Nelder-Mead",tol=1e-4)
            self.costobjs.append(costobj_a)

    #一部まとめて計算
    def calc_b(self):
        self.costobjs = []
        costobj_b = Cost2(self.ancs, self.tar,  self.init1, self.c)
        opt       = optimize.minimize(costobj_b.cost2, self.init2,method="Nelder-Mead",tol=1e-2)
        self.costobjs = costobj_b.costobjs
        
#%%誤差クラス
class Cost():

    #諸々の数値
    def __init__(self,anc,tar,cx=()):
        self.anc = anc
        self.tar = tar     
        self.cx  = cx
        self.real = self.anc[0]

        #インスタンス初期化
        self.calcobj = Hypo(anc)
            
    @jit
    def cost(self,coef):
    
            #係数展開
            self.a = 0.98 + coef[0]/100
            self.b = coef[1] + 1
    
            #上書きする場合
            if len(self.cx)>0:
                self.coefc = self.cx[0]
                
            else:
                #個別合わせ用
                self.coefc = coef[2]
                
            self.c = self.coefc/1000

    
            #予測値計算
            h = self.calcobj.hypo(coef[0], coef[1], self.coefc)
    
            #誤差計算
            L = self._cost(h)
            return L
    
    def set_coefc(self,cx):
        self.cx = cx
    
    
    def get_coef(self):
        return [self.a, self.b, self.c]
    
    @jit        
    def _cost(self,h):
            #★誤差1
            err = h - self.real
            L1  = sum(err**2)
    

#            #★誤差2(係数範囲1)
#            if self.tar[0] < self.b/(1-self.a) < self.tar[1]:
#                L2 = 0
#            else:
#                L2=L1*100
#            
#            #★誤差3(マイナス制限)
#            if min(err)>0:
#                L3 = 0
#            else:
#                L3=L1*1000                 
                
            L = L1 #+ L2 + L3           
            return L

#%%誤差クラス2
class Cost2():
    
    #諸々の数値
    def __init__(self,ancs,tar,init,cx=()):
        self.init = init
        self.costobjs = []
        self.cx=cx
        #インスタンス生成
        for idx,anc in enumerate(ancs):
            #余剰係数coefを初期化数値とする
            costobj = Cost(anc, tar, cx)
            self.costobjs.append(costobj)

    def cost2(self,coef):
        sum_err = 0
        
        for costobj in self.costobjs:
            #cを設定
            if len(self.cx)>0:
                coef = self.cx
            costobj.set_coefc((coef))
            #a,bを最適化
            opt = optimize.minimize(costobj.cost, self.init, method="Nelder-Mead")
            #誤差和
            sum_err += opt["fun"]
        
        print(sum_err)
        return sum_err

#%%予測クラス
class Hypo():
    #諸々の数値
    def __init__(self,anc):
        self.a = 0
        self.b = 0
        self.c = 0
        
        self.real     = anc[0]
        self.h        = anc[1]
        self.sts      = anc[2]
        self.NCmean   = anc[3]
        self.flg      = anc[4]
        self.dropcoef = anc[5]
            
    @jit
    def hypo(self,coef0,coef1,coef2):
        self.a = 0.98 + coef0/100
        self.b = coef1 + 1
        self.c = coef2/1000
        
        #高速化計算
        for idx,i in enumerate(self.h):
            if idx>0:           
                #もしstscounterが切り替わったら真値にする(=何もしない)
                if self.sts[idx] != self.sts[idx-1]:
                    continue
                 
                #基本計算
                self.h[idx] = self.a*self.h[idx-1] + self.b + self.c*self.NCmean[idx-1]
                
                #もしドロップ領域なら、、、
                if DROPFLG == True:
                    if self.flg[idx] == 3:
                        self.h[idx] = self.h[idx-1] + self.dropcoef[idx-1]           
        return self.h
