# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:26:32 2017

@author: p000495138
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
matplotlib.style.use('ggplot')

fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))
ax.lines.remove(line) # remove line from bg
fig.show()
fig.canvas.draw()
background = fig.canvas.copy_from_bbox(ax.bbox) # save the bg

tstart = time.time()
num_plots = 0
while time.time()-tstart < 5:
    line.set_ydata(np.random.randn(100))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.update()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots/5)