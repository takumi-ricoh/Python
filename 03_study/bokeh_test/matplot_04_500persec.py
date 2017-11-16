# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 21:31:50 2017

@author: p000495138
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

fig, ax = plt.subplots()
line1, = ax.plot(np.random.randn(1000),"-*")
line2, = ax.plot(np.random.randn(1000))
plt.show(block=False)
fig.canvas.draw()

tstart = time.time()
num_plots = 0
while time.time()-tstart < 5:
    line1.set_ydata(np.random.randn(1000))
    line2.set_ydata(np.random.randn(1000))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line1)
    ax.draw_artist(line2)
    fig.canvas.update()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots/5)

