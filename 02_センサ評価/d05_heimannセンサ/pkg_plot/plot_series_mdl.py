# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:17:46 2018

@author: takumi
"""

import matplotlib.pyplot as plt

#%%時系列グラフの親クラス
class TimeSeries():

    def __init__(self, fig, ax, ylim):

        #初期設定
        self.ax.set_xlabel("time")
        self.ax.set_ylabel("temperature")        
        self.ax.grid(True)
        self.ax.set_ylim(0,300) 
      
        #グラフ初期化
        self.fig.canvas.draw()
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)
    
    def draw_update(self):
        #ライン更新
        self.fig.canvas.restore_region(self.bg)
        self.fig.canvas.draw()
        #画面の更新
        self.fig.canvas.update()
        self.fig.canvas.flush_events()


#%%センサ時系列    
class SensorSeries(TimeSeries):
        
    def __init__(self, fig, ax,):
        self.fig    = fig
        self.ax     = ax

        super().__init__(self.fig, self.ax,)

    def init_line(self,data):
        #センサ数を確認
        self.num   = data["num"]
        self.lines = []
        #センサ数だけ初期プロット
        for i in range(self.num):
            self.lines.append(self.ax.plot(0,0,".-")[0])
            plt.hold(True)    

        #その他(熱電対)
        self.others = []
        self.others.append(self.ax.plot(0,0,".-")[0])
        self.others.append(self.ax.plot(0,0,".-")[0])

    def update(self,data):
        #npデータ
        self.time    = data["time"]
        self.couple  = data["couple"]
        self.num     = data["num"]
        self.obj     = data["obj"]        
        self.amb     = data["amb"]        

        #検知温度           
        for idx,line in enumerate(self.lines):
            line.set_data(self.time, self.num[:,idx])
            self.ax.draw_artist(self.line)

        #熱電対
        self.others[0].set_data(self.time, self.couple[:,0])      
        self.ax.draw_artist(self.others[0])
        self.others[1].set_data(self.time, self.couple[:,1])      
        self.ax.draw_artist(self.others[1])

#%%マシンログ時系列    
class MachineSeries(TimeSeries):
        
    def __init__(self, fig, ax,):
        self.fig    = fig
        self.ax     = ax

        super().__init__(self.fig, self.ax,)

    def init_line(self):
        #データ構造初期化
        self.f22_lines = {"Sen1":None, "Sen3":None}
        self.f26_lines = {"Heater1":None, "Heater2":None}

        self.f22_lines["Sen1"] = {"Tar":None, "Cur":None}
        self.f22_lines["Sen3"] = {"Tar":None, "Cur":None}

        self.f26_lines["Heater1"] = {"FFduty":None,"Duty":None}
        self.f26_lines["Heater2"] = {"FFduty":None,"Duty":None}
        
        #プロット初期化
        self.f22_lines["Sen1"]["Tar"] = self.ax.plot(0,0,".-")[0]
        self.f22_lines["Sen1"]["Cur"] = self.ax.plot(0,0,".-")[0]
        self.f22_lines["Sen3"]["Tar"] = self.ax.plot(0,0,".-")[0]        
        self.f22_lines["Sen3"]["Cur"] = self.ax.plot(0,0,".-")[0]

        self.f26_lines["Heater1"]["FFduty"] = self.ax.plot(0,0,".-")[0]
        self.f26_lines["Heater1"]["Duty"]   = self.ax.plot(0,0,".-")[0]
        self.f26_lines["Heater2"]["FFduty"] = self.ax.plot(0,0,".-")[0]        
        self.f26_lines["Heater2"]["Duty"]   = self.ax.plot(0,0,".-")[0]        

    def update(self,data):
        #辞書&pandasデータ
        self.f22     = data["f22"]
        self.f26     = data["f26"]

        #データ更新
        self.f22_lines["Sen1"]["Tar"].set_data(self.f22["Sen1"]["time"], self.f22["Sen1"]["Tar"])
        self.f22_lines["Sen1"]["Cur"].set_data(self.f22["Sen1"]["time"], self.f22["Sen1"]["Cur"])
        self.f22_lines["Sen3"]["Tar"].set_data(self.f22["Sen3"]["time"], self.f22["Sen3"]["Tar"])
        self.f22_lines["Sen3"]["Cur"].set_data(self.f22["Sen3"]["time"], self.f22["Sen3"]["Cur"])

        self.f26_lines["Heater1"]["FFduty"].set_data(self.f26["Heater1"]["time"], self.f26["Heater1"]["FFduty"])
        self.f26_lines["Heater1"]["Duty"]  .set_data(self.f26["Heater1"]["time"], self.f26["Heater1"]["Duty"])
        self.f26_lines["Heater2"]["FFduty"].set_data(self.f26["Heater2"]["time"], self.f26["Heater2"]["FFduty"])
        self.f26_lines["Heater2"]["Duty"]  .set_data(self.f26["Heater2"]["time"], self.f26["Heater2"]["Duty"])


        #プロット更新
        self.ax.draw_artist(self.self.f22_lines["Sen1"]["Tar"])
        self.ax.draw_artist(self.self.f22_lines["Sen1"]["Cur"])
        self.ax.draw_artist(self.self.f22_lines["Sen3"]["Tar"])
        self.ax.draw_artist(self.self.f22_lines["Sen3"]["Cur"])
        self.ax.draw_artist(self.self.f26_lines["Heater1"]["FFduty"])
        self.ax.draw_artist(self.self.f26_lines["Heater1"]["Duty"])
        self.ax.draw_artist(self.self.f26_lines["Heater2"]["FFduty"])
        self.ax.draw_artist(self.self.f26_lines["Heater2"]["Duty"])
