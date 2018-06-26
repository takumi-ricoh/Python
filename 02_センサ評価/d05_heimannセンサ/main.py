# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:48:26 2018

@author: p000495138
"""
import ctypes
import time
import itertools
from pkg_read import sensor_mdl
from pkg_read import machine_mdl
from pkg_plot import plot_mdl
from pkg_config import sensor_cfg_mdl 
from pkg_config import machine_cfg_mdl
from pkg_config import plotter_cfg_mdl
from pkg_save import save_mdl

#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          

#%%パラメータ
sensor_param     = sensor_cfg_mdl.get_cfg()

machine_param    = machine_cfg_mdl.get_cfg()

plotter_param    = plotter_cfg_mdl.get_cfg()

#%% 基準時刻を取得する
t0 = int(time.time())

#%%オブジェクト生成
#サーモパイル
#sensor  = sensor_mdl.SensorLog(sensor_param,t0)
sensor = sensor_mdl.SensorLog(sensor_param,t0)
#マシンログ
machine = machine_mdl.MachineLog(machine_param,t0)
#プロット
plotter = plot_mdl.Plotter(plotter_param)

#セーブ用
#saver   = save_mdl.Saver()

#%%データ取得スタート
sensor.start()
machine.start()

#センサ数取得
sensor_number = sensor.senNum


#%%グラフ化するキー組み合わせ
f22_key1 = ["f22"]
f22_key2 = ["Sen1","Sen3"]
f22_key3 = ["Tar","Cur"]
f22_keys = list(itertools.product(f22_key1,f22_key2,f22_key3))
f26_key1 = ["f26"]
f26_key2 = ["Heater1"]
f26_key3 = ["Duty"]
f26_keys = list(itertools.product(f26_key1,f26_key2,f26_key3))
machine_keys = f22_keys + f26_keys

thermopile_key1 = ["sensor"]
thermopile_key2 = ["obj"]
thermopile_key3 = ["obj" + str(i) for i in range(sensor_number)]
thermopile_keys = list(itertools.product(thermopile_key1,thermopile_key2,thermopile_key3))
couple_key1     = ["sensor"]
couple_key2     = ["obj"]
couple_key3     = ["couple1","couple2"]
couple_keys     = list(itertools.product(couple_key1,couple_key2,couple_key3))
sensor_keys     = thermopile_keys + couple_keys

plotter.sensor.init_line(sensor_keys)
plotter.machine.init_line(machine_keys)


#%%繰り返し処理

while True:
    #データ取得
    sensor_data   = sensor.get_value()
    #machine_data  = machine.get_value()

    #プロットの更新
    plotter.sensor.update(sensor_data)
    #plotter.machine.update(machine_data)
    
    #描画の更新
    plotter.sensor.draw_update()
    #plotter.machine.draw_update()
    
    # ESCキーが押されたら終了
    if getkey(ESC):
       break
   
    sensor.stop()
    
    time.sleep(.5)

#%%繰り返し処理
