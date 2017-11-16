# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 18:28:48 2016

@author: p000495138
"""

import numpy as np
from sklearn import linear_model as lin

a=[1,2,1,1,2,2,2,1,1,2,1]
b=[3,4,3,3,4,4,4,3,3,4,3]

f =  lin.LogisticRegression.fit(a,b)
res = f(2)
