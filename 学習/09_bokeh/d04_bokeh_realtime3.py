# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 23:08:09 2018

@author: takumi
"""
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

import numpy as np

source = ColumnDataSource(dict(x=[],y=[],avg=[]))

fig = Figure()
fig.line(source=source, x='x', y='y', line_width=2, alpha=.85, color='red')
fig.line(source=source, x='x', y='avg', line_width=2, alpha=.85, color='blue')

ct = 0
sine_sum = 0
def update_data():
    global ct, sine_sum
    ct +=1
    sin = np.sin(ct/10)
    sine_sum += sin
    new_data = dict(x=[ct], y=[sin], avg=[sine_sum/ct])
    source.stream(new_data, 300)

curdoc().add_root(fig)
curdoc().add_periodic_callback(update_data, 30)