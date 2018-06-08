# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 10:03:29 2018

@author: p000495138
"""

import glob

#%%　元データ読み込み
filename = glob.glob("*.txt")[0]

data0 = []
with open(filename,"r") as f:
    for row in f:
        data0.append(row.strip())

data0.pop(0)  #1つ目は消しておく
data0.pop(-1) #最後も消しておく

#%% タイプスタンプ削除

data1 = []

for i in data0:
    tmp = i.split("2018] ")
    if len(tmp) > 1:
        data1.append(tmp[1])

#%% 「電源ＯＮ・・・」のインデックス取得
index = []

for idx,i in enumerate(data1):
    if "電源ONによるリセット" in i:
        index.append(idx)

#%% データ分割
job0 = data1[index[0] : index[1]-1]
job1 = data1[index[1] : index[2]-1]
job2 = data1[index[2] : index[3]-1]
job3 = data1[index[3] : index[4]-1]
job4 = data1[index[4] : ]    

jobs = [job0, job1, job2, job3, job4]

#%% ファイル保存
for idx,job in enumerate(jobs):
    savename = "result/" + filename + "_job" + str(idx) + ".txt"
    with open(savename, "w") as f:
        #1行ずつ書き出す
        for line in job: 
            f.write(line + "\n")
