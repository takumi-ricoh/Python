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
import itertools

#%% データの中身を判定してリスト保存
class MachineLog(base_r.SerialThread):
    
    def __init__(self, cfg, t0):
        self.port       = cfg.PORT
        self.baudrate   = cfg.BAUDRATE
        self.samplerate = cfg.SAMPLERATE
        self.t0         = t0
        
        self.ser        = base_r.SerialCom(self.port, self.baudrate)     
        
        super().__init__(self.ser)
        
        #初期化(データフレーム)
        f22_init = pd.DataFrame([],columns=["sec","time","Tar","Cur","Sen"])
        f26_init = pd.DataFrame([],columns=["sec","time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        
        self.f22 = {"Sen1":f22_init, "Sen3":f22_init}
        self.f26 = {"Heater1":f26_init, "Heater2":f26_init}


    def get_value(self):        
        return {"f22":self.f22,"f26":self.f26}
    
    #オーバーライド
    def _worker(self):
        self.data = self.ser.serial_read("shift-jis").split(",")

        #インデックス用のカウンタ
        it = itertools.count()
        
        while not self.stop_event.is_set():
            
            #時刻
            time_now    = [time.time() - self.t0]
            #カウンタ
            self.count       = next(it)
                        
            #f22
            if   "f22" in self.data:
                [sec,Tar,Cur,Sen] = f.f22(self.data)
                f22_tmp = time_now + [sec,Tar,Cur,Sen]
                
                if Sen == '[Sensor1]':
                    self.f22["Sen1"].loc[self.count] = f22_tmp
                elif Sen == '[Sensor3]':
                    self.f22["Sen3"].loc[self.count] = f22_tmp
            
            #f26
            elif "f26" in self.data:
                [sec,MVn,FF_Duty,Max_Duty,Duty,Heater] = f.f26(self.data)
                f26_tmp = time_now + [sec,MVn,FF_Duty,Max_Duty,Duty,Heater]
    
                if   Heater == '[Heat1]':
                        self.f26["Heater1"].loc[self.count] = f26_tmp
                elif Heater == '[Heat2]':
                        self.f26["Heater2"].loc[self.count] = f26_tmp

    
            time.sleep(.3)