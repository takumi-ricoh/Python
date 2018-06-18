# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:21:33 2018

@author: p000495138
"""

import serial
import time
import threading
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np

#%% シリアルクラス
class SerialThread():

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
        #異常がある場合に自動で、シリアル通史を閉じる
        ser = serial.Serial(
            port=com,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True)
        return ser

#%% シリアルクラス
class PlotProcess():
    def __init__(self):
        #停止用の初期化
        self.stop_event = multiprocessing.Event() #停止させるかのフラグ        
        #グラフの初期化初期化
        #self._init_plot()
        self.data2 = 0
        #データl更新プロセスの作成と初期化
        self.process = multiprocessing.Process(target = self._target, )
        self.process.start()
        

    def stop(self):
        self.stop_event.set()
        self.process.join()    #スレッドが停止するのを待つ

    def set_value(self, data):
        self.data = data

    def _init_plot(self):
        #初期化
        self.data = {"a":0,"b":0}
        #共通データ
        self.fig, self.ax = plt.subplots(2,1)
        self.line1, = self.ax[0].plot(np.zeros(1),"r.-")
        self.line2, = self.ax[1].plot(np.zeros(1),"g.-")
        self.fig.show()
        self.fig.canvas.draw()
#        self.bg0 = self.fig.canvas.copy_from_bbox(self.ax[0].bbox)
#        self.bg1 = self.fig.canvas.copy_from_bbox(self.ax[1].bbox)

    def _target(self):
        #stop_event がセットされるまでは、、」
        while not self.stop_event.is_set():
            self.data2 = self.data *2
#            print(self.data["a"])
#            #データ更新
#            x=np.arange(0,len(self.plot_data))
#            self.line1.set_data(x,self.data["a"])
#            self.line2.set_data(x,self.data["b"])
#            #おまじない           
#            self.fig.canvas.restore_region(self.bg0)
#            self.fig.canvas.restore_region(self.bg1)
#            self.fig.canvas.draw()
#            self.ax[0].draw_artist(self.line1)
#            self.ax[1].draw_artist(self.line2)
#            self.fig.canvas.update()
#            self.fig.canvas.flush_events()    
#            self.fig.tight_layout()      
            time.sleep(.1)

#%%メイン処理
if __name__ == "__main__":

    #シリアル通信スレッド開始
    param1 = {"com":"COM13", "rate":9600}
    param2 = {"com":"COM5",  "rate":9600}

    th1 = SerialThread(param1)
    th2 = SerialThread(param2)
    
    #プロットプロセス実行
    pro1 = PlotProcess()
    
    #%%実行    
    start = time.time()

    while True:
        a=th1.get_value()
        b=th2.get_value()
        
        #data = {"a":a, "b":b}
        data=1
        
        if len(a)>0: 
            pro1.set_value(data)
            print(pro1.get_value())
    
        if time.time()-start > 5:
            th1.stop()
            th2.stop()
            pro1.stop()
            print("finish")
            break

