# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:07:38 2017

@author: p000495138
"""

import matplotlib.pyplot as plt
import numpy as np
import time

x = np.arange(0, 2*np.pi, 0.01)
y = np.sin(x)

fig, axes = plt.subplots(nrows=6)
styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
lines = [ax.plot(x, y, style)[0] for ax, style in zip(axes, styles)]

fig.show()

tstart = time.time()
for i in range(1, 20):
    for j, line in enumerate(lines, start=1):
        line.set_ydata(np.sin(j*x + i/10.0))
    fig.canvas.draw()

print('FPS:' , 20/(time.time()-tstart))