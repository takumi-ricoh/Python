# -*- coding: utf-8 -*-
"""
自宅、会社、バーを行き来する場合に、報酬を最大化する方策(行動)を選択する

例）　状態が「自宅」のとき、
　　　・行動として「move」を選択
　　　　　→　0.8の確率で会社へ行き、報酬は＋１
　　　　　→　0.2の確率でバーへ行き、報酬は＋２
　　　・行動として「stay」を選択     
   　　 →　1.0の確率で自宅にとどまり、報酬は0

"""


import numpy as np
import copy

res = {"v":[],"q":[],"pi":[]}

#%% 基本情報

#マルコフ決定過程
p = [0.8, 0.5, 1.0] 
"""
自宅 → 会社 ：確率0.8
会社 → バー ：確率0.8
バー　→ 自宅 ：確率0.8
"""

#割引率
gamma = 0.95

#報酬期待値
r = np.zeros((3,3,2))
r[0,1,0] = 1.0 #状態0→状態1 (自宅→会社) にmove(0)したとき報酬が1.0
r[0,2,0] = 2.0 #状態0→状態2 (自宅→バー)　にmove(0)したとき報酬が2.0
r[0,0,1] = 0.0 #状態0→状態0 (自宅→自宅) にstay(1)したとき報酬が0.0
r[1,0,0] = 1.0 #状態1→状態0 (会社→自宅) にmove(0)したとき報酬が1.0
r[1,2,0] = 2.0 #状態1→状態2 (会社→バー)　にmove(0)したとき報酬が2.0
r[1,1,1] = 1.0 #状態1→状態1 (会社→会社) にstay(1)したとき報酬が1.0
r[2,0,0] = 1.0 #状態1→状態0 (バー→自宅) にmove(0)したとき報酬が1.0
r[2,1,0] = 0.0 #状態1→状態2 (バー→会社)　にmove(0)したとき報酬が0.0
r[2,2,1] = -1.0 #状態1→状態1 (バー→バー) にstay(1)したとき報酬が-1.0

#価値関数の初期化
v = [0,0,0]
v_prev = copy.copy(v)

#行動価値関数の初期化
q = np.zeros((3,2))
"""
例) ｑ[0,0]:自宅からmoveする行動価値
    ｑ[1,1]:会社にstayする行動価値
    q[i,0] > q[i,1] なら、moveのほうが価値がある
"""

#方策確率分布の初期化
pi = [0.5, 0.5, 0.5] 
"""
#自宅からmoveする確率0.5
#会社からmoveする確率0.5、
#バーからmoveする確率0.5、
"""
#%%方策評価関数の定義
def policy_estimator(pi, p):
    
    
    #初期化
    R = [0,0,0] #報酬期待値
    P = np.zeros((3,3)) #状態遷移確率
    
    #状態遷移行列の計算
    def calc_P(pi,i):
        """
        1行目： stayする場合の状態遷移確率
        2行目： stayする場合の報酬期待値(状態i)
        """
        P[i,i] = 1 - pi[i] #対角成分の計算
        P[i, (i+1)%3] = p[i] * pi[i]
        P[i, (i+2)%3] = (1-p[i]) * pi[i]
        return P
    
    #報酬ベクトル計算
    def calc_R(pi,p,i):
        """
        方策piに従い、確率p、報酬rのもとで、報酬の期待値を計算
        1行目： moveする場合の報酬期待値(状態i)
        2行目： stayする場合の報酬期待値(状態i)
        """
        R[i] = pi[i] * (p[i]*r[i,(i+1)%3,0] + (1-p[i])*r[i,(i+2)%3,0]) \
                + (1-pi[i])*r[i,i,1]
        return R

    #ベルマン方程式を解いて、価値関数vを得る
    def calc_Berman(P,R):
        tmp1 = np.eye(3) - gamma*P
        tmp2 = np.linalg.inv(tmp1)
        v    = np.dot(tmp2,R)
        return v

    #実行:自宅、会社、バーの各状態について、PとRを計算する
    for i in range(3):
        P = calc_P(pi,i) #P行列のi行目を更新
        R = calc_R(pi,p,i) #Rベクトルのi番要素を更新
    
    v_sol = calc_Berman(P,R) #ベルマン方程式を解いて、価値ベクトルvを得る
    
    return v_sol
        
#%% 方策反復法
for step in range(100):
    """
    １．方策piのもとで、価値関数vを計算
        ・ベルマン方程式を解く
    ２．価値関数vをつかって、行動価値関数qを計算
    ３．行動価値関数同士を比較して、moveかstayを決める
    """
    
    #方策の評価
    v = policy_estimator(pi, p)
    
    #価値関数vが改善しなければ終了
    if np.min(v-v_prev) <= 0:
        break
    
    #現ステップの価値関数と方策を表示
    print("step:",step,"value:",v,"policy:",pi)
    
    #%%行動価値関数を計算
    def calc_q(pi,r,v,i):
        """
        状態iにおいて、
        q[i,0]  ：moveする場合の行動価値関数
                ★状態の遷移先が2つあるので、2行ある
        q[i,1]  ：stayする場合の行動価値関数
        """
        q[i,0] = p[i] * (r[i,(i+1)%3,0] + gamma*v[(i+1)%3])      \
                 + (1-p[i]) * (r[i,(i+2)%3,0] + gamma*v[(i+2)%3])
        
        q[i,1] = r[i,i,1] + gamma*v[i]
        
        return q
    
    #%%greedyに方策を改善
    def greedy(q,pi,i):
        if q[i,0] > q[i,1]: #moveの価値＞stayの価値 →　方策をmoveに
            pi[i] = 1
            
        elif q[i,0] == q[i,1]: #moveの価値==stayの価値 →　方策はイーブンに
            pi[i] = 0.5

        else:              #moveの価値＜stayの価値 →　方策をstayに
            pi[i] = 0
        return pi
    
    #%%実行
    for i in range(3):
        q  = calc_q(pi,r,v,i) #行動価値関数の更新
        pi = greedy(q,pi,i) #方策の改善
        
        v_prev = copy.copy(v)
    #%%保存
    res["v"].append(v)
    res["q"].append(v)
    res["pi"].append(v)