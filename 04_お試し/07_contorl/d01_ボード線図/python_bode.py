# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:32:52 2016

@author: p000495138
"""

from control.matlab import *
import matplotlib.pyplot as plt
import numpy as np

def main():

    (k1, T1) = (1, 1)           # 一次遅れ要素のパラメータ1
    (k2, T2) = (2, 10)          # 一次遅れ要素のパラメータ2
    G1= tf([k1],[T1,1])         # 伝達関数表現
    G2= tf([k2],[T2,1])         # 伝達関数表現
    w = np.logspace(-2,2,100)   # 角周波数(10^-2～10^2)
    bode(G1,G2,w)               # ボード線図の計算とプロット
    plt.legend(["T=1, k=1"],["T=10, k=2"],3)  # 凡例
    plt.show()                  # 結果表示


if __name__ == '__main__':
    main()