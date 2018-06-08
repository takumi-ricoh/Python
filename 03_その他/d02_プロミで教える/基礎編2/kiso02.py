# -*- coding: utf-8 -*-
"""
Created on Wed May 30 09:38:50 2018

@author: p000495138
"""

import matplotlib.pyplot as plt
import random

"方法1"
x=[0]
y=[0]
for i in range(300-1):
    xrand = random.random()
    yrand = random.random()
    x.append(x[-1]+xrand-0.5)
    y.append(y[-1]+yrand-0.5)

"方法2"
x=[]
y=[]
x_new = 0
y_new = 0
for i in range(300):
    x.append(x_new)
    y.append(y_new)    
    
    xrand = random.random()
    yrand = random.random()

    x_new = x_new + xrand - 0.5
    y_new = y_new + yrand - 0.5
    

plt.figure(1)
plt.plot(x)
plt.plot(y)

plt.figure(2)
plt.plot(x,y)

x2 = x[50:-50:2]
y2 = y[50:-50:2]

plt.figure(3)
plt.plot(x2,y2,".-r")
plt.grid(True)
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["data"])
plt.title("random")