# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 09:35:27 2016

@author: p000495138
"""

import inspect
import numpy as np
from sklearn import svm
from scipy import random as rand
import matplotlib.pyplot as plt

t=np.linspace(0,100,1000)

x1=10*np.sin(t/2) * np.exp(-t/50)
x2=np.random.randn(1000)
x3 =x1+x2

#特徴量
t2=t.reshape(t.size,1)

m = svm.SVR(C=1,kernel='rbf',gamma=0.1)
y = m.fit(t2,x3)

z = m.predict(t2)

plt.plot(t,x3)
plt.plot(t,z,'r')
