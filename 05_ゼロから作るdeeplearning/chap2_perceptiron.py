# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 12:03:55 2019

@author: p000495138
"""

import numpy as np

AND   = {"w":np.array([0.5,0.5]),"b":-0.7}
NAND  = {"w":np.array([-0.5,-0.5]),"b":0.7}
OR    = {"w":np.array([0.5,0.5]),"b":-0.2}

#%%
def perceptron1(x1,x2,param):
    theta = 0.5
    w1,w2 = param[0],param[1]
    tmp = x1*w1 + x2*w2
    if tmp <= theta:
        return 0
    elif tmp > theta:
        return 1

#%%
def perceptron2(x,p):
    
    tmp = p["w"] @ x + p["b"] 
    
    #print(tmp)
    
    if tmp <= 0:
        return False
    elif tmp > 0:
        return True

#%%XOR
def XOR(x,p):
    s1 = perceptron2(x,NAND)
    s2 = perceptron2(x,OR)
    y  = perceptron2([s1,s2],AND)
    return y

#%%実行

f = perceptron2
p = NAND

#f = XOR
#p = None

x = np.array([1,1])
res = f(x,p)
print("True & True ->",res)

x = np.array([0,0])
res = f(x,p)
print("False & False ->",res)

x = np.array([0,1])
res = f(x,p)
print("False & True ->",res)
