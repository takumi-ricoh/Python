# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:09:42 2018

@author: p000495138
"""

from bokeh.plotting import figure, curdoc,show
from bokeh.driving import linear
import numpy as np
import random

p = figure(plot_width=1000, plot_height=400)
line = p.line([], [], color="firebrick", line_width=2)

ds = line.data_source

@linear()
def update(step):
    ds.data['x'].append(step/100)
    ds.data['y'].append(np.sin(step/10))
    #ds.data['y'].append(random.randint(0,100))
    ds.trigger('data', ds.data, ds.data)
    if step>5:
        p.x_range.start = ds.data['x'][-50]
        p.x_range.end   = ds.data['x'][-50]

curdoc().add_root(p)
show(p)
# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 10)
