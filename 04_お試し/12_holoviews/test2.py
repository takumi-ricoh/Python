# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:18:05 2018

@author: p000495138
"""

"""
Description: Exporting with styles
Author:      Jean-Luc Stevens
HoloViews:   1.6+
Python:      2.7+
This script demonstrates how to render HoloViews objects directly to
files using just the vanilla Python interpreter and Matplotlib,
i.e. without using IPython or a Jupyter notebook.  This script uses core
HoloViews (no extra dependencies) with the matplotlib backend.
To export HoloMaps to MP4, you need matplotlib animation support for
this export format which relies on ffmpeg.
Running this script as follows will generate a number of different files
in the current directory:
``python matplotlib_export.py``
Here are the expected files, listed in the order they are created:
example_I.svg
example_II.svg
example_III.svg
example_IV.svg
example_V.html  # HTML file (HoloMap with slider)
initial_layout.png
recomposed_layout.png
original_layout.png
new_customized_layout.png
new_customized_animation.png
savefig_I.png
savefig_II.png
savefig_III.png
test.mp4       # If the ffmpeg animation writer is enabled
frame.png
"""

import numpy as np
from holoviews import Image, Curve, HoloMap, Store

# Note that outside of Jupyter notebooks, you need to activate the
# appropriate renderer by importing it. Here we import the mpl backend.
from holoviews.plotting import mpl


# First lets create some example HoloViews objects to export

x,y = np.mgrid[-50:51, -50:51] * 0.1
image = Image(np.sin(x**2+y**2))

coords = [(0.1*i, np.sin(0.1*i)) for i in range(100)]
curve = Curve(coords)

curves = {phase:Curve([(0.1*i, np.sin(phase+0.1*i)) for i in range(100)])
                             for phase in [0, np.pi/2, np.pi, np.pi*3/2]}
waves = HoloMap(curves)

# Static layout
layout = image + curve

#==============================#
# Matplotlib renderer instance #
#==============================#

# This renderer will save elements to SVG and HoloMaps to HTML (you may
# select any appropriate format supported by the renderer)

renderer = Store.renderers['matplotlib'].instance(fig='svg')


#====================================================#
# Style I: Applying your chosen options while saving #
#====================================================#


# Example I: Specify the style of the Image object
renderer.save(layout, 'example_I', style=dict(Image={'cmap':'jet'}))

# Example II: Specify the style and plot options of the Image object
renderer.save(layout, 'example_II', style=dict(Image={'cmap':'Blues'}),
                                    plot= dict(Image={'fig_size':150}))

# Example III: Specify the style and plot options of the Image object
renderer.save(layout, 'example_III',
              options={'Image': {'plot':  dict(fig_size=150),
                                 'style': dict(cmap='jet')}})

# Example IV: Specify the style and plot options of the Image object
renderer.save(layout, 'example_IV',
              options={'Image': {'plot':  dict(fig_size=150),
                                 'style': dict(cmap='jet')}})

# Example V: Specify the style using the %opts magic syntax
#             without IPython (requires pyparsing)

from holoviews.ipython.parser import OptsSpec

renderer.save(image + waves, 'example_V',
                      options=OptsSpec.parse("Image (cmap='gray')"))


#=================================================#
# Style II: Creating objects with specific styles #
#=================================================#


# Create a renderer that will save to PNG
renderer = Store.renderers['matplotlib'].instance(fig='png')

# Example I: Save the default Layout
renderer.save(layout, 'initial_layout')

# Example II: Explicitly build a new Layout with a new, customized Image
renderer.save(image(style={'cmap':'Blues'}) + curve, 'recomposed_layout')

# Example III:  Note that the original layout and image are untouched.
renderer.save(layout, 'original_layout')

# Example IV: New Layout with elements customized as desired
renderer.save(layout(options={'Image':{'style':{'cmap':'Reds'}}}), 'new_customized_layout')

# Example IV: Request a new Layout with elements customized as desired
wave_layout = image + curve
renderer.save(wave_layout(options={'Image':{'style':{'cmap':'Reds'}}}),
                         'new_customized_animation')

# Note that __call__ returns a *new* object: your original objects image
# and curve are unchanged.

#==================================================================#
# Style III (Advanced): Directly interfacing with the Plot classes #
#==================================================================#

# Note that this style is of interest to developers and makes uses the
# interface to MPLPlot instances used MPLRenderer.

# Example I: Calling RasterPlot directly
raster_plot = mpl.RasterPlot(image)
raster_plot.update(0)
print("Matplotlib figure: %s" % type(raster_plot.state))
raster_plot.state.savefig('savefig_I.png', format='png')

# Example I: Calling RasterPlot directly with a customized Image
raster_plot = mpl.RasterPlot(image(style={'cmap':'Blues'}))
raster_plot.update(0)
raster_plot.state.savefig('savefig_II.png', format='png')


# Example III: Calling LayoutPlot directly with a customized layout
raster_plot = mpl.LayoutPlot(image(style={'cmap':'Blues'}) + curve)
raster_plot.update(0)
raster_plot.state.savefig('savefig_III.png', format='png')

# Example III: Calling LayoutPlot to generated a customized layout animation
raster_plot = mpl.LayoutPlot(image(style={'cmap':'Blues'}) + waves)
matplotlib_animation = raster_plot.anim()
print("Matplotlib FuncAnimation: %s" % type(matplotlib_animation))
try:
    matplotlib_animation.save('test.mp4', fps=5)
except RuntimeError:
    print("Could not export 'test.mp4' using matplotlib_animation. "
          "Is the appropriate animation write available (requires ffmpeg)")

# Example IV: Frame access for animations
raster_plot = mpl.LayoutPlot(image(style={'cmap':'Blues'}) + waves)
matplotlib_figure = raster_plot[3] # integer frame number
# or matplotlib_figure = raster_plot[2.0,] # continuous coordinate dimension value
print("Frame (matplotlib figure): %s" % matplotlib_figure)
matplotlib_figure.savefig('frame.png', format='png')