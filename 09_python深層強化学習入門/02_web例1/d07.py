# -*- coding: utf-8 -*-
"""
d06でやったようなQ学習で、mountain-carをやってみる

参考：https://qiita.com/minoru_t/items/95b19f824f2af9b704c9
"""

import numpy as np
import pandas as pd
import gym
import time

#%% 対象(エージェントからは状態遷移確率tmは見えない)
class Worker:
    """
    """
    #初期化
    def __init__(self):
        #環境の起動
        self.env = gym.make("MountainCar-v0")
        #状態のインスタンス
        self.state = State()    
        #アクションのインスタンス
        self.action = Action(self.env)    
        #Qテーブルのインスタンス
        self.qtable = Qtable(self.state.num_states, self.action.num_actions)
        
    #サンプル動作
    def sample(self):
        # for episode in range(20):
            observation = self.env.reset()     # 環境の初期化
            for i in range(1000):
                self.env.render()              # レンダリング(画面の描画)
                #action = self.env.action_space.sample()    # 行動の決定
                if observation[1]>0:
                    action =  2
                else:
                    action = 0
                observation, reward, done, info = self.env.step(action)  # 行動による次の状態の決定
                print("=" * 10,"action=",action,"observation=",observation,"reward=",reward,"done=",done)
                #time.sleep(0.5)
    
    #テスト
    def test(self,n,m,end): #(10,1000,500)
        observation = self.env.reset()
        state = self.state.get_state(observation)
        action = np.argmax(self.qtable.qtable[state])

        for i in range(n):    
            self.env.reset()
            for j in range(m):
                #アクションする
                observation,reward,done,info = self.env.step(action)
                #状態に変換
                state = self.state.get_state(observation)
                #次のアクションを決める
                action = np.argmax(self.qtable.qtable[state])            
                #描画
                self.env.render()
                #stepの終了判定
                if end>0: #end条件設定していればそれで終了
                    if j>end:
                        break
                else:
                    if done:
                        break
            print("episode:",i,"step:",j)

    #学習
    def train1(self,n,m,r): #(500,200,100)
        for episode in range(n):
            observation = self.env.reset()
            state = self.state.get_state(observation)
            action = np.argmax(self.qtable.qtable[state])
            episode_reward = 0
            
            for step in range(m):
                #r回に1回描画する
                if episode % r == 0:
                    self.env.render()
                
                #アクション
                observation,reward,done,info = self.env.step(action)

                #重要! NGになったが続いていたら、報酬を差し引く
                # if done and step < m-1:
                #     reward -= m
                episode_reward += reward

                #アクション実施後の状態を観測し、Qテーブルを更新する
                next_state = self.state.get_state(observation)
                self.qtable.update(state,next_state,action,reward)
                
                #次回のアクション選択
                epsilon =  0.1 * (1 / (episode + 1)) #0.5
                action = self.action.get_action(self.qtable.qtable, next_state, epsilon)

                #次回の状態を更新
                state = next_state
                
                #stepの終了判定
                if done:
                    break
                
            #状態表示
            if episode % 100 == 0:
                print("episode:",episode,"step:",step,"episode_reward:",episode_reward)

    #終了
    def close(self):
        self.env.close()

#%% 状態量
class State:
    """    
    計測値をバイナリ値に変換する
    
    """  
    #初期化
    def __init__(self):
        self.car_pos_ary, self.len0 = self.set_state_ary(-1.2, 0.6, 35)# (-2.4, 2.4, 3)
        self.car_vel_ary, self.len1 = self.set_state_ary(-0.07, 0.07, 35)# (-3.0, 3.0, 5)
        
        self.num_states = self.len0*self.len1
        
    #各観測の値
    def set_state_ary(self,dmin,dmax,num):
        tmp = np.linspace(dmin,dmax,num)
        tmp = tmp[1:-1] #上下限をカット
        length = len(tmp) + 1
        return tmp, length
    
    #各観測値をデジタル変換
    def get_state(self,observation):
        car_pos, car_vel = observation
        
        #デジタル化
        car_pos_dig = np.digitize(car_pos, self.car_pos_ary)
        car_vel_dig = np.digitize(car_vel, self.car_vel_ary)
        
        #全部合わせた状態
        state = car_pos_dig \
                + car_vel_dig * self.len0
        return state

#%% アクション
class Action:
    def __init__(self,env):
        self.num_actions = env.action_space.n
        
    #ε-greedy
    def get_action(self,qtable, state, epsilon):

        if  epsilon <= np.random.uniform(0, 1):
            action = np.argmax(qtable[state])
        else:
            action = np.random.choice([0,1])
        
        return action

#%% Qテーブル
class Qtable:
    ALPHA = 0.05
    GAMMA = 0.99
    
    #初期化
    def __init__(self,num_states,num_actions):
        self.qtable = np.random.uniform(low=-1,high=1, size=(num_states, num_actions))
        
    #アップデート
    def update(self,S_from, S_to, action, reward):

        #パラメータ
        alpha = Qtable.ALPHA
        gamma = Qtable.GAMMA
               
        #各項の計算
        q1 = max(self.qtable[S_to,:])
        q2 = self.qtable[S_from, action]
        r  = reward
    
        #アップデートする値    
        tmp = alpha*(r + gamma*q1) + (1-alpha)*q2
        
        #アップデート
        self.qtable[S_from, action] = tmp

#%%実行
