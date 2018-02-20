# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 11:27:43 2018

@author: p000495138
"""
#オフラインモード
#import plotly.offline as offline
import plotly.offline as offline
import plotly.graph_objs as go
from plotly.graph_objs import Data

import numpy as np
import csv

#データ
csvdata=[]
with open("testdata.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        csvdata.append(row)
csvdata=np.array(csvdata)

trace0 = go.Scatter(
    x = csvdata[:,0],
    y = csvdata[:,1],
    name = "data0",)

trace1 = go.Scatter(
    x = csvdata[:,0],
    y = csvdata[:,2],
    name = "data1",
    mode = 'lines',)

data=Data([trace0,trace1])

#レイアウト
layout = go.Layout(
    title='Iris sepal length-width',
    xaxis=dict(title='sec'),
    yaxis=dict(title='℃'),
    showlegend=True,
    hovermode='closest',)

#プロット
fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename="example")

