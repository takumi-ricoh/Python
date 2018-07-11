# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:48:26 2018

*******   Matplotlibを使うパターン   ********

@author: p000495138
"""
from PyQt5.QtWidgets import QApplication
import sys
import ctypes
import time
from pkg_read import sensor_mdl
from pkg_read import machine_mdl
from pkg_plot_qt import plot_mdl
from pkg_config import sensor_cfg_mdl 
from pkg_config import machine_cfg_mdl
from pkg_config import plotter_cfg_mdl
from pkg_save import save_mdl

#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          

#%%スタート
if __name__ == '__main__':

    #%% GUI
    #インスタンスが無い場合のみ新たに作成
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    #%%パラメータ
    sensor_cfg     = sensor_cfg_mdl.Cfg()
    
    machine_cfg    = machine_cfg_mdl.Cfg()
    
    plotter_cfg    = plotter_cfg_mdl.Cfg(sensor_cfg)
    
    #%% 基準時刻を取得する
    t0 = time.time()
    
    #%%オブジェクト生成
    #サーモパイル
    sensor = sensor_mdl.SensorLog(sensor_cfg,t0)
    #マシンログ
    machine = machine_mdl.MachineLog(machine_cfg,t0)
    #プロット
    plotter = plot_mdl.Plotter(plotter_cfg)

    #セーブ用
    #saver   = save_mdl.Saver()    
    #%%データ取得スタート
    sensor.start()
    machine.start()
    
    #センサ数取得
    sensor_number = sensor.senNum
    
    #%%グラフの初期化
    
    #描画条件指定
    mac_plot_key    = plotter_cfg.MACHINE_KEY
    sen_plot_key    = plotter_cfg.SENSOR_KEY
    dist_plot_key   = plotter_cfg.DIST_KEY
    
    #グラフの初期化
    plotter.sensor_plot.init_line(sensor,sen_plot_key)
    plotter.machine_plot.init_line(machine,mac_plot_key)
    #plotter.dist_plot.init_line(dist_plot_key,plotter_cfg.SENPOS)
    
    #%%グラフ表示
    
    #表示スタート
    plotter.start()
    
    #%%終了処理
    if getkey(ESC):   
        sensor.stop() 
        machine.stop()