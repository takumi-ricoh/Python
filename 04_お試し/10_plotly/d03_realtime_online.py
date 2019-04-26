# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:10:59 2018

@author: p000495138
"""

import plotly.plotly as py
from plotly.graph_objs import *

trace0 = Scatter(
    x=[1, 2],
    y=[1, 2]
)

trace1 = Scatter(
    x=[1, 2],
    y=[2, 3]
)

trace2 = Scatter(
    x=[1, 2],
    y=[3, 4]
)

data = Data([trace0, trace1, trace2])

# Take 1: if there is no data in the plot, 'extend' will create new traces.
plot_url = py.plot(data, filename='extend plot', fileopt='extend')
