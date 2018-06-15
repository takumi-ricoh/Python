# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 21:24:49 2018

@author: p000495138
"""

#全データ
import csv
import numpy as np

#リストで呼んで、np.array
def read_data(file):
    data=[]
    with open(file, 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
    
        for row in reader:
            data.append(row)          # 1行づつ取得できる
    
        return data


data1 = read_data("input1.csv")
data1_np = np.array(data1[1:],dtype=np.float32)

data2 = read_data("input2.csv")
data2_np = np.array(data2[1:],dtype=np.float32)

result = (data1_np + data2_np)/2

with open("ouput.csv",'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(result)