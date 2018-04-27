# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:49:55 2017

@author: p000495138
"""

import numpy as np
import matplotlib.pyplot as plt
import time

def pause_plot():
    fig, ax = plt.subplots(1,1)
    x = np.arange(-np.pi, np.pi, 0.1)
    y = np.sin(x*3)
    lines, = ax.plot(x,y,"--")
    plt.show(block=False)
    fig.canvas.draw()
    
    tstart = time.time()
    num_plots = 0
    
    while time.time()-tstart < 5:
        x += 0.1
        y = np.sin(x/5)
        lines.set_data(x,y)
        ax.draw_artist(ax.patch)
        ax.draw_artist(lines)
        ax.set_xlim((x.min(),x.max()))
        ax.set_ylim((y.min(),y.max()))
        fig.canvas.update()
        fig.canvas.flush_events()
        num_plots += 1
    print(num_plots/5)

if __name__ == "__main__":
    pause_plot()