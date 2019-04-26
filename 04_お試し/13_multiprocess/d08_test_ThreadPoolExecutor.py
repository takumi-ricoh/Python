# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:42:11 2018

@author: p000495138
"""
#https://heavywatal.github.io/python/concurrent.html

#同時に複数立ち上げるのに使う

import time
import random

def target_func(x):
    time.sleep(random.uniform(0, 1))
    return x + 1



import os
import concurrent.futures as confu

# 呼び出し順に拾う
with confu.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = [executor.submit(target_func, x) for x in range(200)]
    (done, notdone) = confu.wait(futures)
    for future in futures:
        print(future.result())
    
print("--------------------------------------")

# 終わったやつから拾う
with confu.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = [executor.submit(target_func, x) for x in range(200)]
    for future in confu.as_completed(futures):
        print(future.result())