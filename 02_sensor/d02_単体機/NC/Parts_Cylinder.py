# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:53:51 2016

@author: p000495138
"""

import numpy as np
import pandas as pd

#表面とセンサのなす角度計算
def calc_surf_ang(r,z_range,t_range):
    """
    #r      :円筒半径
    #z_range:センサと円筒軸中心の距離水準
    #t_range:センサから見た角度水準
    
    例)   
    r     = 15
    z_range = np.arange(16,30,1)
    t_range = np.arange(1,90,0.1)
     """
    
    theta_rad = np.deg2rad(t_range)
    
    A  = r/np.tan(theta_rad)
    B  = r
    fi = np.arctan(B/A)
       
    res = np.zeros([len(t_range),len(z_range)])
    print(np.shape(res))
    for i in range(len(t_range)):
        for j in range(len(z_range)):
            temp = z_range[j]/np.sqrt(A[i]**2+B**2)
            alfa = np.rad2deg( np.arcsin(temp) - fi[i] )            
            res[i,j] = 90 - t_range[i] - alfa

    return res


#円筒エッジ角度の計算
def calc_edge_ang(r,z_range,y_range):
    """
    #r       :円筒半径
    #z_range :センサと円筒軸中心の距離水準
    #y_range :センサと円筒軸中心の高さ水準
    
    """
    res = np.ones([len(z_range),len(y_range)]) #とりあえず表を作る

    print(res)
    print(len(y_range))
    print(len(z_range))
    gap          = res.copy()
    edge_plus   = res.copy()    
    edge_minus  = res.copy()    
    
    for j in range(len(y_range)):
        for i in range(len(z_range)):
            #z'
            gap[i,j]   = np.sqrt(y_range[j]**2 + z_range[i]**2)            
            #α
            edge_plus[i,j]  = np.arcsin(r/gap[i,j]) + np.arctan(y_range[j]/z_range[i])
            edge_minus[i,j] = np.arcsin(r/gap[i,j]) - np.arctan(y_range[j]/z_range[i])

    return gap, edge_plus, edge_minus