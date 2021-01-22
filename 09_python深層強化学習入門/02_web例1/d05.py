# -*- coding: utf-8 -*-
"""
★Q学習
https://qiita.com/icoxfog417/items/242439ecd1a477ece312

・d02でモデルが未知とする
・Q学習する
・
"""

import numpy as np
import pandas as pd

#%% 対象(エージェントからは状態遷移確率tmは見えない)
class World:
    
    #move
    tm_m=[[0.0, 0.9, 0.0, 0.1],
       [0.2, 0.0, 0.8, 0.0],
       [0.0, 0.0, 0.0, 1.0],
       [0.0, 0.0, 0.0, 1.0]]
    
    #sleep
    tm_s=[[0.7, 0.0, 0.0, 0.3],
       [0.2, 0.8, 0.0, 0.0],
       [1.0, 0.0, 0.0, 0.0],
       [0.0, 0.0, 0.0, 1.0]]

    #初期化
    def __init__(self):

        #状態遷移確率
        tm_m = self._todf_(World.tm_m)
        tm_s = self._todf_(World.tm_s)
        self.tm   = {"move":tm_m, "sleep":tm_s}
        
        #報酬
        self.rw   = {"H":0, "G":1, "F":10, "D":-10}

        #状態
        self.state = "H"

    #アクションした結果
    def action(self,action):
        #遷移確率の候補
        cand = self.tm[action].loc[self.state]
        #確率に従って遷移
        self.state = str(np.random.choice(["H", "G", "F", "D"], p=list(cand)))
        #報酬をリターン
        return self.rw[self.state]
        
    #pandasに変換
    def _todf_(self,data):
        tmp = pd.DataFrame(data)
        tmp.columns=["Ht","Gt","Ft","Dt"]
        tmp.index=["H","G","F","D"]
        return tmp

#%% Qテーブル
class Qtable:
    ALPHA = 0.7
    GAMMA = 0.9
    
    #初期化
    def __init__(self):
        self.Qtable = self._todf_(np.zeros([4,2]))

    #pandasに変換
    def _todf_(self,data):
        tmp = pd.DataFrame(data)
        tmp.columns=["move","sleep"]
        tmp.index=["H","G","F","D"]
        return tmp

    #アップデート
    def update(self,S_from, S_to, action, reward):

        #パラメータ
        alpha = Qtable.ALPHA
        gamma = Qtable.GAMMA
               
        #各項の計算
        q1 = max(self.Qtable.loc[S_to])
        q2 = self.Qtable.loc[S_from, action]
        r  = reward
    
        #アップデートする値    
        tmp = alpha*(r + gamma*q1) + (1-alpha)*q2
        
        #アップデート
        self.Qtable.loc[S_from, action] = tmp
        
#%%Qテーブルをもとに、探索&最適方策を取る

#MDP初期化
world = World()
#Qテーブル初期化
q     = Qtable()
#εを設定
epsilon = 0.2

#結果保存
res = []

#学習フェーズ
for j in range(100):
    #スタート位置を初期化
    world.state = "H"

    for i in range(10):
        #実行前の状態を確認する
        state_old = world.state
    
        #最適方策を決める(ε-greedy)
        if  epsilon <= np.random.uniform(0, 1):
            action = q.Qtable.loc["H"].idxmax()
        else:
            action = str(np.random.choice(["move","sleep"]))
        
        #実際に行動し報酬を受取る
        r = world.action(action)
        
        #実行後の状態を確認する
        state_new = world.state
        
        #qテーブルを更新する
        q.update(state_old, state_new, action, r)
        
        #結果保存
        res.append([j,i,state_old,state_new,action,r])

        #もしdeadに落ちこんだら終了する
        if state_new == "D":
            break

print(q.Qtable)