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
sensor_param     = sensor_cfg_mdl.set_cfg()

machine_param    = machine_cfg_mdl.set_cfg()

plotter_param    = plotter_cfg_mdl.set_cfg()

#%%オブジェクト生成

sensor  = sensor_mdl.Sensors(sensor_param)

machine = machine_mdl.Machine(machine_param)

plotter = plot_mdl.Plotter(plotter_param)

saver   = save_mdl.Saver()


#%%データ取得スタート
sensor.start()
machine.start()

#%%グラフ初期化

sensor_dict   = sensor.get_value()
machine_dict  = machine.get_value()

plotter.sensor.init_line(sensor_dict)
plotter.machine.init_line(machine_dict)

#%%繰り返し処理
while True:
    #データ取得
    sensor_dict   = sensor.get_value()
    machine_dict  = machine.get_value()

    #プロットの更新
    plotter.sensor.update(sensor_dict)
    plotter.machine.update(machine_dict)
    
    #描画の更新
    plotter.sensor.draw_update()
    plotter.machine.draw_update()
    
    # ESCキーが押されたら終了
    if getkey(ESC):
       break

#%%繰り返し処理

