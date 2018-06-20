
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:52:27 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""
from base_mdl import SerialThread, SerialCom
import time
import functions as f
import pandas as pd

#%% データの中身を判定してリスト保存
class MachineLog(SerialThread):

    def __init__(self, param):
        self.port       = param["port"]
        self.baudrate   = param["baudrate"]
        self.samplerate = param["samplerate"]
        self.t0         = param["t0"]
        
        self.ser        = SerialCom(self.port, self.baudrate)     
        
        super().__init__(self.ser)
        
        self.f22 = {"Sen1":[],"Sen3":[],}
        self.f26 = {"Heater1":[],"Heater2":[],}

    def get_value(self):
        #f22
        f22_pd = self.f22.copy()
        f22_pd["Sen1"] = pd.DataFrame(self.f22["Sen1"],columns=["time","Tar","Cur","Sen"])
        f22_pd["Sen2"] = pd.DataFrame(self.f22["Sen2"],columns=["time","Tar","Cur","Sen"])
        #f26
        f26_pd = self.f26.copy()
        f26_pd["Heater1"] = pd.DataFrame(self.f26["Heater1"],columns=["time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        f26_pd["Heater2"] = pd.DataFrame(self.f26["Heater2"],columns=["time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        
        return {"f22":f22_pd,"f26":f26_pd}
    
    #オーバーライド
    def _worker(self):
        self.data = self.ser.serial_read("shift-jis").split(",")

        #f22
        if   "f22" in self.data:
            [sec,Tar,Cur,Sen] = f.f22(self.data)
            if Sen == '[Sensor1]':
                self.f22["Sen1"].append([sec,Tar,Cur,Sen])
            elif Sen == '[Sensor3]':
                self.f22["Sen3"].append([sec,Tar,Cur,Sen])
        
        #f26
        elif "f26" in self.data:
            [sec,MVn,FF_Duty,Max_Duty,Duty,Heater] = f.f26(self.data)
            if   Heater == '[Heat1]':
                    self.f26["Heater1"].append([sec,MVn,FF_Duty,Max_Duty,Duty,Heater])
            elif Heater == '[Heat2]':
                    self.f26["Heater2"].append([sec,MVn,FF_Duty,Max_Duty,Duty,Heater])


        time.sleep(self.samplerate)