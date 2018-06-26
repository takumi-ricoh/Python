# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:52:27 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""
from pkg_read import base_mdl as base_r
from pkg_read import functions as f
import time
import pandas as pd
import threading

#%% データの中身を判定してリスト保存
class MachineLog(base_r.SerialThread):
    
    def __init__(self, param, t0):
        self.port       = param["port"]
        self.baudrate   = param["baudrate"]
        self.samplerate = param["samplerate"]
        self.t0         = t0
        
        self.ser        = base_r.SerialCom(self.port, self.baudrate)     
        
        super().__init__(self.ser)
        
        #初期化(データフレーム)
        f22_init = pd.DataFrame([],columns=["sec","time","Tar","Cur","Sen"])
        f26_init = pd.DataFrame([],columns=["sec","time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        
        self.f22 = {"Sen1":f22_init, "Sen3":f22_init}
        self.f26 = {"Heater1":f26_init, "Heater2":f26_init}

    def start(self):
        #スレッドの作成と開始
        self.thread = threading.Thread(target = self._worker,)
        self.thread.start()
        print("started")

    def get_value(self):        
        return {"f22":self.f22,"f26":self.f26}
    
    #オーバーライド
    def _worker(self):
        self.data = self.ser.serial_read("shift-jis").split(",")

        #時刻
        time_now    = [time.time() - self.t0]

        #f22
        if   "f22" in self.data:
            [sec,Tar,Cur,Sen] = f.f22(self.data)
            f22_tmp = pd.Series(time_now + [sec,Tar,Cur,Sen])
            
            if Sen == '[Sensor1]':
                self.f22["Sen1"].append(f22_tmp,ignore_index=True)
            elif Sen == '[Sensor3]':
                self.f22["Sen3"].append(f22_tmp,ignore_index=True)
        
        #f26
        elif "f26" in self.data:
            [sec,MVn,FF_Duty,Max_Duty,Duty,Heater] = f.f26(self.data)
            f26_tmp = pd.Series(time_now + [sec,MVn,FF_Duty,Max_Duty,Duty,Heater])
            if   Heater == '[Heat1]':
                    self.f26["Heater1"].append(f26_tmp,ignore_index=True)
            elif Heater == '[Heat2]':
                    self.f26["Heater2"].append(f26_tmp,ignore_index=True)


        time.sleep(self.samplerate)