# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:14:45 2018

@author: p000495138
"""
import numpy as np

a=[[1,2,3],[4,5,6],[7,8,9]]
b=np.array(a)
print("a=")
print(a, end='\n\n')
print("b=")
print(b, end='\n\n')

#データの変換
a2b = np.array(a)
b2a = b.tolist()

#足し算
print("b+1=")
print(b+1, end='\n\n')

#賭け算
print("a*3=")
print(a*3, end='\n\n')
print("b*3=")
print(b*3, end='\n\n')

#転置行列
c=b.T
print("c=")
print(c, end='\n\n')

#行列同士の掛算
d1 = np.dot(b,c)
print("bとcの積")
print(d1, end='\n\n')

#行列の要素の掛算
d2 = b*c
print("要素の積")
print(d2, end='\n\n')
