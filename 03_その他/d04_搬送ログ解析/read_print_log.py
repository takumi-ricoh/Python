# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:53:57 2020

@author: p000495138
"""
import glob
import pandas as pd


#%% 線速テーブル
vel_table = {"高速":276, "通常速":252, "中速":178, "低速":89, "標準速":100}


#%% センサ一覧
sensors =["F1給紙センサ",
"F2給紙センサ",
"LCT F1搬送センサ",
"LCT F2搬送センサ",
"LCT F3搬送センサ",
"バンク F3給紙センサ",
"バンク F４給紙センサ",
"レジストセンサ",
"レジストタイミングセンサ",
"両面センサ",
"両面入口センサ",
"両面出口センサ",
"反転センサ",
"定着入口センサ",
"定着出口センサ",
"排紙センサ",
"本体縦搬送センサ2",
"本体縦搬送センサ１",
"縦搬送センサ３",
"縦搬送センサ４",
"1bin排紙センサ",]

sensors_on  = [i + "_on" for i in sensors]
sensors_off = [i + "_off" for i in sensors]

#on/offをつけた一覧
sensors_onoff = sensors_on + sensors_off

#%% ファイルサーチ
files = glob.glob("d01_griffin/*") + glob.glob("d02_metis/*")
file = files[0]
#file = "両面5枚"

#%% ファイルを読む
raw_list = []
with open(file, mode='r', encoding='cp932') as f:
    for line in f:
        raw_list.append(line.strip())

#%%　プロセス情報
proc_keys_g = ["用紙長　[", "用紙幅　[", "給排紙先", "線速　 :", "紙種/紙厚",]
proc_keys_m = ["マシンタイプ（線速）"] #metis
proc_keys = proc_keys_g + proc_keys_m

#一旦抽出
proc_tmp_list = []
for idx,word in enumerate(raw_list):
    if any([key in word for key in proc_keys]):
        proc_tmp_list.append([idx, word[18:]])


#プロセス情報をまとめる関数
def read_proc(cur_dict, word):
    if "用紙長" in word:
        cur_dict["用紙長"] = float(word[12:])/10
    if "用紙幅" in word:
        cur_dict["用紙幅"] = float(word[12:])/10
    if "給排紙先" in word:
        cur_dict["給紙トレイ"] = word.split("\u3000")[1].split(":")[1]
        cur_dict["排紙トレイ"] = word.split("\u3000")[2].split(":")[1]
    if "線速" in word:
        cur_dict["タイプ"] = word.split(":")[1][0:4]
        cur_dict["線速"] = word.split(":")[1][5:-1]
        cur_dict["線速(数値)"] = vel_table[cur_dict["線速"]]
    if "紙種/紙厚" in word:
        cur_dict["紙種"] = word.split("\u3000")[1].split(":")[1].strip(" ")
        cur_dict["紙厚"] = word.split("\u3000")[2].split(":")[1].strip(" ")
        #metis/griffinの差分
        if "(" in cur_dict["紙厚"]:
            cur_dict["紙厚"]=cur_dict["紙厚"].split("(")[1][:-1]
    return cur_dict


#プロセス情報をひとまとめにする
proc_list = []
for i in proc_tmp_list:
    
    idx  = i[0]
    word = i[1]

    #用紙長さが来たら新しい辞書作成
    if "用紙長" in word :
        proc_list.append({})
        proc_list[-1]["idx"] = idx
        
    #最後のリストに追加していく
    cur_dict = proc_list[-1]

    #関数に通す
    cur_dict = read_proc(cur_dict, word)
    
    #リストに戻す
    proc_list[-1] = cur_dict


#%% 紙生成したidとセンサ値
"""
「紙生成」で分かったidのあとに出てくるセンサ値をとってくる
紙生成でid番号が宣言される前に表示された、センサ値は無視する
"""

#一旦、id番号とセンサ値を保存する
id_sens_data=[]
for idx,word in enumerate(raw_list):
    if ("紙：生成" in word) or ("紙：消滅" in word) :
        id_sens_data.append([idx, word[18:]])
    if ("センサ通知" in word) and ("ID:" in word):
        id_sens_data.append([idx, word[18:]])
    if "[割り込みセンサ]" in word:
        id_sens_data.append([idx, word[18:]])


#idとセンサ値を紐付けたカタマリを作る
sens_tmp_dict = {}  #一時データ
sens_list     = []  #完成データ(次の「紙生成」が来たら完成したと判断)

for idx,i in enumerate(id_sens_data):
    cur_idx  = i[0]
    cur_word = i[1]
    cur_id   = cur_word[-1]

    #紙生成が来たとき
    if "紙：生成" in cur_word:
        #sens_tmp_dictに空リストを作る
        if cur_id not in sens_tmp_dict.keys():
            sens_tmp_dict[cur_id] = {"idx":cur_idx,#インデックス
                                     "id":cur_id , #id
                                     "value":{}.fromkeys(sensors_onoff),#センサ値
                                     "flg":{}.fromkeys(sensors_onoff)}  #単位変換必要かのフラグ

    #紙消滅が来た時
    elif "紙：消滅" in cur_word:
        #値をresultに移し、sens_tmp_dictは空にする
        if cur_id  in sens_tmp_dict.keys():
            sens_list.append(sens_tmp_dict[cur_id])
            sens_tmp_dict.pop(cur_id)

    #そうでなければ、データをsens_tmp_listに追加していく
    else:
        if cur_id in sens_tmp_dict.keys():
            sens_val = cur_word.split("：")[1].split("　")
            
            #===センサ名===
            #センサ名を抽出して、_on,_offをつける
            if ("ＯＮ" in sens_val[0]):   
                sens_name  = sens_val[0].split("ＯＮ")[0] + "_on"
            if ("ON" in sens_val[0]):   
                sens_name  = sens_val[0].split("ON")[0] + "_on"
            if ("ＯＦＦ" in sens_val[0]):   
                sens_name  = sens_val[0].split("ＯＦＦ")[0] + "_off" 
            if ("OFF" in sens_val[0]):   
                sens_name  = sens_val[0].split("OFF")[0] + "_off"                 
            
            
            #===センサ誤差値====
            #文字列抽出
            # A.レジストセンサの場合：特殊抽出
            if "レジスト" in sens_name:
                reg_cur_word = id_sens_data[idx+1][1]
                sens_err1  = reg_cur_word.split(": 　")[1].split(":")[1]
            
            # B.その他の場合
            else:
                sens_err1  = sens_val[1].split(":")[1]
                
                
            #単位除く
            sens_err2  = sens_err1.split("m")[0]
            #±0対応
            if sens_err2 == "±0":
                sens_err2 = 0
            else:
                sens_err2 = int(sens_err2)
            #保存
            sens_tmp_dict[cur_id]["value"][sens_name] = sens_err2


            #===単位変換必要フラグ===
            if "ms" in sens_err1:
                sens_tmp_dict[cur_id]["flg"][sens_name] = 0
            if "mm" in sens_err1:
                sens_tmp_dict[cur_id]["flg"][sens_name] = 1

#%% まとめる
result_list=[]
for sens in sens_list:
    for proc in proc_list:
        if proc["idx"] > sens["idx"]:
            result_list.append({**proc,**sens})
            break

#%% valueは分ける
value_list = []
for sens in result_list:
    value_list.append(sens.pop("value"))


#%% 単位変換するかのフラグ
flg_list = []
for sens in result_list:
    flg_list.append(sens.pop("flg"))

#%% dataframe
df1 = pd.DataFrame(result_list) #プロセス
df2 = pd.DataFrame(value_list)  #センサ誤差
df3 = pd.DataFrame(flg_list)    #単位変換フラグ

#速度をかけたもの
df2_ = df2.div(1/df1["線速(数値)"],axis=0)/1000

#df3=1の場合はdf2を、df3=0の場合はdf2_を使う
df2_new = df2*df3 + df2_*(1-df3)

#プロセス情報とセンサ情報をあわせる
df  = pd.concat([df1,df2_new],axis=1)

#idxでソート
df = df.sort_values("idx")

#%% csv保存
savename = "result/" + file.split("\\")[1] + "_result.csv"
df.to_csv(savename, encoding='utf-8-sig')