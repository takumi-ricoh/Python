# -*- coding: utf-8 -*-
"""
★価値反復法

行動を追加する

↓

現在の状態から、最適な(Qが最大となる)アクションを取り続けた場合に、
どのような状態価値(v)に収束するか、がわかる

こうして、Value Iterationにより「環境のみから」報酬マップを推定することができました。
ただ、この状態だとすべての状況に置けるすべての行動をしらみつぶしに調べていることになるので、
最適な行動は導けますがあまり効率が良くありません。そのため、まず適当な戦略を決めてしまって、
その範囲で報酬の探索を行い、更新していくという手法を考えます。それがPolicy Iterationです。

"""
import numpy as np
import pandas as pd

#%% MDPモデル

#状態遷移確率

#move(eat or hunt)
TM_m=[[0.0, 0.9, 0.0, 0.1],
   [0.2, 0.0, 0.8, 0.0],
   [0.0, 0.0, 0.0, 1.0],
   [0.0, 0.0, 0.0, 1.0]]
TM_m=pd.DataFrame(TM_m)
TM_m.columns=["Ht","Gt","Ft","Dt"]
TM_m.index=["H","G","F","D"]

#sleep
TM_s=[[0.7, 0.0, 0.0, 0.3],
   [0.2, 0.8, 0.0, 0.0],
   [1.0, 0.0, 0.0, 0.0],
   [0.0, 0.0, 0.0, 1.0]]
TM_s=pd.DataFrame(TM_s)
TM_s.columns=["Ht","Gt","Ft","Dt"]
TM_s.index=["H","G","F","D"]

#確率まとめ
TM = {"move":TM_m, "sleep":TM_s}

#報酬
RW = {"H":0, "G":1, "F":10, "D":-10}

#割引率
GAMMA = 0.9

#%% Q(s=H,a)
def calcQ(v, state, action):

    #今の報酬
    r = RW[state]

    #state → ある状態への確率
    p={}
    p["Ht"] = TM[action].loc[state,"Ht"]
    p["Gt"] = TM[action].loc[state,"Gt"]
    p["Ft"] = TM[action].loc[state,"Ft"]
    p["Dt"] = TM[action].loc[state,"Dt"]    
    
    #vの計算  Bellman方程式(報酬の総和を計算)
    Q = r + GAMMA*(p["Ht"]*v["H"]
                  +p["Gt"]*v["G"]
                  +p["Ft"]*v["F"]
                  +p["Dt"]*v["D"])
    return Q

#%%状態価値の計算

#初期状態
v = [RW]

#繰り返し
for i in range(100):

    #初期化
    Q = {"H":{"move":0,"sleep":0},
         "G":{"move":0,"sleep":0},
         "F":{"move":0,"sleep":0},
         "D":{"move":0,"sleep":0},}
    Q_best ={"H":0, "G":0, "F":0, "D":0}
    
    #状態×アクションごとのQを計算し、状態ごとに最大となるアクションを選択
    #すべての状況に置けるすべての行動をしらみつぶしに調べている
    for state in ["H","G","F","D"]:
        #各アクションごとに計算
        for action in ["move","sleep"]:
            Q[state][action] = calcQ(v[-1],state,action)

        #Qの大きい方を取る(大きくなるactionを選択)
        Q_best[state] = max(Q[state].values())

    #vを更新
    v.append(Q_best)