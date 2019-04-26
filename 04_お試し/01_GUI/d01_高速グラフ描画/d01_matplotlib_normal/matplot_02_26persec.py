# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 21:31:50 2017

@author: p000495138
"""

import matplotlib.pyplot as plt
import numpy as np
import time


fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))

tstart = time.time()
num_plots = 0
while time.time()-tstart < 1:
    line.set_ydata(np.random.randn(100))
    plt.pause(0.001)
    num_plots += 1
print(num_plots)
