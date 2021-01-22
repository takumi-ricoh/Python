# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 18:09:12 2020

@author: p000495138
"""

#%% データ読み
data = []
with open('d01_griffin/両面5枚', mode='r', encoding='cp932') as f:
    for line in f:
        data.append(line.strip())
res = []

#%% 紙生成とIDだけ抽出
for i in data:
    if "紙：生成" in i:
        res.append(i)
    if ("センサ通知" in i) and ("ID:" in i):
        res.append(i)

#%% 結果格納
tmp_dict={}  #一時データ
result = []  #完成データ(次の「紙生成」が来たら完成したと判断)

for i in res:
    cur_id = i[-1]

    #紙生成が来たとき
    if "紙：生成" in i:
        
        #もしキーが無ければ(初回)　キー作成
        if cur_id not in tmp_dict.keys():
            tmp_dict[cur_id] = {"id":cur_id, "value":[]}

        #そうでなければ値をresultに移し、tmp_dictは空リストにする
        else:
            result.append(tmp_dict[cur_id])
            tmp_dict[cur_id] = {"id":cur_id, "value":[]}

    #そうでなければ、データをtmp_listに追加していく
    else:
        if cur_id in tmp_dict.keys():
            tmp_dict[cur_id]["value"].append(i)