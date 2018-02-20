# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 12:20:32 2018

@author: p000495138
"""

from bokeh.io import show
import numpy as np

#%% テスト1
from bokeh.plotting import figure, output_file, show
x = np.linspace(0,100,1001)
y = np.sin(x/3)
output_file("line.html")
p = figure(title="line",x_axis_label="x",y_axis_label="y")
p.line(x,y,legend="Temp",line_width=2)
#show(p)

#%% テスト2
from bokeh.plotting import figure, output_file, show
x = np.linspace(0,100,1001)
y1 = np.sin(x/3)+1
y2 = np.cos(x/4)+1
y3 = np.cos(x/5)+1

output_file("lines_log.html")

p = figure(
        tools = "pan,box_zoom,reset,save,hover",
        y_axis_type = "log",
        y_range = [0.001,2],
        title="log_axis_example",
        x_axis_label="sections",
        y_axis_label="particles")

p.line(x,x,legend="y=x")
p.circle(x,x,legend="y=x",fill_color="white",size=8)
p.line(x,y1,legend="y1",line_width=3)
p.line(x,y2,legend="y2",line_color="red")
p.circle(x,y2,legend="y2",fill_color="red",line_color="red",size=6)
p.line(x,y3,legend="y3",line_color="orange",line_dash="4 4")

show(p)

#%% テスト3
from bokeh.plotting import figure, output_file, show
N=4000
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
]

#出力物の設定
output_file("scatter.html")
TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,hover"
#プロット
p = figure(tools=TOOLS, x_range=(0,100), y_range=(0,100))
p.circle(x,y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)
show(p)

#%%　テスト4
import bokeh
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

x = np.linspace(0,100,301)
y0 = np.sin(x/3)+1
y1 = np.cos(x/4)+1
y2 = np.cos(x/5)+1
#出力物の設定
output_file("linked_panning.html")

#プロット
s1 = figure(width=250, plot_height=250, title=None)
s1.circle(x, y0, size=10, color="navy", alpha=0.5)

s2 = figure(width=250, height=250, x_range=s1.x_range, y_range=s1.y_range, title=None)
s2.triangle(x, y1, size=10, color="firebrick", alpha=0.5)

s3 = figure(width=250, height=250, x_range=s1.x_range, title=None)
s3.square(x, y2, size=10, color="olive", alpha=0.5)

p = gridplot([[s1], [s2], [s3]], toolbar_location=None)

#show(p)

