# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 17:54:19 2016

@author: p000495138
"""

import matplotlib.pyplot as plt


def myplot(t,f,case):
    if case==1:#方式1
        sub1_1 = f['Tobj']
        sub1_2 = f['Tobj LP2']*(2**17/2**20)
        sub2_1 = f['TP presence']
        sub2_2 = f['Tobj']-f['Tobj LP2']*(2**17/2**20)
        leg2   = ['presence','Tobj - LP2']
    elif case==2:#方式2
        sub1_1 = f['Tobj LP1']
        sub1_2 = f['Tobj LP2']
        sub2_1 = f['TP presence']
        sub2_2 = f['Tobj LP1']-f['Tobj LP2'] 
        leg2   = ['presence','LP1 - LP2']
    elif case==3:#方式3
        sub1_1 = f['Tobj']
        sub1_2 = f['Tobj LP frozen']*(2**17/2**24)
        sub2_1 = f['TP presence']
        sub2_2 = f['Tobj']-f['Tobj LP frozen']*(2**17/2**24)
        leg2   = ['presence','Tobj - frozen']
    elif case==4:#方式4
        sub1_1 = f['Tobj LP1']
        sub1_2 = f['Tobj LP frozen']*(2**20/2**24)
        sub2_1 = f['TP presence']
        sub2_2 = f['Tobj LP1']-f['Tobj LP frozen']*(2**20/2**24)
        leg2   = ['presence','LP1 - frozen']
    
    plt.subplot(211)
    plt.plot(t,sub1_1)
    plt.plot(t,sub1_2,'g') 
    plt.grid(True)
    
    sub1_3 = f['Tobj LP2']*(2**20/2**20)
    plt.plot(t,sub1_3,'g--')
    
    plt.legend(loc=0)

    plt.subplot(212)
    plt.plot(t,sub2_1)
    plt.plot(t,sub2_2,'g') 
    plt.grid(True)
    plt.legend(leg2,loc=0)