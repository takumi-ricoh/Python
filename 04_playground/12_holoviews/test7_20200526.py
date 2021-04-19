# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:52:06 2020

@author: p000495138
"""

from itertools import islice
import numpy as np
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

bounds = (-2,-1.4,0.8,1.4)
# Growth rates used in the logistic map
growth_rates = np.linspace(0.9, 4, 1000)
# Bifurcation points
bifurcations = [1, 3, 3.4494, 3.5440, 3.5644, 3.7381, 3.7510, 3.8284, 3.8481]


def mandelbrot_generator(h,w, maxit, bounds=bounds):
    "Generator that yields the mandlebrot set."
    (l,b,r,t) = bounds
    y,x = np.ogrid[b:t : h*1j, l:r:w*1j]
    c = x+y*1j
    z = c
    divtime = maxit + np.zeros(z.shape, dtype=int)
    for i in range(maxit):
        z  = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime==maxit)
        divtime[div_now] = i
        z[diverge] = 2
        yield divtime
        
def mandelbrot(h,w, n, maxit):
    "Returns the mandelbrot set computed to maxit"
    iterable =  mandelbrot_generator(h,w, maxit)
    return next(islice(iterable, n, None))

def mapping(r):
    "Linear mapping applied to the logistic bifurcation diagram"
    return (r /2.0) * ( 1 - (r/2.0))

def logistic_map(gens=20, init=0.5, growth=0.5):
    population = [init]
    for gen in range(gens-1):
        current = population[gen]
        population.append(current * growth * (1 - current))
    return population


bifurcation_diagram = hv.Points([(mapping(rate), pop) for rate in growth_rates for 
             (gen, pop) in enumerate(logistic_map(gens=110, growth=rate))
             if gen>=100])  # Discard the first 100 generations to view attractors more easily

vlines = hv.Overlay([hv.Curve([(mapping(pos),0), ((mapping(pos),1.4))]) for pos in bifurcations])
overlay = (hv.Image(mandelbrot(800,800, 45, 46).copy(), bounds=(-2, -1.4, 0.8, 1.4))
           * bifurcation_diagram * hv.HLine(0) * vlines)

hv.output(size=150)
overlay.opts(
    opts.HLine(color='k', line_dash='dashed'),
    opts.Image(cmap='Reds', logz=True, xaxis=None, yaxis=None),
    opts.Points(size=0.5, color='g'),
    opts.Curve(color='teal', line_width=1))