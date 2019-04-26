# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:23:23 2018

@author: p000495138
"""

#https://stackoverflow.com/questions/43571924/multiprocessing-show-matplotlib-plot


import matplotlib.pyplot as plt
import numpy as np

import multiprocessing
#multiprocessing.freeze_support() # <- may be required on windows

def plot(datax, datay, name):
    x = datax
    y = datay**2
    plt.scatter(x, y, label=name)
    plt.legend()
    plt.show()

def multiP():
    for i in range(2):
        p = multiprocessing.Process(target=plot, args=(i, i, i))
        p.start()

if __name__ == "__main__": 
    input('Value: ') 
    multiP()
    