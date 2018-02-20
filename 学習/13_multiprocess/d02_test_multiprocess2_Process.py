# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:50:12 2018

@author: p000495138
"""

#http://www.yoheim.net/blog.php?q=20170601

from multiprocessing import Process
import time

# 呼び出したい関数
def f1(name):
    print("Hello", name)
    print("Sleeping... 3s")
    time.sleep(3)
    print("Good morning", name)

if __name__ == "__main__":
    # サブプロセスを作成します
    p = Process(target=f1, args=("Bob",))
    # 開始します
    p.start()
    print("Process started.")
    # サブプロセス終了まで待ちます
    p.join()
    print("Process joined.")
