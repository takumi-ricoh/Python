# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%%
import gym
import numpy as np

gyms = [spec.id for spec in gym.envs.registry.all()]

for i in range(200):
    try:
        mygym = np.random.choice(gyms)#gyms[7]
        #mygym = gyms[807]#'SpaceInvaders-v0'
        env = gym.make(mygym)
        env.reset()
        
        print(mygym)
        env.render()
        break
    except:
        continue
    
#%%
import time
def invadertest():
    env = gym.make('SpaceInvaders-v0')
    for i in range(10):
        env.reset()
        for _ in range(1000):
            env.render()
            _,_,done,_ = env.step(env.action_space.sample())
            if done:
                break
            time.sleep(0.01)
    env.close()
    
#%%

#Acrobot-v1
#Pendulum-v0

#atary-py
#https://qiita.com/tomp/items/7410e2e5f777be5b85f1