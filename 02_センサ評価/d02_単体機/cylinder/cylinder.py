# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:17:33 2016

@author: p000495138
"""
import numpy as np
import pandas as pd

r     = 15
z     = np.arange(15,30,1)
theta = np.arange(1,90,0.1)
theta_rad = np.deg2rad(theta)

A  = r/np.tan(theta_rad)
B  = r
fi = np.arctan(B/A)


res = np.zeros(len(theta),)
for i in range(len(z)):
    s=[]
    for j in range(len(theta)):
        temp = z[i]/np.sqrt(A[j]**2+B**2)
        alfa = np.arcsin(temp) - fi[j] 
        
        alfa = np.rad2deg(alfa)
        theta2 = 90 - theta[j] - alfa
        s.append(theta2)
    res = np.c_[res,np.array(s)]
 
res = np.c_[theta,res]
       
#3write_data = data.T
name="result.csv"
writedata_pd = pd.DataFrame(res) #データフレーム化
writedata_pd.to_csv(name) #ｃｓｖ保存

