# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:47:37 2019

@author: p000495138
"""

import pathlib
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#%%データのロード
dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
dataset_path

#pandas
column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight',
                'Acceleration', 'Model Year', 'Origin']
raw_dataset = pd.read_csv(dataset_path,names=column_names,
                          na_values="?",comment="\t",
                          sep=" ",skipinitialspace=True)
dataset = raw_dataset.copy()
#print(dataset.tail())

#%%データのクレンジング
#print(dataset.isna().sum())

#nan削除
dataset = dataset.dropna()
#originの行はラベルなので分ける
origin = dataset.pop("Origin")

#ワンホットエンコーディング(originの数値 → フラグ化)
dataset["USA"] = (origin==1)*1.0
dataset["Europe"] = (origin==2)*1.0
dataset["Japan"] = (origin==3)*1.0
#print(dataset.tail())

#%%データの調査

#データをランダムに分ける
train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset  = dataset.drop(train_dataset.index)

#グラフ化
#sns.pairplot(train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")

#全体統計
train_stats = train_dataset.describe()
train_stats.pop("MPG")
train_stats = train_stats.transpose()

#特徴量とラベルの分離
train_labels = train_dataset.pop("MPG")
test_labels = test_dataset.pop("MPG")

#正規化
def norm(x):
    return (x-train_stats["mean"])/train_stats["std"]
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

#%%モデル
def build_model():
    model = keras.Sequential([
            layers.Dense(64, activation=tf.nn.relu, input_shape = [len(train_dataset.keys())]),
            layers.Dense(64, activation=tf.nn.relu),
            layers.Dense(1)
    ])
    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mean_squared_error",
                  optimizer=optimizer,
                  metrics=["mean_absolute_error","mean_squared_error"])
    return model

model = build_model()