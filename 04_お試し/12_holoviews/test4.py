# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:25:35 2018

@author: p000495138
"""

import holoviews as hv
import numpy as np
hv.extension('bokeh')
%opts Curve [show_grid=False xaxis=None yaxis=None]

def clifford(a,b,c,d,x0,y0):
    xn,yn = x0,y0
    coords = [(x0,y0)]
    for i in range(10000):
        x_n1 = np.sin(a*yn) + c*np.cos(a*xn)
        y_n1 = np.sin(b*xn) + d*np.cos(b*yn)
        xn,yn = x_n1,y_n1
        coords.append((xn,yn))
    return coords

def clifford_attractor(a,b,c,d):
    return hv.Curve(clifford(a,b,c,d,x0=0,y0=0))

%%opts Curve (line_width=0.03 color='red')
clifford_attractor(a =-1.5, b=1.5, c=1, d=0.75 )

dmap = hv.DynamicMap(clifford_attractor, kdims=['a','b','c','d'])

%%opts Curve (line_width=0.03 color='green')
# When run live, this cell's output should match the behavior of the GIF below
dmap.redim.range(a=(-1.5,-1),b=(1.5,2),c=(1,1.2),d=(0.75,0.8))

def interactive_clifford(a,b,c,d,x=0,y=0):
    coords = clifford(a,b,c,d,x0=x,y0=y)
    return (hv.Curve(coords) * hv.Points(coords[0]) * hv.Curve(coords[:2], group='Init')
            * hv.Text(-0.75,1.35, 'x:{x:.2f} y:{y:.2f}'.format(x=coords[0][0],y=coords[0][1])))
    
