# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:48:48 2020

@author: p000495138
"""

import holoviews as hv
from holoviews import opts
import numpy as np
hv.extension('bokeh')

class DragonCurve(object):
    "L-system agent that follows rules to generate the Dragon Curve"
    
    initial ='FX'
    productions = {'X':'X+YF+', 'Y':'-FX-Y'}
    dragon_rules = {'F': lambda t,d,a: t.forward(d),
                    'B': lambda t,d,a: t.back(d),
                    '+': lambda t,d,a: t.rotate(-a),
                    '-': lambda t,d,a: t.rotate(a),
                    'X':lambda t,d,a: None,
                    'Y':lambda t,d,a: None }
    
    def __init__(self, x=0,y=0, iterations=1):
        self.heading = 0
        self.distance = 5
        self.angle = 90
        self.x, self.y = x,y
        self.trace = [(self.x, self.y)]
        self.process(self.expand(iterations), self.distance, self.angle)
        
    def process(self, instructions, distance, angle):
        for i in instructions:          
            self.dragon_rules[i](self, distance, angle)
        
    def expand(self, iterations):
        "Expand an initial symbol with the given production rules"
        expansion = self.initial
        
        for i in range(iterations):
            intermediate = ""
            for ch in expansion:
                intermediate = intermediate + self.productions.get(ch,ch)
            expansion = intermediate
        return expansion

    def forward(self, distance):
        self.x += np.cos(2*np.pi * self.heading/360.0)
        self.y += np.sin(2*np.pi * self.heading/360.0)
        self.trace.append((self.x,self.y))
    
    def rotate(self, angle):
        self.heading += angle
        
    def back(self, distance):
        self.heading += 180
        self.forward(distance)
        self.heading += 180
        
    @property
    def path(self):
        return hv.Path([self.trace])
    
hmap = hv.HoloMap(kdims='Iteration')
for i in range(7,17):
    hmap[i] = DragonCurve(-200, 0, i).path

hmap.opts(
    opts.Path(axiswise=False, color='black', line_width=1, 
              title='', xaxis=None, yaxis=None, framewise=True))