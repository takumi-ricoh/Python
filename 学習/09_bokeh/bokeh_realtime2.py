# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:48:13 2018

@author: p000495138


https://qiita.com/kazetof/items/49d4ebdd532b52245732

"""
from bokeh.plotting import figure, curdoc,show
from bokeh.plotting import ColumnDataSource
from bokeh.driving import linear
import numpy as np
import pandas as pd
import time

x = np.linspace(0,100,1001)
y = np.sin(x/3)
p = figure(title="line",x_axis_label="x",y_axis_label="y")

source = ColumnDataSource(dict(x=x, y=y))

p.line(source.data["x"],source.data["y"],legend="Temp",line_width=2)

curdoc().add_root(p)

show(p)

def update_data(x,y):
    source.data = dict(x=x, y=y)

for i in range(10000):
    x = np.linspace(i,100+i,1000)
    y=np.sin(x/10)*2
    time.sleep(0.1)
    update_data(x,y)
#
#curdoc().add_root(p)
#
## Add a periodic callback to be run every 500 milliseconds
#curdoc().add_periodic_callback(update, 10)
