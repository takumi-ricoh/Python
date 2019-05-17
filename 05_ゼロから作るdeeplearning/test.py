# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:32:28 2019

@author: p000495138
"""

import two_layer_net as two
import load_mnist
import numpy as np

net = two.TwoLayerNet(input_size=784, hidden_size=100, output_size=10)

print("\n ## パラメータサイズ ##")
print("W1サイズ=",net.params["W1"].shape)
print("b1サイズ=",net.params["b1"].shape)
print("W2サイズ=",net.params["W2"].shape)
print("b2サイズ=",net.params["b2"].shape)

x = np.random.rand(100,784)
y = net.predict(x)

print("\n ## 勾配計算(ダミーデータ) ##")
t = np.random.rand(100,10)
#grads = net.numerical_gradient(x,t)
grads = net.gradient(x,t)
print(grads)

