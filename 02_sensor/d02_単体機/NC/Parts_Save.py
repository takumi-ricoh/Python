# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:21:10 2016

@author: p000495138
"""

import numpy as np
import pandas as pd

###---------データの保存---------####
def save_csv(data,save_legend,name): #データ/ 
    print(save_legend)
    write_data = data.T
    writedata_pd = pd.DataFrame(write_data) #データフレーム化
    writedata_pd.columns = save_legend
    writedata_pd.to_csv(name) #ｃｓｖ保存
