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
import numpy as np
import time

#%% センサ値のロギング
class SensorLog(SerialThread):
    """
    引数：辞書
    [ポート番号,ボーレート,サンプリング周期]
    """

    def __init__(self, param):
        self.port       = param["port"]
        self.baudrate   = param["baudrate"]
        self.samplerate = param["samplerate"]
        self.t0         = param["t0"]
        
        self.ser        = SerialCom(self.port, self.baudrate)       
        
        super().__init__(self.ser)

        self.time = []
        self.couple = []
        self.num_np = []
        self.obj_np = []
        self.amb_np = []

    def get_value(self):
        time_np   = np.array(self.time,dtype=np.float32)
        couple_np = np.array(self.couple,dtype=np.float32).T
        num_np    = np.array(self.num,dtype=np.float32).T
        obj_np    = np.array(self.obj,dtype=np.float32).T
        amb_np    = np.array(self.amb,dtype=np.float32).T
        return {"time":time_np,"couple":couple_np,"num":num_np,"obj":obj_np,"amb":amb_np}
    
    #オーバーライド
    def _worker(self, t0):
        self.data = self.ser.serial_read("shift-jis").split(",")
        
        time_now    = time.time() - t0
        couples_now = self.data[1:2]
        nums_now    = []
        objs_now    = []
        ambs_now    = []
        for i in self.data[1:-1]:
            nums_now.append(i.split(":")[0])
            objs_now.append(i.split(":")[1])
            ambs_now.append(i.split(":")[2])    
    
        self.time.append(time_now)
        self.couple.append(couples_now)
        self.num.append(nums_now)
        self.obj.append(objs_now)
        self.amb.append(ambs_now)
        
        time.sleep(self.samplerate)