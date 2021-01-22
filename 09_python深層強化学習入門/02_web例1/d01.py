# -*- coding: utf-8 -*-
"""

行動なし（状態のみ）の遷移計算(p.18)

"""

import numpy as np
import pandas as pd


#%% MDPモデル

#状態遷移確率(● → ●tへの確率)
TM=[[0.5, 0.4, 0.0, 0.1],
   [0.2, 0.1, 0.6, 0.1],
   [0.9, 0.0, 0.0, 0.1],
   [0.0, 0.0, 0.0, 1.0]]
TM=pd.DataFrame(TM)
TM.columns=["Ht","Gt","Ft","Dt"]
TM.index=["H","G","F","D"]

#報酬
RW = {"H":0, "G":1, "F":10, "D":-10}

#割引率
GAMMA = 0.9

#%% v(s=H)
def v_state(v, state):
    #今の報酬
    r = RW[state]
    #state → ある状態への確率
    p={}
    p["Ht"] = TM.loc[state,"Ht"]
    p["Gt"] = TM.loc[state,"Gt"]
    p["Ft"] = TM.loc[state,"Ft"]
    p["Dt"] = TM.loc[state,"Dt"]    
    #vの計算
    v_state = r + GAMMA*(p["Ht"]*v["H"]
                  +p["Gt"]*v["G"]
                  +p["Ft"]*v["F"]
                  +p["Dt"]*v["D"])
    return v_state

#%%状態価値の計算

#初期状態
v = [RW]

#繰り返し
for i in range(100):
    #各状態ごとに更新
    v_new = v[-1].copy()
    for state in ["H","G","F","D"]:
        v_new[state] = v_state(v[-1], state)
    #vを更新
    v.append(v_new)