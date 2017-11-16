# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:33:25 2017

@author: p000495138
"""

import numpy as np
import math
import random
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

#ガウス分布に従う確率の計算
def gaussian(x, m, v): #平均m、分散v
    p = math.exp(-pow(x-m, 2)/(2*v)) / math.sqrt(2*math.pi*v)
    return p

#Eステップ
def e_step(xs, ms, vs, p):
    burden_rates=[]
    for x in xs:
        #pの割合で確率をミックスする
        d = (1-p)*gaussian(x,ms[0],vs[0]) + p*gaussian(x,ms[1],vs[1])
        n = p*gaussian(x,ms[1],vs[1])
        burden_rate = n/d #混合率?
        burden_rates.append(burden_rate)
    return burden_rates

#Mステップ
def m_step(xs,burden_rates):
    #step1
    d = sum([(1-r) for r in burden_rates]) #1-rを合算
    n = sum([(1-r)*x for x,r in zip(xs,burden_rates)]) #同じインデックスのxsとburden_ratesの組合せで計算
    mu1 = n/d #μ1
    
    n=sum([(1-r)*pow(x-mu1,2) for x,r in zip(xs,burden_rates)])
    var1 = n/d
    
    #step2
    d = sum(burden_rates) #1-rを合算
    n = sum([r*x for x,r in zip(xs,burden_rates)]) #同じインデックスのxsとburden_ratesの組合せで計算
    mu2 = n/d #μ2
    
    n=sum([(1-r)*pow(x-mu2,2) for x,r in zip(xs,burden_rates)])
    var2 = n/d
    
    N = len(xs)
    p = sum(burden_rates)/N
    
    return [mu1,mu2], [var1,var2], p

#対数尤度計算
def calc_log_likelihood(xs,ms,vs,p):
    s=0
    for x in xs:
        g1 = gaussian(x,ms[0],vs[0])
        g2 = gaussian(x,ms[1],vs[1]) 
        s += math.log((1-p)*g1 + p*g2)
    return s

#ヒストグラムをプロット
def draw_hist(xs,bins):
    plt.hist(xs, bins=bins, normed=True, alpha=0.5)
    
"""main"""

#1列目を読み込む
fp = open("faithful.txt")
data = []
for row in fp:
    data.append(float((row.split()[0])))
fp.close()

#mu,vs,pの初期値を設定
p=0.5
ms = [random.choice(data), random.choice(data)] #データからランダムに
vs = [np.var(data), np.var(data)] #データの分散そのまま
T = 50 #反復回数
ls = [] #対数尤度関数の計算結果

"""EM計算"""
for t in range(T):
    burden_rates = e_step(data, ms, vs, p)
    ms, vs, p = m_step(data, burden_rates)
    ls.append(calc_log_likelihood(data, ms, vs, p))
print("predict: mu1={0}, mu2={1}, v1={2}, v2={3}, p={4}".format(ms[0], ms[1], vs[0], vs[1], p))


"""結果"""
plt.subplot(211)
xs = np.linspace(min(data), max(data), 200)
norm1 = mlab.normpdf(xs, ms[0], math.sqrt(vs[0]))
norm2 = mlab.normpdf(xs, ms[1], math.sqrt(vs[1]))
draw_hist(data, 20)
plt.plot(xs, (1-p)*norm1 + p*norm2, color="red", lw=3)
plt.xlim(min(data), max(data))
plt.xlabel("x")
plt.ylabel("Probability")

plt.subplot(212)
plt.plot(np.arange(len(ls)), ls)
plt.xlabel("step")
plt.ylabel("log_likelihood")
plt.show()




    