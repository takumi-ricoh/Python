# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 17:55:41 2019

@author: p000495138
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
#MNISTデータのロード
import load_mnist
import pickle

#%%　活性化関数
class Activation:

    def __init__(self):
        pass
    
    #ステップ関数
    def step_function(self,x):
        if x > 0:
            return 1
        else:
            return 0
        
    #ステップ関数
    def step_function2(self,x):
        y = x > 0
        return y.astype(np.int)
    
    
    #シグモイド関数
    def sigmoid(self,x):
         y = 1 / (1+np.exp(-x))
         return y
    
    #Relu関数
    def relu(self,x):
         y = np.maximum(0,x)
         return y

#%%　出力層クラス

class Output:
    def __init__(self):
        pass
    
    #恒等関数
    def identity_function(self,x):
        return x

    #ソフトマックス関数
    def softmax(self,a):
        """
        0～1の間の配列を返す。合計が1になる
        """
        #オーバーフロー対策
        c = np.max(a)
        #計算
        exp_a = np.exp(a-c)
        sum_exp_a = np.sum(exp_a)
        y = exp_a / sum_exp_a
        return y

    def softmax2(self,x):
        if x.ndim == 2:
            x = x.T
            x = x - np.max(x, axis=0)
            y = np.exp(x) / np.sum(np.exp(x), axis=0)
            return y.T 
        
        x = x - np.max(x) # オーバーフロー対策
        return np.exp(x) / np.sum(np.exp(x))


#%%& 簡単なニューラルネットワーク
class Naive_network:
    
    def __init__(self):
        self.init_network()

    def init_network(self):
        self.network = {}
        self.network["W1"] = np.array([[0.1,0.3,0.5],[0.2,0.4,0.6]])
        self.network["b1"] = np.array([0.1,0.2,0.3])
        self.network["W2"] = np.array([[0.1,0.4],[0.2,0.5],[0.3,0.6]])
        self.network["b2"] = np.array([0.1,0.2])
        self.network["W3"] = np.array([[0.1,0.3],[0.2,0.4]])
        self.network["b3"] = np.array([0.1,0.2])
                
    def forward(self,x):
        
        #活性化関数
        act = Activation()
        
        W1,W2,W3 = self.network["W1"],self.network["W2"],self.network["W3"]
        b1,b2,b3 = self.network["b1"],self.network["b2"],self.network["b3"]        
        
        a1 = x@W1 + b1
        z1 = act.sigmoid(a1)
        a2 = z1@W2 + b2
        z2 = act.sigmoid(a2)        
        a3 = z2@W3 + b3
        z3 = act.sigmoid(a3)
        
        y  = act.identity_function(z3)
        
        return y

#%% MNISTを予め学習済みのネットワークで認識する
class MNIST_net:
    def __init__(self):    
        self.act = Activation()
        self.out = Output()
        
    def get_data(self):
        (self.x_train, self.t_train),(self.x_test, self.t_test) = load_mnist.load_mnist(flatten=True, normalize=False)
        return self.x_test,self.t_test
    
    def init_network(self):
        with open("sample_weight.pkl","rb") as f:
            network = pickle.load(f)
        return network
    
    def predict(self,network,x):
        W1, W2, W3 = network["W1"], network["W2"], network["W3"]
        b1, b2, b3 = network["b1"], network["b2"], network["b3"]
        
        a1 = x@W1 + b1
        z1 = self.act.sigmoid(a1)
        a2 = z1@W2 + b2
        z2 = self.act.sigmoid(a2)
        a3 = z2@W3 + b3
        z3 = self.act.sigmoid(a3)
        y  = self.out.softmax(z3)
        
        return y
    
    def calc_accuracy(self):
        x, t    = self.get_data() #特徴量,答え
        self.network = self.init_network() 
        
        accuracy_cnt = 0
        
        for idx,xi in enumerate(x):
            #1データずつ予測
            h = self.predict(self.network,xi)
            #最も評価値の高いクラスを計算
            p = np.argmax(h)
            print(p)
            
            if p == t[idx]:
                accuracy_cnt += 1
        
        print("Accuracy:" + str(float(accuracy_cnt) / len(x)))
        
    def calc_accuracy_batch(self,batch_size):
        #x　：　10000×784
        #t　：　10000×1

        x, t    = self.get_data() #特徴量,答え
        self.network = self.init_network()
        
        accuracy_cnt = 0
        
        for i in range(0, len(x), batch_size):
            
            #x_batch　：　batch_size×784
            x_batch = x[i : i+batch_size]

            #h_batch ： batch_size×10
            h_batch = self.predict(self.network, x_batch)
            
            #p ： batch_size×1
            p = np.argmax(h_batch,axis=1)
            #print(p)
            
            #Trueの個数をカウントする
            accuracy_cnt += np.sum(p == t[i:i+batch_size])
        
        print("Accuracy:" + str(float(accuracy_cnt) / len(x)))        

#%%
#mnist = MNIST_net()
#res = mnist.calc_accuracy_batch(20)