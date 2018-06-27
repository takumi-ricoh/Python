# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:48:23 2018

@author: p000495138
"""
import threading
from serial import Serial

#%% スレッドクラス
class SerialThread():

    def __init__(self, ser):
        
        #停止用の初期化
        self.stop_event = threading.Event() #停止させるかのフラグ
        #停止時はシリアルポートを閉じる
        self.ser = ser
        #保存用データの初期化
        self.return_value = []

    def start(self):
        #スレッドの作成と開始
        self.thread = threading.Thread(target = self._worker,)
        self.thread.start()
        print("thread started")

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ
        self.ser.com.close()      #終わったら通信をきる

#    def _worker(self):
#        None

#%%シリアルポートクラス
class SerialCom():
    
    def __init__(self,port,baudrate):
        self.port       = port
        self.baudrate   = baudrate
        self._serial_init(self.port,self.baudrate)
    
    def _serial_init(self,port,baudrate):
        self.com = Serial(
        port=port,
        baudrate=baudrate,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1,
        xonxoff=0,
        rtscts=0,
        writeTimeout=None,
        dsrdtr=None)         

    def serial_read(self, coding):
        data = self.com.readline()
        data = data.strip().decode(coding) #先頭/末を消す
        return data