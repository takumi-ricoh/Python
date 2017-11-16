# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:12:33 2016

@author: p000495138
"""
##フィッティングに使うもの
from scipy.optimize import curve_fit
import numpy as np

## 図示のために使うもの
import seaborn as sns
import matplotlib.pyplot as plt

list_linear_x = range(0,20,2)

array_error = np.random.normal(size=len(list_linear_x))

array_x = np.array(list_linear_x)
array_y = array_x + array_error ##完全な y=x の直線に誤差項を加えてボコボコしたデータを作ってます

sns.pointplot(x=array_x,y=array_y,join=False)

def linear_fit(x,a,b):
    return a*x + b

param, cov = curve_fit(linear_fit, array_x, array_y)

array_fit = param[0] * array_x + param[1]

sns.pointplot(x=array_x,y=array_fit,markers="")