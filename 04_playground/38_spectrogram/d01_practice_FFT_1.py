# -*- coding: utf-8 -*-
"""
FFTについて学習する


"""

"""
参考
https://momonoki2017.blogspot.com/2018/03/pythonfft-1-fft.html

"""

#****　No.1 簡単な信号でFFTを体験する  *******

from scipy.fftpack import fft
from scipy.signal import spectrogram
import numpy as np
import matplotlib.pyplot as plt

plt.clf()
plt.close("all")

#%% データ1 (1周期)
#fftは2のn乗個にする必要がある
#まずは2**5 = 32個で考える

N = 32
n = np.arange(32)
signal1 = np.sin(2*np.pi * n/N) 

plt.figure(1)
plt.plot(signal1)

#%% データ2 (3周期)
#fftは2のn乗個にする必要がある
#まずは2**5 = 32個で考える

N = 32
n = np.arange(N)
freq = 3
signal2 = np.sin(freq * 2*np.pi * n/N)

plt.figure(2)
plt.plot(signal2)

#%% データ2のFFT
F = np.fft.fft(signal2)

#結果は複素数
print(F)

#絶対値に変換する
F_abs = np.abs(F)

#後半は鏡像なので無視すること！
#データ数の半分までしか確認できない！ので、個数を絞る
plt.figure(3)
plt.plot(F_abs[:int(N/2)+1])
plt.grid(True)

#%% Y軸の値を調整する (1になる)

F_abs_amp = F_abs / N * 2        # 交流成分はデータ数で割って2倍する
F_abs_amp[0] = F_abs_amp[0] / 2  # 直流成分は2倍不要

plt.figure(4)
plt.plot(F_abs_amp[:int(N/2)+1])
plt.grid(True)

#%% 振幅を変えてみる

N = 32
n = np.arange(N)
freq = 3
amp = 4
signal3 = amp * np.sin(freq * 2*np.pi * n/N)

#FFT
F = np.fft.fft(signal3)
F_abs = np.abs(F) #絶対値変換

#振幅調整
F_abs_amp = F_abs / N * 2        # 交流成分はデータ数で割って2倍する
F_abs_amp[0] = F_abs_amp[0] / 2  # 直流成分は2倍不要
 
plt.figure(5)
plt.plot(F_abs_amp[:int(N/2)+1])
plt.grid(True)

#%% 複雑な波形を作る
N = 64
n = np.arange(N)
f1 = 2 #周期
f2 = 6 #周期
amp1 = 1.5
amp2 = 3

signal4 = amp1*np.sin(f1*2*np.pi*(n/N)) + amp2*np.sin(f2*2*np.pi*(n/N))

plt.figure(6)
plt.plot(signal4)
plt.grid(True)

#FFT
F = np.fft.fft(signal4)
F_abs = np.abs(F) #絶対値変換

#振幅調整
F_abs_amp = F_abs / N * 2        # 交流成分はデータ数で割って2倍する
F_abs_amp[0] = F_abs_amp[0] / 2  # 直流成分は2倍不要
 
plt.figure(7)
plt.plot(F_abs_amp[:int(N/2)+1])
plt.grid(True)
