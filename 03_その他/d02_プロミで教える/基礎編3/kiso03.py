# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 10:21:32 2018

@author: p000495138
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,50,10001)
y1 = np.sin(x)
y2 = np.sin(x*8)/5
y3 = y1+y2
y4=y3.copy()
y4[y3>0.5]=0.5
y4[y3<-0.5]=-0.5

plt.subplot(2,2,1)
plt.plot(x,y1)
plt.ylim(-1.5,1.5)
plt.grid(True)

plt.subplot(2,2,2)
plt.plot(x,y2)
plt.ylim(-1.5,1.5)
plt.grid(True)

plt.subplot(2,2,3)
plt.plot(x,y3)
plt.ylim(-1.5,1.5)
plt.grid(True)

y4=y3.copy()

y4[y3>0.5]=0.5
y4[y3<-0.5]=-0.5

plt.subplot(2,2,4)
plt.plot(x,y4)
plt.ylim(-1.5,1.5)
plt.grid(True)