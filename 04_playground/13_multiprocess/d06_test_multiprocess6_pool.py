# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:33:19 2018

@author: p000495138
"""

#http://www.yoheim.net/blog.php?q=20170601

from multiprocessing import Pool, TimeoutError
import time 
import os

def f7(x):
    return x*x

if __name__ == "__main__":
    # 4つのプロセスを開始します.
    with Pool(processes=4) as pool:

        # 0〜9の10個の値を、4つのプロセスで処理します.
        print(pool.map(f7, range(10)))
        # print: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

        # ひとつ上と似ていますが、プロセスの実行順が不定になります.
        for i in pool.imap_unordered(f7, range(10)):
            print(i)
            # print: 0, 1, 4, 16, 9, 25, 36, 49, 64, 81

        # "f7(20)"という処理を非同期に実行します（利用するプロセスは1つのみ）
        res = pool.apply_async(f7, (20,))
        # 処理結果が返ってくるまで、最大1秒間待機します
        print(res.get(timeout=1))
        # print: 400

        # 上記の仕組みを連続して呼ぶと、複数のプロセスで処理を行うことができます.
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(10)]
        results = [res.get(timeout=1) for res in multiple_results]
        # 10個出力されます
        print(results)
        # print : [37604, 37607, 37606, 37605, 37604, 37607, 37606, 37605, 37604, 37607]

        # ただしユニークにすると4つのみ（=プールしたプロセス数）であることがわかります
        print(set(results), len(set(results)))
        # {37604, 37605, 37606, 37607} 4

        # タイムアウトが発生する場合のサンプルです
        res = pool.apply_async(time.sleep, (10,))
        try:
            res.get(timeout=1)
        except TimeoutError as e:
            print("Timeout.....!!!", e)
