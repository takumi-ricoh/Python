# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:21:33 2018

@author: p000495138
"""

import serial
import time
import threading

class SerialThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

def read_worker(ser):
    for i in range(50):
        read = ser.readline().decode("utf-8").strip()
        print(read)
        time.sleep(.1)
        
    ser.close()

def set_serial(com,rate):
    ser = serial.Serial(
        port=com,
        baudrate=rate,
        bytesize=serial.EIGHTBITS,
        stopbits=serial.STOPBITS_ONE,
        rtscts=True)
    return ser

#シリアル通信
ser1 = set_serial("COM13",9600)
ser2 = set_serial("COM5",9600)

#スレッドを作成
th1 = threading.Thread(name = "COM13", target=read_worker,args=(ser1,))
th2 = threading.Thread(name = "COM5" , target=read_worker,args=(ser2,))

#スレッドスタート
th1.start()
th2.start()

#終了