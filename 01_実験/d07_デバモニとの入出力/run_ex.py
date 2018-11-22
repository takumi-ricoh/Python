# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 17:55:53 2018

@author: p000495138
"""

import set_param as sp
from serial import Serial
import ctypes
import time
from threading import Thread,Event

#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B        

#%%シリアル通信クラス
class Ser():

    def __init__(self,port,baudrate):
        self.com = Serial(port=port,baudrate=baudrate,timeout=0.01)
#        self.com.set_buffer_size(rx_size = 12800, tx_size = 12800)

    def write(self,word):
        word2 = word + "\r\n"
        self.com.write(word2.encode())

    def read(self):
        data = self.com.readline()
        data = data.strip().decode("utf-8") #先頭/末を消す
        return data
    
    def close(self):
        self.com.close()
        
#%%CLRログモニタ
class CLRMonitor():

    def __init__(self):
        self.clr = []
        self.size = 1

    def set_mode(self,word):
        if "a = " in word:
            self.clr.append(word)

    def get_last_jdg(self):
        #サイズが変化してたらTrueを返す
        if len(self.clr) > self.size:
            self.size = len(self.clr)
            return True
        else:
            return None

#%%定着モードモニタ
class ModeMonitor():

    def __init__(self):
        self.mode = ["dammy"]
        self.size = 1

    def set_mode(self,word):
        if "FusModeChg" in word:
            self.mode.append(word)

    def get_last_jdg(self):
        #サイズが変化してたら値を返す
        if len(self.mode) > self.size:
            self.size = len(self.mode)
            print("kita")
            #当接側への変更
            if "3-8" in self.mode[-1]:
                print("to_print")
                return "to_print"
            if "3-8" in self.mode[-2]:
                if "2-5" in self.mode[-1]:
                    return "to_standby"
            else:
                return None
        else:
            return None

#%%離間モニタ
class JdgMonitor():

    def __init__(self):
        self.clr = ["dammy"]
        self.size = 1
        
    def set_mode(self,word):
        if "FusSepSnrChg[1]" in word:
            self.clr.append("jdg1_contact")    
        if "FusSepSnrChg[0]" in word:
            self.clr.append("jdg2_apart")  

    def get_last_jdg(self):
        #サイズが変化してたら値を返す
        if len(self.clr) > self.size:
            self.size = len(self.clr)
            return self.clr[-1]
        else:
            return None
                
#%%GPIO向けカウンタ
class GpioCounter():

    def __init__(self):
        self.num = 0
        self.count = 0 
        self.flg   = 0
    
    def get_flg(self):
        return self.flg
    
    def start(self,num):
        self.num = num #落とす回数
        self.count = 0
        self.flg = 1

    def call(self):
        #コールされたらカウントアップ
        if self.flg == 1:
            self.count += 1    

        #所定回数行ったらリセット
        if self.count > self.num:
            self.flg = 0
            self.count = 0

    def end(self):
        self.count=0
        self.flg  =0


#%%実行部
class Worker():

    def __init__(self,engine,gpio):
        #計測初期化
        self.clr_monitor  = CLRMonitor()      #CLRログモニタ
        self.mode_monitor = ModeMonitor()      #定着状態モニタ
        self.jdg_monitor  = JdgMonitor()       #判定状態モニタ
        self.gpio_count0  = GpioCounter()     #CLRコマンド
        self.gpio_count1  = GpioCounter()     #判定1 & 判定2
        self.gpio_count2  = GpioCounter()     #定着状態
        self.gpio_count3  = GpioCounter()     #CLR当接離間状態
        self.event1    = Event()
        self.event2    = Event()
        self.event3    = Event()
        self.enginelog_updated = False
        print("initialized done")

    #%%エンジンログの読み込み
    def engine_reader(self):
        print("スレッド1開始")
        #log全般
        self.loglist = []
        #CLRログのみ
        self.CLRloglist=[]
        while not self.event1.is_set():
            #エンジンログを読む
            engine_word = engine.read()
    
            if len(engine_word)>0:
                self.log_size = len(engine_word)
                self.loglist.append(engine_word)
                #モニタ変数にセット
                #self.clr_monitor.set_mode(engine_word)
                self.mode_monitor.set_mode(engine_word)
                self.jdg_monitor.set_mode(engine_word)
                
#                if "MainMT" in engine_word:
#                    print(engine_word)
                
            time.sleep(0.01)

        print("スレッド1終了")

    #%%GPIOカウンタ
    def gpio_counter(self):
        print("スレッド2開始")
    
        while not self.event2.is_set():
            #GPIOのアップデート
            #gpioカウンタアップデート
            #self.gpio_count0.call()
            self.gpio_count1.call()
            self.gpio_count2.call()
            self.gpio_count3.call()

            time.sleep(0.05)
        print("スレッド2終了")

    #%%GPIOアップデート
    def gpio_updater(self):
        print("スレッド3開始")
        self.CLRlogsize=0
        while not self.event3.is_set():
            #判定材料
            #last_clr    = self.clr_monitor.get_last_jdg()#CLRログが更新したか?
            last_mode   = self.mode_monitor.get_last_jdg()#定着状態
            last_jdg    = self.jdg_monitor.get_last_jdg()#離間状態
    
            #CLRログ
            #変化してたら
#            if last_clr == True:
#                gpio.write("gpio set 0")
#                self.gpio_count0.start(5) #
#            if self.gpio_count0.get_flg() == 0:
#                gpio.write("gpio clear 0")
#            
#            time.sleep(0.02)
        
#            #判定1　＆ 判定2 
#            if last_jdg == "jdg1_contact": #判定1
#                gpio.write("gpio set 1")
#                self.gpio_count1.start(5)
#            if last_jdg == "jdg2_apart":  #判定2
#                gpio.write("gpio set 1")
#                self.gpio_count1.start(5)        
#            if self.gpio_count1.get_flg() == 0: #タイムアウト
#                gpio.write("gpio clear 1")
#
#            time.sleep(0.02)
#        
#            #定着状態f
#            if last_mode == "to_print": #印刷になったらstart
#                gpio.write("gpio set 2")
#                self.gpio_count2.start(10000)
#            if last_mode == "to_standby": #印刷から抜けたらend
#                gpio.write("gpio clear 2")
#                self.gpio_count2.end()        
#            if self.gpio_count2.get_flg() == 0: #タイムアウト
#                gpio.write("gpio clear 2")
#
#            time.sleep(0.02)
        
            #CLR状態
            if last_mode == "to_print": #判定1通ったらstart
                gpio.write("gpio set 3")
                self.gpio_count3.start(10000)
            if last_jdg == "jdg2_apart":   #終了条件1：判定2
                gpio.write("gpio clear 3")
                self.gpio_count3.end()
#            if last_mode == "to_standby":   #終了条件2：印刷抜け
#                gpio.write("gpio clear 3")
#                self.gpio_count3.end()

            time.sleep(0.05)
                        
        print("スレッド3終了")
            
#%%
def my_reset(gpio,engine):
    gpio.write("gpio clear 0") #CLRコマンドフラグ
    gpio.write("gpio clear 1") #判定1&判定2
    gpio.write("gpio clear 2") #状態変化
    gpio.write("gpio clear 3") #CLR当接離間状態
    engine.write("TMP")
    engine.write("CLR")
    engine.close()
    gpio.close()

#%%通信開始(gpio)
gpio = Ser("COM11",9600)
#初期化
gpio.write("gpio clear 0") #CLRコマンドフラグ
gpio.write("gpio clear 1") #判定1&判定2
gpio.write("gpio clear 2") #状態変化
gpio.write("gpio clear 3") #CLR当接離間状態
print("GPIO8 start")


#%%通信開始(エンジン)
engine = Ser("COM10",57600)
engine.write("TMP")
engine.write("CLR")
print("EngineLog start")

#%%SP設定
commands = sp.get_config()
for command in commands:
    engine.write(command)
    time.sleep(0.02)
print("config done")
time.sleep(5)

#%%ループ
print("スレッド生成")
worker = Worker(engine,gpio)
thread1 = Thread(target=worker.engine_reader)
thread2 = Thread(target=worker.gpio_counter)
thread3 = Thread(target=worker.gpio_updater)
thread1.setDaemon(True)
thread2.setDaemon(True)
thread3.setDaemon(True)

print("スレッド開始")
thread1.start()
thread2.start()
thread3.start()

print("ESC待ち")
while True:
    #割り込み終了
    if getkey(ESC) == True:
        break
print("ESC受けた")

worker.event3.set()
thread3.join()
print("スレッド3終了")

worker.event2.set()
thread2.join()

worker.event1.set()
thread1.join()

print("loop end")

#%%終了処理
my_reset(gpio,engine)
flg = 0
