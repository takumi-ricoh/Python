# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:43:02 2019

@author: p000495138
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np

print(tf.__version__)

#%%データのロード
imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
