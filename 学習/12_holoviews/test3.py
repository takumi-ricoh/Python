# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:22:55 2018

@author: p000495138
"""
#動く

import holoviews as hv

curve = hv.Curve(range(10)) # Could be any HoloViews object

renderer = hv.renderer('bokeh')

# Using renderer save
#renderer.save(curve, 'graph.html')

# Convert to bokeh figure then save using bokeh
plot = renderer.get_plot(curve).state

#from bokeh.io import output_file, save, show
from bokeh.plotting import output_file, save, show

#save(plot, 'graph.html')
# OR
#output_file("graph.html")
show(plot)


