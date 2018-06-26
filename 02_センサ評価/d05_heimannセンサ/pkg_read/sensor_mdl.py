# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:10:30 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""

from pkg_read import base_mdl as base_r
import pandas as pd
import numpy as np
import threading
import time

#%% センサ値のロギング
class SensorLog(base_r.SerialThread):

    def __init__(self, param, t0):
        #センサパラメータセット
        self.param      = param
        self.port       = param["port"]
        self.baudrate   = param["baudrate"]
        self.samplerate = param["samplerate"]
        self.senNum     = param["senNum"]         #センサ数
        self.senPos     = param["senPos"]
        self.t0         = 1

        self.ser        = base_r.SerialCom(self.port, self.baudrate) 
        
        super().__init__(self.ser)

        #データ格納用の空データフレームを準備
        self.couple = pd.DataFrame([],columns=["sec","couple1","couple2"])
        self.num    = pd.DataFrame([],columns=["sec"]+["num"+str(i) for i in range(self.senNum)])
        self.obj    = pd.DataFrame([],columns=["sec"]+["obj"+str(i) for i in range(self.senNum)])
        self.amb    = pd.DataFrame([],columns=["sec"]+["amb"+str(i) for i in range(self.senNum)])

    def start(self):
        #スレッドの作成と開始
        self.thread = threading.Thread(target = self._worker,)
        self.thread.start()
        #print("started")

    def get_value(self):
        return {"sensor":{"couple":self.couple,"num":self.num,"obj":self.obj,"amb":self.amb}}
        
    #オーバーライド
    def _worker(self):
        #self.data = self.ser.serial_read("shift-jis").split(",")
        self.data = ["5","50","60","1:2:3","4:5:6","7:8:9","10:11:12","13:14:15","16:17:18","19:20:21","22:23:24"]
        
        print("sensorworker start")
        
        #ある時刻でのデータ列取得(リスト)
        time_now    = [time.time() - self.t0]
        couples_now = time_now + self.data[1:3]
        nums_now    = time_now + [i.split(":")[0] for i in self.data[3:]]
        objs_now    = time_now + [i.split(":")[1] for i in self.data[3:]]
        ambs_now    = time_now + [i.split(":")[2] for i in self.data[3:]]

        #データフレームに追加
        self.couple = self.couple.append(pd.Series(couples_now),ignore_index=True)
        self.num    = self.num.append(pd.Series(nums_now),ignore_index=True)
        self.obj    = self.obj.append(pd.Series(objs_now),ignore_index=True)
        self.amb    = self.amb.append(pd.Series(ambs_now),ignore_index=True)
        
        #センサ数取得
        self.sensor_number = len(objs_now)
        
        #ワーカー
        time.sleep(.1)