# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 22:44:05 2018

@author: takumi
"""

def get_cfg():
    param = {
            "port":"COM1", 
            "baudrate":9600, 
            "samplerate":0.1, 
            "senNum":8, #センサ数
            "senPos":[-100,-80,-60,-10,10,60,80,100]
            }
    return param
    