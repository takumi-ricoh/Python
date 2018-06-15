# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:21:33 2018

@author: p000495138
"""

import serial
import time
import threading

#%% シリアルクラス
class SerialThread(threading.Thread):

    def __init__(self, param):
        #停止用の初期化
        self.stop_event = threading.Event() #停止させるかのフラグ
        #シリアル通信開始
        self.ser = self._serInit(param["com"],param["rate"])
        #保存用データの初期化
        self.return_value = []

        #スレッドの作成と開始
        self.thread = threading.Thread(target = self._target)
        self.thread.start()


    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ
        self.ser.close()      #終わったら通信をきる

    def get_value(self):
        return self.return_value

    def _target(self):
        #stop_event がセットされるまでは、、」
        while not self.stop_event.is_set():
            line = self.ser.readline().decode("utf-8").strip()
            #データ保存
            self.return_value.append(line)
            time.sleep(.1)
    
    def _serInit(self,com,rate):
        ser = serial.Serial(
            port=com,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True)
        return ser


#%%シリアル通信パラメータ
param1 = {"com":"COM13", "rate":9600}
param2 = {"com":"COM5",  "rate":9600}

#%%スレッド実行
#スレッド1
th1 = SerialThread(param1)
th2 = SerialThread(param2)


start = time.time()

while True:
    a=th1.get_value()
    b=th2.get_value()
    if len(a)>0:    
        print("th1:"+a[-1])
        print("th2:"+b[-1])

    if time.time()-start > 5:
        th1.stop()
        th2.stop()
        print("finish")
        break

