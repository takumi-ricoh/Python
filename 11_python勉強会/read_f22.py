# -*- coding: utf-8 -*-
"""
python勉強会
エンジンログのうち、f22について、抽出する
"""
import numpy as np
import pandas as pd

#%% データ抽出
"""
 mode は、ファイルが読み出し専用なら 'r' 、書き込み専用 (同名の既存のファイルがあれば消去されます) なら 'w' とします。
 'a' はファイルを追記用に開きます。ファイルに書き込まれた内容は自動的にファイルの終端に追加されます。 
 'r+' はファイルを読み書き両用に開きます。 
 mode 引数は省略可能で、省略された場合には 'r' であると仮定します。
"""

#リストに読み込む
tmp_list = []
with open('fusMd_engine_log2.txt', mode='r', encoding='utf-8') as f:
    for line in f:
        tmp_list.append(line.strip())
        
#f22のsensor1抽出
key1 = "@f22@|[Sensor1]"
key2 = "Dbg"
f22_list = []
for tmp_line in tmp_list:
    if (key1 in tmp_line) and (key2 not in tmp_line):
        f22_list.append(tmp_line)

#%%　f22        
def f22(data):
    #分ける
    temp1 = data
    temp2 = temp1.split('|')
    temp3 = temp2[-1].split(',')
    #時刻を計算
    time_str = temp2[2].split(':')
    time = float(time_str[0])*60 + float(time_str[1]) #秒単位換算
    #数値に変換
    Tar = np.float64(temp3[1])
    Cur = np.float64(temp3[3])
    #センサ種類
    Sen = temp2[1]
    #print(Sensor)
    return [time,Tar,Cur]
        
#%% 分割する
f22_splited_list = []
for tmp in f22_list:
    f22_splited_list.append(f22(tmp))

#%% データフレームに変換
df = pd.DataFrame(f22_splited_list)
df.columns = ["sec","target","current"]

#%% プロット
df.plot(x="sec",y=["target","current"],grid=True)

#%% データをCSVファイルとして出力する
df.to_csv("f22data.csv")