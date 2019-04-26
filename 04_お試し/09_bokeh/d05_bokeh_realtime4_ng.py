# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 23:51:51 2018

@author: takumi
"""

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure,show

import numpy as np

#source = ColumnDataSource(dict(y=[]))
source = ColumnDataSource(data=dict(foo=[10, 20, 30], bar=[100, 200, 300]))

fig = Figure()
fig.line(source=source, x='x', y='y', line_width=2, alpha=.85, color='red')

#y = np.random.randn(100)
#patches = {'y': [y]}
patches = {
    'foo' : [ (slice(2), [11, 12]) ],
    'bar' : [ (0, 101), (2, 301) ],
}
source.patch(patches)
show(fig)

#def update_data():
#    y = np.random.randn(100)
#    patches = {'y': [y]}
#    source.patch(patches)
#
#curdoc().add_root(fig)
#curdoc().add_periodic_callback(update_data, 100)