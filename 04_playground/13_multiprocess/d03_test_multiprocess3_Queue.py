# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:21:58 2018

@author: p000495138
"""

#http://www.yoheim.net/blog.php?q=20170601

from multiprocessing import Process
from multiprocessing import Queue
import time

def f2(q):
    time.sleep(3)
    # 3秒後に、キューに値を渡します.
    q.put([42, None, "Hello"])
    time.sleep(2)

if __name__ == "__main__":
    # スレッド間でやり取りするためのキューを作成します.
    q = Queue()
    # キューを引数に渡して、サブプロセスを作成します.
    p = Process(target=f2, args=(q,))
    # サブプロセスを開始します.
    p.start()
    # q.get()できるまで待ちます.
    print(q.get())
    # サブプロセス完了を待ちます.
    p.join()
