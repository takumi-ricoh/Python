# -*- coding: utf-8 -*-
"""
cartpoleに対して、kerasによるニューラルネットワークを適用する
http://neuro-educator.com/rl2/
"""


import numpy as np
import pandas as pd
import gym

#%% 対象(エージェントからは状態遷移確率tmは見えない)
class Worker:
    """
    reward:うまく立っていると1、倒れ始めると0
    observation：カート、ポールの4特性 →　離散化してQテーブル化
    done：うまく立っているとFalse、倒れるとTrue
    """

    #初期化
    def __init__(self):
        #環境の起動
        self.env = gym.make("CartPole-v0")
        # self.env = gym.make("CartPole-v1")
        #状態のインスタンス
        self.state = State()    
        #アクションのインスタンス
        self.action = Action(self.env)    
        #Qテーブルのインスタンス
        self.qtable = Qtable(self.state.num_states, self.action.num_actions)
        
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
                if episode < 100:
                    if episode % 10 == 0:
                        self.env.render()
                else:
                    if episode % r == 0:
                        self.env.render()
                
                #アクション
                observation,reward,done,info = self.env.step(action)

                #重要! NGになったが続いていたら、報酬を差し引く
                if done and step < m-1:
                    reward -= m
                episode_reward += reward

                #アクション実施後の状態を観測し、Qテーブルを更新する
                next_state = self.state.get_state(observation)
                self.qtable.update(state,next_state,action,reward)
                
                #次回のアクション選択
                epsilon =  0.5 * (1 / (episode + 1))
                action = self.action.get_action(self.qtable.qtable, next_state, epsilon)

                #次回の状態を更新
                state = next_state
                
                #stepの終了判定
                if done:
                    break
                
            #状態表示
            if episode % 100 == 0:
                print("episode:",episode,"step:",step,"episode_reward:",episode_reward)

    #学習0:失敗
    def run0(self,n,m):
        self.env.reset()
        self.res = []
        #初期値
        action = 0

        for i in range(n):

            #レンダラーを初期化
            self.env.reset()
        
            #1エピソードあたり            
            sum_reward=0
            for j in range(m):
                self.env.render()
                #観測
                observation, reward, done, info = self.env.step(action)
                #状態に変換
                state_old   = self.state.get_state(observation)
                #テーブル取得
                qtable  = self.qtable.qtable
                #アクション選択
                action_new  = self.action.get_action(qtable, state_old, 0.2)
                #アクション実行
                self.env.step(action_new)
                #観測
                observation, reward, done, info = self.env.step(action)
                #状態に変換
                state_new   = self.state.get_state(observation)
                #テーブルを更新
                self.qtable.update(state_old, state_new, action, reward )
                #sum_rewardを更新
                sum_reward += reward
                #100回やったところで、sum_reward でエピソードを続けるか判断
                if done == True:
                    break
                else:
                    pass
                print(i,j,self.qtable.qtable.mean())
    
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
        self.cart_pos_ary, self.len0 = self.set_state_ary(-2.4, 2.4, 3)# (-2.4, 2.4, 3)
        self.cart_vel_ary, self.len1 = self.set_state_ary(-3.0, 3.0, 5)# (-3.0, 3.0, 5)
        self.pole_ang_ary, self.len2 = self.set_state_ary(-0.5, 0.5, 5)# (-0.5, 0.5, 5) 
        self.pole_vel_ary, self.len3 = self.set_state_ary(-2.0, 2.0, 5)# (-2.0, 2.0, 5)
          
        self.num_states = self.len0*self.len1*self.len2*self.len3
        
    #各観測の値
    def set_state_ary(self,dmin,dmax,num):
        tmp = np.linspace(dmin,dmax,num)
        tmp = tmp[1:-1] #上下限をカット
        length = len(tmp) + 1
        return tmp, length
    
        
    #各観測値をデジタル変換
    def get_state(self,observation):
        cart_pos, cart_vel, pole_ang, pole_vel = observation
        
        #デジタル化
        cart_pos_dig = np.digitize(cart_pos, self.cart_pos_ary)
        cart_vel_dig = np.digitize(cart_vel, self.cart_vel_ary)
        pole_ang_dig = np.digitize(pole_ang, self.pole_ang_ary)
        pole_vel_dig = np.digitize(pole_vel, self.pole_vel_ary)
        
        #全部合わせた状態
        state = cart_pos_dig \
                + cart_vel_dig * self.len0 \
                + pole_ang_dig * self.len0 * self.len1 \
                + pole_vel_dig * self.len0 * self.len1 * self.len2
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
    ALPHA = 0.2
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


