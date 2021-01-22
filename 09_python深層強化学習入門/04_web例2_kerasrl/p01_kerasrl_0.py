# -*- coding: utf-8 -*-
"""
tensorflow 2.1.0

&

keras-rl2 → pip install
keras-rl2 example
https://github.com/wau/keras-rl2/tree/master/examples

"""
import numpy as np
import gym
import matplotlib.pyplot as plt

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

# 環境（タスク）の設定
ENV_NAME = 'Pendulum-v0'
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
assert len(env.action_space.shape) == 1
nb_actions = env.action_space.shape[0]

# actorの設定
actor = Sequential()
actor.add(Flatten(input_shape=(1,) + env.observation_space.shape))
actor.add(Dense(16))
actor.add(Activation('relu'))
actor.add(Dense(16))
actor.add(Activation('relu'))
actor.add(Dense(16))
actor.add(Activation('relu'))
actor.add(Dense(nb_actions))
# 出力は連続値なので、linerを使う
actor.add(Activation('linear'))
print(actor.summary())

# criticの設定。上記で設定したactorのinputを入力に含める
action_input = Input(shape=(nb_actions,), name='action_input')
observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
flattened_observation = Flatten()(observation_input)
x = Concatenate()([action_input, flattened_observation])
x = Dense(32)(x)
x = Activation('relu')(x)
x = Dense(32)(x)
x = Activation('relu')(x)
x = Dense(32)(x)
x = Activation('relu')(x)
x = Dense(1)(x)
x = Activation('linear')(x)
critic = Model(inputs=[action_input, observation_input], outputs=x)
print(critic.summary())

# Experience Bufferの設定
memory = SequentialMemory(limit=100000, window_length=1)
# 行動選択時に加えるノイズ(探索のため)
# 平均回帰課程を用いている。単純にノイズが、muに収束していく。
# ここでは、mu=0に設定しているので、ノイズはゼロになっていく。つまり、探索を行わなくなる。
random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.3)

# DDPGエージェントの設定
agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                  memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                  random_process=random_process, gamma=.99, target_model_update=1e-3)
agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])

# エージェントの学習
# visualizeで学習中のゲーム画面を表示するか。verboseで学習プロセスの表示をするかを設定できる
history = agent.fit(env, nb_steps=50000, visualize=False, verbose=1, nb_max_episode_steps=200)

# 学習曲線のプロット
history = history.history
plt.plot(np.arange(len(history["episode_reward"])), history["episode_reward"])

# 学習済みモデルのパラメータの読み込み
# agent.load_weights('ddpg_{}_weights.h5f'.format(ENV_NAME))

# 学習したモデルのパラメータの保存
agent.save_weights('ddpg_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# 評価
agent.test(env, nb_episodes=5, visualize=False, nb_max_episode_steps=200)