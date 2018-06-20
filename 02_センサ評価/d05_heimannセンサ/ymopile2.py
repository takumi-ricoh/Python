# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:48:26 2018

@author: p000495138
"""
import ctypes
from pkg_read import sensor_mdl
from pkg_read import machine_mdl
from pkg_read import plot_mdl
from pkg_config import sensor_cfg_mdl 
from pkg_config import machine_cfg_mdl
from pkg_config import plotter_cfg_mdl
from pkg_save import save_mdl

#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          

#%%パラメータ
slog_param    = sensor_cfg_mdl.SensorConfig()
mlog_param    = machine_cfg_mdl.MachineConfig()
plotter_param = plotter_cfg_mdl.PlotterConfig()

#%%オブジェクト生成
sensor  = sensor_mdl.Sensors(slog_param)
machine = machine_mdl.Machine(mlog_param)
plotter = plot_mdl.Plotter(plotter_param)
saver   = save_mdl.Saver()
#%%プロット初期化
plotter.init()

#%%データ取得スタート
sensor.start()
machine.start()

#%%繰り返し処理
while True:
    #データ取得
    sensor_tmp   = sensor.get_value()
    machine_data = machine.get_value()
    #プロットの更新
    plotter.sensor.update(sensor_tmp)
    plotter.machine.update(sensor_tmp)
    
    # ESCキーが押されたら終了
    if getkey(ESC):
       break