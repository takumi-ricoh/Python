# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 11:15:43 2021

@author: p000495138
"""


#****　No.2 信号を時間軸と周波数軸で表現する *******

import numpy as np
import matplotlib.pyplot as plt

#%% 信号生成

#信号生成
N = 128        #サンプル数
dt = 0.01      #サンプリング周期
freq = 10      #信号の周波数 => 周期0.1sec
amp = 1        #振幅

t  = np.arange(0, N*dt, dt) #時間

#超重要公式 !!!!
f1 = amp * np.sin(2*np.pi * freq * t) 

#表示
plt.figure(1)
plt.plot(t,f1)
plt.grid(True)

#%% FFT

F = np.fft.fft(f1)

F_abs = np.abs(F)

F_abs_amp = F_abs / N * 2

F_abs_amp[0] = F_abs_amp[0] / 2

plt.figure(2)
plt.plot(F_abs_amp)
plt.grid(True)