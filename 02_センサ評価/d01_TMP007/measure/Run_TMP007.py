# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 12:30:55 2017

@author: root
"""

import time
import TMP007.TMP007 as TMP007
import numpy as np
import RPi.GPIO as GPIO
import TMP007.Plot_TMP007 as plot
import matplotlib.pyplot as plt
import multiprocessing as mp

sensor = TMP007.TMP007()

#set GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

print('Press Ctrl + Z to cancel...')
objTempCold = 0
#%%
"""GPIO initialize"""
#init
GPIO.output(21,GPIO.LOW)
GPIO.output(26,GPIO.LOW)
res=[]

"""start"""
time.sleep(1)
start   = time.time()
oldtime = start

#queue = mp.Queue() #multi
#thisplot = plot.PlotTemp()
#p=mp.Process(target=thisplot.plotupdate,args=(i,objTempC,dieTempC,))
#p.start()

"""sampling"""
for i in range(20000000): #2000point @ calibration
    #sampling triger ON
    time.sleep(0.2)
    GPIO.output(21,GPIO.HIGH)
    #time
    newtime   = time.time()
    dt        = newtime-oldtime
    totaltime = newtime -start   
    oldtime   = newtime
    #shutter ON/OFF
    if i in [10, 50, 90, 130, 170, 210, 250]:
        GPIO.output(26,GPIO.HIGH)
    elif i in [30, 70, 110, 150, 190, 230, 270]:
        GPIO.output(26,GPIO.LOW)
    #get data
    dieTempC = sensor.readDieTempC()
    objTempC = sensor.readObjTempC()
    sensorVolts = sensor.readVoltage()    
    #list    
    temp = [totaltime,dieTempC,objTempC,sensorVolts]
    res.append(temp)
    #sampling triger OFF
    time.sleep(0.2)
    GPIO.output(21,GPIO.LOW)

    print("time="+str(round(totaltime,3)),"  dieTempC="+ str(round(dieTempC,1)),"  objTempC="+ str(round(objTempC,1)) )

"""post process"""
res2 = np.array(res)
np.savetxt("d06_pi30_gap5mm_060deg.csv",res2,delimiter=",")
plt.plot(res2[:,0],res2[:,2],".-")
print("--------------------------------------")
print("Tave: ",np.average(res2[:,2]))
print("Vave: ",np.average(res2[:,3]))

"""check register"""
sensor.readConfig()
sensor.readCoeff()
sensor.readStatusmask()
sensor.readAlert()
#sensor.readStatus


