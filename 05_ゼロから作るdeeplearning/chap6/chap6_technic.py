# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:27:44 2019

@author: p000495138
"""

import numpy as np
from mnist import load_mnist
import matplotlib.pyplot as plt

#%%アクティベーション関数

#シグモイド関数
def sigmoid(self,x):
     y = 1 / (1+np.exp(-x))
     return y

#%%出力関数
def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T 
    
    x = x - np.max(x) # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x))


#%%誤差計関数
def cross_entropy_error(y,t):
    
    #ベクトルの場合は行列に変換
    if y.ndim == 1:
        t = t.reshape(1,t.size)
        y = y.reshape(1,y.size)
    
    #データ数
    batch_size = y.shape[0]
    
    # 教師データがone-hot-vectorの場合、正解ラベルのインデックスに変換
    if t.size == y.size:
        t = t.argmax(axis=1)        
    
    #教師ラベルがインデックスそのものの場合
    result = -np.sum(np.log( y[np.arange(batch_size),t] + 1e-7 ))/batch_size
    
    return result


#%% 学習用クラス
class Momentum:
    def __init__(self,lr=0.01,momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None
        
    def update(self,params,grads):
        if self.v is None:
            self.v = {}
            for key, val in params.items():
                self.v[key] = np.zeros_like(val)

        for key in params.keys():
            self.v[key] = self.momentum*self.v[key] - self.lr*grads[key]
            params[key] += self.v[key]

#%% 学習用クラス
class AdaGrad:
    def __init__(self,lr=0.01):
        self.lr = lr
        self.v = None
        
    def update(self,params,grads):
        if self.v is None:
            self.v = {}
            for key, val in params.items():
                self.v[key] = np.zeros_like(val)

        for key in params.keys():
            self.h[key] +=  grads[key] * grads[key]
            params[key] -= self.lr * grads[key] / (np.sqrt(self.h[key]) + 1e-7)

#%% 学習用クラス
class Adam:

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.iter = 0
        self.m = None
        self.v = None
        
    def update(self, params, grads):
        if self.m is None:
            self.m, self.v = {}, {}
            for key, val in params.items():
                self.m[key] = np.zeros_like(val)
                self.v[key] = np.zeros_like(val)
        
        self.iter += 1
        lr_t  = self.lr * np.sqrt(1.0 - self.beta2**self.iter) / (1.0 - self.beta1**self.iter)         
        
        for key in params.keys():
            #self.m[key] = self.beta1*self.m[key] + (1-self.beta1)*grads[key]
            #self.v[key] = self.beta2*self.v[key] + (1-self.beta2)*(grads[key]**2)
            self.m[key] += (1 - self.beta1) * (grads[key] - self.m[key])
            self.v[key] += (1 - self.beta2) * (grads[key]**2 - self.v[key])
            
            params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + 1e-7)

#%% 乗算レイヤの実装
class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None
    
    def forward(self,x,y):
        self.x = x
        self.y = y
        out = self.x*self.y
        return out 
    
    def backward(self,dout):
        dx = dout * self.y
        dy = dout * self.x
        
        return dx,dy

#%%加算レイヤの実装
class AddLayer:
    def __init__(self):
        pass
    
    def forward(self,x,y):
        out = x+y
        return out 
    
    def backward(self,dout):
        dx = dout * 1
        dy = dout * 1
        
        return dx,dy    

#%%Reluレイヤの実装
class Relu:
    def __init__(self):
        self.mask = None
    
    def forward(self,x):
        self.mask = (x<=0)
        out = x.copy()
        out[self.mask] = 0
        return out
    
    def backward(self,dout):
        dout[self.mask] = 0
        dx = dout
        return dx    

#%%Sigmoidレイヤの実装
class Sigmoid:
    def __init__(self):
        self.out = None
    
    def forward(self,x):
        out = 1 / (1 + np.exp(-x))
        self.out = out
        return out
    
    def backward(self,dout):
        dx = dout * (1.0 - self.out) * self.out
        return dx

#%%Affineレイヤの実装
class Affine:
    def __init__(self,W,b):
        self.W = W
        self.b = b
        self.x = None
        self.dW = None
        self.db = None
        
    def forward(self,x):
        self.x = x
        out = x @ self.W + self.b
        return out
    
    def backward(self,dout):
        dx = dout @ self.W.T
        self.dW = self.x.T @ dout
        self.db = np.sum(dout, axis=0)
        
        return dx

#%%Solfmax-with-Lossレイヤ
class SoftmaxwithLoss:
    def __init__(self):
        self.loss = None
        self.y = None #出力
        self.t = None #教師(one-hot)
        
    def forward(self,x,t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y,self.t)
        return self.loss
    
    def backward(self,dout=1):
        batch_size = self.t.shape[0]
        dx = (self.y - self.t) / batch_size
        return dx


#%%ニューラルネット
class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        #重みの初期化
        self.params = {}
        self.params["W1"] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params["b1"] = np.zeros(hidden_size)
        self.params["W2"] = weight_init_std * np.random.randn(hidden_size, output_size)        
        self.params["b2"] = np.zeros(output_size)
        
        #レイヤ作成
        self.layers = {}
        self.layers["Affine1"] = Affine(self.params["W1"], self.params["b1"])
        self.layers["Relu"]    = Relu()
        self.layers["Affine2"] = Affine(self.params["W2"], self.params["b2"])
        self.lastLayer = SoftmaxwithLoss()

    def predict(self,x):
        for layer in self.layers.values():
            #xｆが更新されて、次のレイヤに入力される。
            #なので、layerの順序が重要
            x = layer.forward(x)
                    
        return x
    
    #x:入力,t:正解ラベル
    def loss(self,x,t):
        y = self.predict(x)
        return self.lastLayer.forward(y,t)
    
    def accuracy(self,x,t):
        y = self.predict(x)
        y = np.argmax(y,axis=1)        
        if t.ndim != 1:            
            t = np.argmax(t,axis=1)        
        accuracy = np.sum(y==t) / float(x.shape[0])
        return accuracy
    
    def numerical_gradient(self,x,t):
        #入力は無視される。
        f_loss = lambda dummy: self.loss(x,t)        
        grads={}        
        grads["W1"] = self.grad.numerical_gradient(f_loss, self.params["W1"])
        grads["b1"] = self.grad.numerical_gradient(f_loss, self.params["b1"])
        grads["W2"] = self.grad.numerical_gradient(f_loss, self.params["W2"])
        grads["b2"] = self.grad.numerical_gradient(f_loss, self.params["b2"])
        return grads

    def gradient(self, x, t):

        """
        x：各層のパラメータ
        for・・・のところで1層ずつさかのぼる。(xが切り替わる)
        そして、それをbackwardで誤差逆伝搬する
        """
        # forward
        self.loss(x,t)
        
        # backward
        dout = 1
        dout = self.lastLayer.backward(dout)
        
        #順番を逆転する。一旦リストにコピーし、reverseする
        layers = list(self.layers.values())
        layers.reverse()
        #逆伝搬したものがdout。これを更新して次の引数にする。
        for layer in layers:
            dout = layer.backward(dout)

        grads ={}
        grads['W1'] = self.layers["Affine1"].dW
        grads['b1'] = self.layers["Affine1"].db
        grads['W2'] = self.layers["Affine2"].dW
        grads['b2'] = self.layers["Affine2"].db
    
        return grads
    

#%%Momentum最適化



#%%学習実行

#データ読み込み
(x_train, t_train),(x_test, t_test) = load_mnist.load_mnist(normalize=True, one_hot_label=True)

#ニューラルネット作成
network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

#ハイパーパラメータ
iters_num=10000
train_size = x_train.shape[0]
batch_size=100
learning_rate=0.1

#記録用
train_loss_list = []
train_acc_list = []
test_acc_list = []


#1エポックあたりの繰り返し数
iter_per_epoch = max(train_size/batch_size,1)

#インスタンス
fig,ax = plt.subplots()
lines1, = ax.plot(np.array([1]),[1],".-")
lines2, = ax.plot(np.array([1]),[1],".-")
ax.set_ylim(0,1)

#最適化計算
optimizer = Momentum()

for i in range(iters_num):
    
    #print(i)
    
    #ミニバッチ取得
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch    = x_train[batch_mask]
    t_batch    = t_train[batch_mask]
    
    ##勾配計算
    grad = network.gradient(x_batch,t_batch)
    
    #パラメータ更新

#    if i==0:
#        for key in ("W1","b1","W2","b2"):
#            network.params[key] -= learning_rate * grad[key]
#    else:
#        network.params = optimizer.update(network.params,grad)
     
    for key in ("W1","b1","W2","b2"):
         network.params[key] -= learning_rate * grad[key]
    
        
    #経過記録
    loss = network.loss(x_batch,t_batch)
    train_loss_list.append(loss)
    
    #1エポックごとに認識精度を計算
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train,t_train)
        test_acc  = network.accuracy(x_test,t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + "," + str(test_acc))

        #プロット更新
        data1 = train_acc_list
        data2 = test_acc_list
        x1=np.linspace(0,len(data1)-1,len(data1))
        x2=np.linspace(0,len(data2)-1,len(data2))
        lines1.set_data(x1,data1)
        lines2.set_data(x2,data2)
        ax.set_xlim((x1.min(), x1.max()))
        plt.grid(True)
        plt.pause(0.01)
        
#    #プロット更新
#    x=np.linspace(0,len(train_loss_list)-1,len(train_loss_list))
#    lines.set_data(x,train_loss_list)
#    ax.set_xlim((x.min(), x.max()))
#    plt.pause(0.01)