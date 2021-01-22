# -*- coding: utf-8 -*-
"""
Q学習法
Qをアップデートする方法を学ぶ(方策の選択はやらない)
(p.42～)
"""

import numpy as np
import pandas as pd

table = pd.DataFrame(np.zeros([4,4]))
table.columns = ["up","down","left","right"]
table.index   = ["S1","S2","S3","S4"]

REWARDS = {"S1":-1,"S2":-1,"S3":-1,"S4":10}

ALPHA = 0.7
GAMMA = 0.9

#%% テーブルのアップデート
def update(table, S_from, S_to, move):

    #各項の計算
    q1 = max(table.loc[S_to])
    q2 = table.loc[S_from, move]
    r  = REWARDS[S_from]

    #アップデートする値    
    tmp = ALPHA*(r + GAMMA*q1) + (1-ALPHA)*q2
    
    #アップデート
    table.loc[S_from, move] = tmp
    
    return table

#%%初期状態
print(table)

#%%step1
S_from = "S1"
move  = "up"
S_to   = "S2"
update(table, S_from, S_to, move)
print(table)

#%%step2
S_from = "S2"
move  = "right"
S_to   = "S3"
update(table, S_from, S_to, move)
print(table)

#%%step3
S_from = "S3"
move  = "right"
S_to   = "S3"
update(table, S_from, S_to, move)
print(table)

#%%step4
S_from = "S3"
move  = "down"
S_to   = "S4"
update(table, S_from, S_to, move)
print(table)

#%%step5
S_from = "S4"
move  = "left"
S_to   = "S4"
update(table, S_from, S_to, move)
print(table)

#%%step6
S_from = "S4"
move  = "up"
S_to   = "S3"
update(table, S_from, S_to, move)
print(table)

#%%step7
S_from = "S3"
move  = "down"
S_to   = "S4"
update(table, S_from, S_to, move)
print(table)