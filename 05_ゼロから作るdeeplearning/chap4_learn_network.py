# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 12:04:51 2019

@author: p000495138
"""
import numpy as np
import matplotlib.pyplot as plt

import load_mnist
import chap3_neuralnetwork as cp3

from common import functions as cmfuncs
from common import gradient as cmgrads

#%%　誤差計算関数
class CalcErr:
    def __init__(self):
        pass
    
    #2乗誤差
    def mean_squared_error(self,y,t):
        return 0.5 * np.sum((y-t)**2)
    
    #交差エントロピー
    def cross_entropy_error(self,y,t):
        delta = 1e-7
        return -np.sum(t*np.log(y+delta))
    
    #交差エントロピー(複数データ)
    def cross_entropy_error2(self,y,t):
        
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

#%%　誤差計算関数
class MNIST_net2(cp3.MNIST_net):
    def __init__(self):
        pass
    
    def get_train_data(self):
        (self.x_train, self.t_train),(self.x_test, self.t_test) = load_mnist.load_mnist(normalize=False,one_hot_label = True)
        return self.x_train,self.t_train

    def get_test_data(self):
        (self.x_train, self.t_train),(self.x_test, self.t_test) = load_mnist.load_mnist(normalize=False,one_hot_label = True)
        return self.x_test,self.t_test

#%%勾配法
        
class Gradient_descent:
    def __init__(self):
        pass
    
    #数値微分
    def numerical_diff(self,f,x):
        h = 1e-4 # 0.0001
        return (f(x+h) - f(x-h))/(2*h)
    
    #サンプル：1変数関数
    def function_1(self,x):
        return 0.01*x**2 + 0.1*x


    #サンプル：2変数関数
    def function_2(self,x):
        return x[0]**2 + x[1]**2 #+ x[0]*x[1]
        
    #片側固定化
    def function_tmp1(self,x0):
        return x0**2    + 4.0**2
    def function_tmp2(self,x1):
        return 3.0**2.0 + x1**2

    #ベクトルの勾配計算
    def numerical_gradient_1d(self,f,x):
        #print("xのサイズ= ",x.shape)
        h = 1e-4 #0.001
        grad = np.zeros_like(x)
            
        for idx in range(x.size):
            tmp_val = x[idx]
            #f(x+h)の計算
            x[idx] = tmp_val + h
            fxh1   = f(x)
            #f(x+h)の計算
            x[idx] = tmp_val - h
            fxh2   = f(x)            

            grad[idx] = (fxh1 - fxh2) / (2*h)
            x[idx]    = tmp_val
            
        return grad

    #配列の勾配計算
    def numerical_gradient(self,f_loss, param):
        
        """
        paramは参照であることに注意!!
        """
        
        h = 1e-4 #0.001
        grad = np.zeros_like(param)
        
        it = np.nditer(param ,flags=["multi_index"], op_flags=["readwrite"])
        
        while not it.finished:
            
            idx = it.multi_index                        
            print(idx)
            tmp_val = param[idx]
            
            #パラメータの要素を一つ動かす
            param[idx] = float(tmp_val) + h
            fxh1   = f_loss(param)
            
            #パラメータの要素を一つ動かす
            param[idx] = float(tmp_val) - h
            fxh2   = f_loss(param)            
            
            grad[idx] = (fxh1 - fxh2) / (2*h)
            
            param[idx] = tmp_val
            it.iternext()
            
        return grad


    #勾配降下法
    def gradient_descent(self,f, init_x, lr=0.01, step_num=100):
        x = init_x
        progress = []

        for i in range(step_num):
            grad = self.numerical_gradient(f,x)
            x    -= lr * grad
            progress.append(x.copy())
        return x,progress

#%%　1層
class simpleNet:
    
    def __init__(self):
        self.W = np.random.randn(2,3)
        self.err_obj = CalcErr()
        self.out_obj = cp3.Output()
        
    def predict(self,x):
        return x@self.W
    
    def loss(self, x, t):
        z = self.predict(x)
        y = self.out_obj.softmax2(z)
        loss = self.err_obj.cross_entropy_error2(y,t)
        
        return loss

#%%　2層
class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        #重みの初期化
        self.params = {}
        self.params["W1"] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params["b1"] = np.zeros(hidden_size)
        self.params["W2"] = weight_init_std * np.random.randn(hidden_size, output_size)        
        self.params["b2"] = np.zeros(output_size)
        
        #使う関数類
        self.act = cp3.Activation()
        self.out = cp3.Output()
        self.err = CalcErr()
        self.grad = Gradient_descent()

    def predict(self,x):
        W1, W2 = self.params["W1"], self.params["W2"]
        b1, b2 = self.params["b1"], self.params["b2"]
        
        a1 = x@W1 + b1
        #z1 = self.act.sigmoid(a1)
        z1  = cmfuncs.sigmoid(a1)
        a2 = z1@W2 + b2
        #z2 = self.act.sigmoid(a2)
        z2 = cmfuncs.sigmoid(a2)
        #y  = self.out.softmax(z2)
        y = cmfuncs.softmax(z2)
        
        return y
    
    #x:入力,t:正解ラベル
    def loss(self,x,t):
        y = self.predict(x)
        
        #return self.err.cross_entropy_error2(y,t)
        return cmfuncs.cross_entropy_error(y,t)
    
    def accuracy(self,x,t):
        y = self.predict(x)
        y = np.argmax(y,axis=1)
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
        
        def sigmoid_grad(x):
            return (1.0 - self.act.sigmoid(x)) * self.act.sigmoid(x)
        
        W1, W2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']
        grads = {}
        
        batch_num = x.shape[0]
        
        # forward
        a1 = np.dot(x, W1) + b1
        z1 = self.act.sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = self.out.softmax2(a2)
        
        # backward
        dy = (y - t) / batch_num
        grads['W2'] = np.dot(z1.T, dy)
        grads['b2'] = np.sum(dy, axis=0)
        
        dz1 = np.dot(dy, W2.T)
        da1 = sigmoid_grad(a1) * dz1
        grads['W1'] = np.dot(x.T, da1)
        grads['b1'] = np.sum(da1, axis=0)

        return grads



#%%誤差計算
print("------誤差計算練習------")
#1データ
err=CalcErr()
t=[0,  0,   1,  0,  0,   0,  0,  0,  0,  0] #one_hot
y=[0.1,0.05,0.6,0.0,0.05,0.1,0.0,0.1,0.0,0.0]
res = err.cross_entropy_error(np.array(y),np.array(t))
print("クロスエントロピー誤差：",res)

#複数データ(バッチ処理)
mnist2 = MNIST_net2()
x_train, t_train = mnist2.get_train_data()

train_idx = np.random.choice(x_train.shape[0],10)
t_batch   = t_train[train_idx,:]
y_batch   = np.abs(np.random.randn(10,10))
err2      = err.cross_entropy_error2(y_batch,t_batch)
print("誤差のバッチ計算 ",err2)

#%%勾配降下法
print("\n\n------勾配計算練習------")
g = Gradient_descent()

#偏微分：変数固定
g.numerical_diff(g.function_tmp1,3.0)
g.numerical_diff(g.function_tmp2,4.0)

#偏微分:勾配ベクトル
vec = g.numerical_gradient(g.function_2, np.array([8.0, 4.0]))
print("勾配ベクトル:",vec)

#勾配降下法
init_x = np.array([-3.0, 4.0])
res,progress = g.gradient_descent(g.function_2, init_x, lr=1e-2, step_num=100)
print("最も勾配が小さくなるのは," ,res)
#plt.plot(progress)

#%%simpleNetの計算
print("\n\n------1層ネットワーク------")
net = simpleNet()
grad = Gradient_descent()

print("\n ## 順方向計算 ##")
print("ネットワークの重み：",net.W)
x = np.array([0.6, 0.9])
p = net.predict(x)
print("予測結果：",p)
print("最大値のインデックス：",np.argmax(p))
t = np.array([0,0,1])
print("正解ラベル：",t)
print("誤差：",net.loss(x,t))

print("\n ## 勾配計算 ##")
def f(W):
    return net.loss(x,t)
dW = grad.numerical_gradient(f, net.W)
print("勾配：",dW)


#%%TwoLayerNetの計算 
print("\n\n------2層ネットワーク------")
net = TwoLayerNet(input_size=784, hidden_size=100, output_size=10)

print("\n ## パラメータサイズ ##")
print("W1サイズ=",net.params["W1"].shape)
print("b1サイズ=",net.params["b1"].shape)
print("W2サイズ=",net.params["W2"].shape)
print("b2サイズ=",net.params["b2"].shape)

print("\n ## 推論処理(ダミーデータ) ##")
x = np.random.rand(100,784)
y = net.predict(x)

print("\n ## 勾配計算(ダミーデータ) ##")
t = np.random.rand(100,10)
#grads = net.numerical_gradient(x,t)

#%%TwoLayerNetの計算（手書き文字認識）

#記録用
mnist2 = MNIST_net2()
x_train, t_train = mnist2.get_train_data()
x_test,  t_test  = mnist2.get_test_data()

#記録用
train_loss_list = []
train_acc_list = []
test_acc_list = []

#ハイパーパラメータ
iters_num = 10000
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.1

#1エポックあたりの繰り返し数
iter_per_epoch = max(train_size/batch_size,1)

#学習
net2 = TwoLayerNet(input_size=784, hidden_size=100, output_size=10)
for i in range(iters_num):
    
    print(i)
    
    #ミニバッチ取得
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch    = x_train[batch_mask]
    t_batch    = t_train[batch_mask]
    
    ##勾配計算
    #grad = net2.numerical_gradient(x_batch,t_batch)
    grad = net2.gradient(x_batch,t_batch)
    
    #パラメータ更新
    for key in ("W1","b1","W2","b2"):
        net2.params[key] = net2.params[key] - learning_rate * grad[key]
        
    #経過記録
    loss = net2.loss(x_batch,t_batch)
    train_loss_list.append(loss)
    
    #1エポックごとに認識精度を計算
    if i % iter_per_epoch == 0:
        train_acc = net2.accuracy(x_train,t_train)
        test_acc  = net2.accuracy(x_test,t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + "," + str(test_acc))

plt.plot(train_loss_list)
