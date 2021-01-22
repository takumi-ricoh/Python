# -*- coding: utf-8 -*-
"""
torchの関数群について
"""
import torch
import torch.nn.functional as f
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

import numpy as np

#%% modules
a = dir(torch)

b = dir(torch.nn)

c = dir(torch.nn.functional)

d = dir(torch.optim)

#%% loaders = load_MNIST()

def load_MNIST(batch=128, intensity=1.0):
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('./data',
                       train=True,
                       download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Lambda(lambda x: x * intensity)
                       ])),
        batch_size=batch,
        shuffle=True)
 
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('./data',
                       train=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Lambda(lambda x: x * intensity)
                       ])),
        batch_size=batch,
        shuffle=True)
 
    return {'train': train_loader, 'test': test_loader}

loaders = load_MNIST()
a = list(loaders["train"])
b = a[1][0][0][0]
plt.imshow(b)

#%% data.view

a = np.eye(3)
print(a.shape)

b = torch.tensor(a)
print(b.shape)

c = b.view(-1,9)
print(c.shape)

#%% torch.sigmoid

x1 = torch.tensor(-100.0)
x2 = torch.tensor(0.0)
x3 = torch.tensor(100.0)

a = print(float(torch.sigmoid(x1)))
b = print(float(torch.sigmoid(x2)))
c = print(float(torch.sigmoid(x3)))

#%% f.nll_loss

# input is of size N x C = 3 x 5
d_input = torch.randn(3, 5, requires_grad=True)

# each element in target has to have 0 <= value < C
target = torch.tensor([1, 0, 4])
output = f.nll_loss(f.log_softmax(d_input), target)
output.backward()

#%% torch.nn.Linear
m = torch.nn.Linear(20, 30)

d_input = torch.randn(128, 20)
print(d_input.size())

output = m(d_input)
print(output.size())

#%% optimizer.zero_grad()
f = torch.optim.Adam.zero_grad
help(f)

#%% nn.Module
class MyNet(torch.nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        self.fc1 = torch.nn.Linear(28*28, 1000)
        self.fc2 = torch.nn.Linear(1000, 10)
 
    def forward(self, x):
        x = self.fc1(x)
        x = torch.sigmoid(x)
        x = self.fc2(x)
 
        return f.log_softmax(x, dim=1)
    
net = MyNet()
print(net)