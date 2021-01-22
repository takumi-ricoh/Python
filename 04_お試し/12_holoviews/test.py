# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:16:48 2018

@author: p000495138
"""
import holoviews as hv
import holoviews.plotting.mpl

import time

r = hv.Store.renderers['matplotlib'].instance(interactive=True)

curve = hv.Curve(range(10))
r.show(curve)