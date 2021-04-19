# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 11:27:43 2018

@author: p000495138
"""
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly import tools
import time
from IPython import display

#pyo.init_notebook_mode(connected=True)

trace = go.Scatter(
    x=[1, 2, 3],
    y=[4, 5, 6]
)

fig = tools.make_subplots(rows=1, cols=1)
fig['data'].append(trace)
pyo.plot(fig)

for i in range(3):
    time.sleep(1)
    trace = go.Scatter(
        x=[i, i+1, i+2],
        y=[4, 5, 6]
    )
    fig['data'].update(trace)
    pyo.plot(fig)