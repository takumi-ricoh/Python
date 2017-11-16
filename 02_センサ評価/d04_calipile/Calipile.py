# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 12:45:37 2016

@author: p000495138
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plot_junk as ju

columns=["Tobj","Tamb","Tobj LP1","Tobj LP2","Tobj LP frozen","Tamb LP", "TP presence", "TP motion", "Tamb shock","int status flag","int status sign","chip status flag","chip status sign",
        "TC1","TC2","TC3","presence treshold","motion treshold","shock treshold","interrupt mask","cycle for diff","src select","timer interrupt","Tobj *10[ｰC]","Tamb *10[ｰC]"]

file = ['res1.log','res2.log','res3.log','res4.log','res5.log','res6.log','res7.log','res8.log','res9.log']
f=[]
t=[]

for i in file:
    temp = pd.read_csv(i,skiprows=3,encoding = "ISO-8859-1",delim_whitespace=True,names=columns)
    f.append(temp)
    t.append(np.linspace(0,0.03*len(temp),len(temp)))

"""Tobj,Tpresence,Tmotion,Tambshock"""

num = 3

case = [1,2,3,4,1,1,1,3,4]

fig1=plt.figure(0)

plt.subplot(221)
plt.plot(t[num],f[num][columns[0]])
plt.grid(True)
plt.legend(loc=0)

plt.subplot(222)
plt.plot(t[num],f[num][columns[6]])
plt.grid(True)
plt.legend(loc=0)

plt.subplot(223)
plt.plot(t[num],f[num][columns[7]])
plt.grid(True)
plt.legend(loc=0)

plt.subplot(224)
plt.plot(t[num],f[num][columns[8]])
plt.grid(True)
plt.legend(loc=0)

fig2=plt.figure(2)
ju.myplot(t[num],f[num],case[num])


"""全部表示"""
#plt.figure(0)
#for i in range(len(columns)):
#    ax = plt.subplot(5,5,i+1)
#    ax.plot(t,f[columns[i]])    
#    ax.set_title(columns[i],fontsize=10)
#    #ax.tick_params(labelbottom='off')
#    #ax.tick_params(labelleft='off')
#    ax.grid(True)
#plt.tight_layout(pad=0.2)