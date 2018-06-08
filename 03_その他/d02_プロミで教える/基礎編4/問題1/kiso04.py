# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:21:24 2018

@author: p000495138
"""
#全データ
data=[]
with open('input.txt','r') as f:
    for row in f:
        data.append(row)

#俺はを含むもの
data2=[]
for word in data:
    if "俺は" in word:
        tmp = word.split("、")[1].strip()
        data2.append(tmp)

#名前を追加
data3=[]
for word in data2:
    tmp = "私は、" + word + "です。\n"
    data3.append(tmp)

#保存
with open('output.txt','a') as f:
    for i in data3:
        f.write(i)
