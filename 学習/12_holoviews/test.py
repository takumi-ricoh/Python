# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:16:48 2018

@author: p000495138
"""
import holoviews as hv
import numpy as np

hv.extension('bokeh')

np.random.seed(111)
x = np.linspace(-np.pi, np.pi, 100)

hv.Curve((x, np.sin(x)))

