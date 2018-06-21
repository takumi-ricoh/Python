# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:10:30 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""

from base_mdl import SerialThread, SerialCom
import pandas as pd
import numpy as np

import time

#%% センサ値のロギング
class SensorLog(SerialThread):

    def __init__(self, param, senNum, t0):
        #センサパラメータセット
        self.port       = param["port"]
        self.baudrate   = param["baudrate"]
        self.samplerate = param["samplerate"]
        self.senNum     = param["senNum"]         #センサ数
        self.t0         = t0

        self.ser        = SerialCom(self.port, self.baudrate) 
        
        super().__init__(self.ser)

        #データ格納用の空データフレームを準備
        self.couple = pd.DataFrame([],columns=["sec","couple1","couple2"])
        self.num    = pd.DataFrame([],columns=["sec"]+["num"+str(i) for i in range(self.senNum)])
        self.obj    = pd.DataFrame([],columns=["sec"]+["obj"+str(i) for i in range(self.senNum)])
        self.amb    = pd.DataFrame([],columns=["sec"]+["amb"+str(i) for i in range(self.senNum)])

    def get_value(self):
        return {"couple":self.couple,"num":self.num,"obj":self.obj,"amb":self.amb}
        
    #オーバーライド
    def _worker(self, t0):
        self.data = self.ser.serial_read("shift-jis").split(",")
        
        #ある時刻でのデータ列取得(リスト)
        time_now    = [time.time() - self.t0]
        couples_now = time_now + self.data[1:2]
        nums_now    = time_now + [i.split(":")[0] for i in self.data[3:]]
        objs_now    = time_now + [i.split(":")[1] for i in self.data[3:]]
        ambs_now    = time_now + [i.split(":")[2] for i in self.data[3:]]

        #データフレームに追加
        self.couple.append(pd.Series(couples_now),ignore_index=True)
        self.num.append(pd.Series(nums_now),ignore_index=True)
        self.obj.append(pd.Series(objs_now),ignore_index=True)
        self.amb.append(pd.Series(ambs_now),ignore_index=True)
        
        #センサ数取得
        self.sensor_number = len(objs_now)
        
        #ワーカー
        time.sleep(self.samplerate)