# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:18:13 2016

@author: p000495138
"""

#from __future__ import unicode_literals,print_function

import numpy as np
import matplotlib.pyplot as plt
import time


def pause_plot():
    fig, ax = plt.subplots(1,1)
    n = 10
    x = 
    y = np.sin(x*3)
    lines, = ax.plot(x,y)
    
    tstart = time.time()
    num_plots = 0
    while time.time()-tstart < 5:
        x += 0.1
        y = np.sin(x/3)
        lines.set_data(x,y)
        ax.set_xlim((x.min(),x.max()))
        plt.pause(.0001) ##必要!!
        num_plots += 1
        ax.legend("a")
    print(num_plots/5)
    
if __name__ == "__main__":
    pause_plot()
