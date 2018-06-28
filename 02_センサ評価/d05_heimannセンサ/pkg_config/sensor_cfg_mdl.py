# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 22:44:05 2018

@author: takumi
"""

class Cfg():
    def __init__(self):
        self.PORT        = "COM13"
        self.BAUDRATE    = 9600
        self.SAMPLERATE  = 0.1
        self.SENNUM      = 8 #センサ数
        self.SENPOS      =[-100,-80,-60,-10,10,60,80,100]
    