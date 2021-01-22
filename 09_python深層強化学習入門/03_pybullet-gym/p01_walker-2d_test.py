# -*- coding: utf-8 -*-
"""
1.visual studio インストール
 https://qiita.com/F_murasaki/items/9359cab8dd56a30c885e

2.pip install pybullet

3.ここからダウンロード、cdでフォルダ移動し、pip install -e .
  https://github.com/benelot/pybullet-gym



"""
import gym
import pybullet_envs


pybullet_envs.getList()

# 環境の生成
#env = gym.make('AntBulletEnv-v0')
env = gym.make('PusherBulletEnv-v0')

# env.render(mode="human")
# env.reset()
# while True:
#     env.step(env.action_space.sample())

while True:
#for _ in range(1):
    env.render(mode="human")
    state = env.reset()
    c=0
    while True:
        action = env.action_space.sample()
        state_new, r, done, info = env.step(action)
        #print("reward:",r)
        # if done:
        #     print('episode done')
        #     break
    
        c+=1
        if c>5000:
            break