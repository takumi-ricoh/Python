# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 15:30:28 2021

@author: p000495138


やるお
"""


###矩形関数のフーリエ変換結果

import numpy as np
import matplotlib.pyplot as plt

a=4

omega = np.arange(-np.pi,np.pi,0.001)

f = 2/omega * np.sin(a*omega)

f[3140] = 2*a


#plt.plot(omega,np.abs(f))
#plt.grid(True)


#%% 離散信号

omega1 = np.pi/4 #rad/sample
#omega1 = 2 #rad/sample

samples1 = np.arange(0,16,1)     #サンプリング
samples2 = np.arange(0,16,0.01)  

y1 = np.cos(omega1*samples1)
y2 = np.cos((omega1)*samples2)
y3 = np.cos((omega1+2*np.pi)*samples2)

plt.scatter(samples2,y3)
plt.scatter(samples2,y2)
plt.scatter(samples1,y1)
#plt.scatter(samples2,y2)
#plt.legend(["+2pi","def"])
plt.grid(True)

