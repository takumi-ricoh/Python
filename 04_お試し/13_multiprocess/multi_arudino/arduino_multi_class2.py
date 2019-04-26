# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:21:33 2018

@author: p000495138
"""

#別プロセスで
#https://stackoverflow.com/questions/36181316/python-matplotlib-plotting-in-another-process

#別プロセスでのプロットはうまくいかないのでやらない

import serial
import time
import threading
import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import random

#%% スレッドクラス
class SerialThread():

    def __init__(self, param):
        
        #停止用の初期化
        self.stop_event = threading.Event() #停止させるかのフラグ
        #シリアル通信開始
        self.ser = self._serInit(param["com"],param["rate"])
        #保存用データの初期化
        self.return_value = []

        #スレッドの作成と開始
        self.thread = threading.Thread(target = self._serial_worker)
        self.thread.start()

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ
        self.ser.close()      #終わったら通信をきる

    def get_value(self):
        return self.return_value

    def _serial_worker(self):
        #stop_event がセットされるまでは、、」
        while not self.stop_event.is_set():
            line = self.ser.readline().decode("utf-8").strip()
            #データ保存
            self.return_value.append(line)
            time.sleep(.1)
    
    def _serInit(self,com,rate):
        #異常がある場合に自動で、シリアル通史を閉じる
        ser = serial.Serial(
            port=com,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True)
        return ser

#%% プロセスクラス
class SerialProcess():
    def __init__(self,param):
        #停止用の初期化
        self.stop_event = mp.Event() #停止させるかのフラグ        
        #シリアル通信開始
        self.ser = self._serInit(param["com"],param["rate"])
        #保存用データの初期化
        self.return_value = []

        #プロセスの作成と開始
        self.queue = mp.Queue()
        self.process = mp.Process(target = self._serial_worker, args=(self.queue,self.ser,self.return_value))
        self.process.start()
        
    def stop(self):
        self.stop_event.set()
        self.process.join()    #プロセスが停止するのを待つ

    def get_value(self):
        return self.queue.get()

    def _serial_worker(self,q,ser,value):        
        #stop_event がセットされるまでは、、」
        while not self.stop_event.is_set():
            line = ser.readline().decode("utf-8").strip()
            obj = q.put(value.append(line))
            print(obj)
            time.sleep(.1)
    
    def _serInit(self,com,rate):
        #異常がある場合に自動で、シリアル通史を閉じる
        ser = serial.Serial(
            port=com,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True)
        return ser

#%%メイン処理
if __name__ == '__main__':
    #シリアル通信スレッド開始
    param1 = {"com":"COM13", "rate":9600}
    param2 = {"com":"COM5",  "rate":9600}

    alist=[]

    th = SerialThread(param1)
#    process = SerialProcess(param2)
    
    #%%実行    
    start = time.time()

    while True:

        a=th.get_value()
        #b=process.get_value()
        if len(a)>0:
            print(a[-1])
    
        if time.time()-start > 5:
            th.stop()
            #process.stop()
            print("finish")
            break
        
        time.sleep(.1)
