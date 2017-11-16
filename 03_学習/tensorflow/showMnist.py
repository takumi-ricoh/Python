# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 15:05:51 2017

@author: p000495138
"""


import matplotlib.pyplot as plt

img = mnist.train.images
label = mnist.train.labels
n=150
img2 = img[0:n,:]

fig = plt.figure()
ax=[]
plots=[]
ydata=[]
img_list=[]

label2=[]
for i in range(n):
    image = img2[i,:].reshape([28,28])
    plt.subplot(int(n/15),15,i+1)
    plt.imshow(image,cmap='gray')
    plt.tick_params(labelbottom="off")
    plt.tick_params(labelleft='off')
    
    img_list.append(image)
    
    for j in range(10):
        if label[i,j] != 0:
            label2.append(j)

plt.figure(2)
plt.plot(label2,".-")