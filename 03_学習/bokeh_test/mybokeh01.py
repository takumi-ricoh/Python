# -*- coding: utf-8 -*-
"""
Created on Mon May 29 10:57:42 2017

@author: p000495138
"""

from bokeh.plotting import figure, output_file, show

x=[1,2,3,4]
y=[3,2,4,1]

p=figure()

p.line(x,y,)

show(p)