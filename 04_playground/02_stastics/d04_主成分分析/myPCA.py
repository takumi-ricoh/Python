# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 18:38:28 2016

@author: p000495138
"""

from sklearn.decomposition import PCA
import numpy as np

x = np.linspace(0.2,1,100)
y = 0.8*x + np.random.randn(100)*0.1
X =  np.c_[x,y]
np.random.shuffle(X)

pca = PCA(n_components=2)
pca.fit(X)

#特性表示
print(pca)
print('components')
print(pca.components_)
print('mean')
print(pca.mean_)
print('covariance')
print(pca.get_covariance())

#共分散行列の作成
mn = np.mean(X,axis=0)
z = X - mn
cv = np.cov(z[:,0],z[:,1],bias=1)
#固有値と固有ベクトル
W, v = np.linalg.eig(cv)
print('eigenvector')
print(v)
print('eigenvalue')
print(W)

#共分散行列に固有ベクトルをかけてみる
print(cv.)