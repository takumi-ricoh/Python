# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:11:43 2017

@author: p000495138
"""

from sklearn import datasets
import numpy as np

""" データ読み出し """
iris = datasets.load_iris()
X = iris.data[:, [2, 3]] #特徴量
y = iris.target #ラベル
print("Class labels:", np.unique(y)) #ラベルの種類を表示

""" データ分割 """
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0)

