# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 09:28:25 2016

@author: p000495138
"""

import scipy.interpolate as interp
import numpy as np
import matplotlib.pyplot as plt

a = np.loadtxt("mitsubishi.csv",delimiter=',')

b = interp.interp1d(a[:,0],a[:,1])

c = np.arange(0,126)

d = b(c)

#plt.plot(c,d,'.')

np.savetxt("res.csv",d)