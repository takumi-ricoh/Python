# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:28:51 2018

@author: p000495138
"""

#http://www.yoheim.net/blog.php?q=20170601

from multiprocessing import Value, Array
import time

def f5(n, a):
    n.value = 3.1415926
    for i in range(len(a)):
        a[i] *= -1

if __name__ == "__main__":
    # 共有メモリ（Value）を作成します.
    num = Value('d', 0.0)
    # 共有メモリ（Array）を作成します.
    arr = Array('i', range(10))
    # サブプロセスを作り、実行します.
    p = Process(target=f5, args=(num, arr))
    p.start()
    p.join()
    # 共有メモリ（Value）から値を取り出します
    print(num.value)
    # 共有メモリ（Array）から値を取り出します
    print(arr[:])
    
    time.sleep(3)