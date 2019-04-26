# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 09:32:03 2018

@author: p000495138
"""

#うごかねえ！#
#https://stackoverflow.com/questions/36181316/python-matplotlib-plotting-in-another-process

import matplotlib.pyplot as plt
import multiprocessing as mp
import random
import numpy
import time

def worker(q):
    #plt.ion()
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ln, = ax.plot([], [])
    fig.canvas.draw()   # draw and show it
    plt.show(block=False)

    while True:
        obj = q.get()
        n = obj + 0
        print("sub : got:", n)

        ln.set_xdata(numpy.append(ln.get_xdata(), n))
        ln.set_ydata(numpy.append(ln.get_ydata(), n))
        ax.relim()

        ax.autoscale_view(True,True,True)
        fig.canvas.draw()

if __name__ == '__main__':
    queue = mp.Queue()
    p = mp.Process(target=worker, args=(queue,))
    p.start()

    while True:
        n = random.random() * 5
        print("main: put:", n)
        queue.put(n)
        time.sleep(1.0)