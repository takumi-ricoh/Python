# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:27:44 2019

@author: p000495138
"""

import numpy as np
from mnist import load_mnist

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
    
    def forward(self,x,y):
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
    
    def forward(self,x,y):
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
        return cross_entropy_error(y,t)
    
    def accuracy(self,x,t):
        y = self.predict(x)
        y = np.argmax(y,axis=1)        
        if t.nedim != 1:            
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
    
#%%確認１
print("\n\n---確認1---")
apple = 100
apple_num = 2
tax = 1.1

#layer
mul_apple_layer = MulLayer()
mul_tax_layer   = MulLayer()

#forward
apple_price = mul_apple_layer.forward(apple,apple_num)
price       = mul_tax_layer.forward(apple_price,tax)
print(price)

#backward
dprice = 1
dapple_price, dtax = mul_tax_layer.backward(dprice)
dapple,dapple_num  = mul_apple_layer.backward(dapple_price)
print(dapple,dapple_num,dtax)


#%%確認１
print("\n\n---確認2---")
apple = 100
apple_num = 2
orange = 150
orange_num = 3
tax = 1.1

#layer
mul_apple_layer    = MulLayer()
mul_orange_layer   = MulLayer()
add_apple_orange_layer = AddLayer()
mul_tax_layer      = MulLayer()

#forward
apple_price  = mul_apple_layer.forward(apple,apple_num)
orange_price = mul_apple_layer.forward(orange,orange_num)
all_price    = add_apple_orange_layer.forward(apple_price,orange_price)
price        = mul_tax_layer.forward(all_price,tax)
print(price)

#backward
dprice = 1
dapple_price, dtax = mul_tax_layer.backward(dprice)
dapple,dapple_num  = mul_apple_layer.backward(dapple_price)
print(dapple,dapple_num,dtax)

#%%確認１
print("\n\n---確認2---")
apple = 100
apple_num = 2
orange = 150
orange_num = 3
tax = 1.1

#layer
mul_apple_layer    = MulLayer()
mul_orange_layer   = MulLayer()
add_apple_orange_layer = AddLayer()
mul_tax_layer      = MulLayer()

#forward
apple_price  = mul_apple_layer.forward(apple,apple_num)
orange_price = mul_apple_layer.forward(orange,orange_num)
all_price    = add_apple_orange_layer.forward(apple_price,orange_price)
price        = mul_tax_layer.forward(all_price,tax)
print(price)

#backward
dprice = 1
dapple_price, dtax = mul_tax_layer.backward(dprice)
dapple,dapple_num  = mul_apple_layer.backward(dapple_price)
print(dapple,dapple_num,dtax)

#%%実行

#データ読み込み
(x_train, t_train),(x_test, t_test) = load_mnist.load_mnist(normalize=True, one_hot_label=True)

#ニューラルネット作成
network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

#ハイパーパラメータ
iters_num=10000
train_size = x_train.shape[0]
batch_size=100
learning_rate=0.1
