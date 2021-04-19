# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:34:03 2017

@author: p000495138
"""
import serial
import matplotlib.pyplot as plt

class ReadSerial():
    def __init__(self):
        pass
    def main(self,ser):
        self.err =0 
        a=ser.readline().rstrip()
        #print(a)
        if a == b'':
            self.temp=0
            #print("kita")
        else:
            c = float(a)
            self.temp=c
            #print("kitakita")
        return self.temp

def main():
    #グラフ
    fig,ax=plt.subplots()
    line, = ax.plot(0)
    
    #データ
    a=ReadSerial()
    err=0
    nums=[]
    ser=serial.Serial('COM5',9600,timeout=0.1)
    while err==0:
        try:
            num,err = a.main(ser)
            nums.append(num)
            #print(nums)    
            #グラフ更新
            ax.clear()
            ax.plot(nums)
            plt.pause(0.001)
        except KeyboardInterrupt:
            err=1
            ser.close()

if __name__=="__main__":
    main()

