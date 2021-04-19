# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:00:55 2018

https://logics-of-blue.com/python-time-series-analysis/

@author: p000495138
"""


import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt

import statsmodels.api as sm

# https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/AirPassengers.html
dataNormal = pd.read_csv("AirPassengers.csv")
dataNormal.head()

# 日付形式で読み込む（dtype=floatで読み込まないと、あとでARIMAモデル推定時にエラーとなる）
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
data = pd.read_csv('AirPassengers.csv', index_col='Month', date_parser=dateparse, dtype='float')
data.head()

# 日付形式にする
ts = data['#Passengers'] 
ts.head()

#%% 解析

# 自己相関を求める
ts_acf = sm.tsa.stattools.acf(ts, nlags=40)
ts_acf
 
# 偏自己相関
ts_pacf = sm.tsa.stattools.pacf(ts, nlags=40, method='ols')
ts_pacf

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(ts, lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(ts, lags=40, ax=ax2)

# たぶん和分過程なので、差分をとる
diff = ts - ts.shift()
diff = diff.dropna()
 
# 差分系列への自動ARMA推定関数の実行
resDiff = sm.tsa.arma_order_select_ic(diff, ic='aic', trend='nc')
resDiff