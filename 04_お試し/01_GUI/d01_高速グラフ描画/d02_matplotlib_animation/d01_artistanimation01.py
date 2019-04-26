# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 12:09:48 2018

https://qiita.com/chez_sugi/items/93ff2efad50f16bc8c37

@author: p000495138
"""

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np
fig, ax = plt.subplots()
artists = []
x = np.arange(10)
for i in range(10):
    y = np.random.rand(10)
    im = ax.plot(x, y)
    artists.append(im)
anim = ArtistAnimation(fig, artists, interval=10)
fig.show()
