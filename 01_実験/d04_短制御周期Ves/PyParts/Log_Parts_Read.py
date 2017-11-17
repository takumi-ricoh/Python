# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:07:42 2017

@author: p000495138
"""

import numpy as np
import matplotlib.pyplot as plt

#%% bytes型ファイル読み出し(とりあえずファイルを全て開く)
def read_bytes(file):
    f=open(file,"rb")
    readbytes = f.readlines()
    f.close
    return readbytes

"""リスト化"""
def tolist(file):
    thisfile = read_bytes(file)
    datalist  = []
    for i in thisfile: #file[1]：中身
        try:
            temp = i.decode("cp932").strip() #文字列変換して改行を削除
            datalist.append(temp)
        except:
            pass
    return datalist         

"""分割"""
def splitdata(datalist):
    fuslist = []
    tmplist = []
    wavelist = []
    
    #とりあえず定着関係を抽出
    for i in datalist:
        if ("*FS" in i)or("Half" in i):#どちらか含まれたらとりあえず保存
            fuslist.append(i)        

    #先頭がHalfなら消す
    if "*Half" in fuslist[0]:
        del fuslist[0]
    
    #先頭から振り分け
    for i in fuslist:
        if ("*FS" in i)and("Half" in i):#両方含まれたらむし
            pass
        elif i.count("*FS")>1:#FSが２つ含まれたらむし
            pass
        elif i.count("Half")>1:#FSが２つ含まれたらむし
            pass        
        elif i[0:3] == "*FS":
            tmplist.append(i)
        elif i[0:16] == ">>> HalfWaveDuty":
            wavelist.append(i)

    #最後の1行は消す(欠損があるため)
    del(fuslist[-1])   
    del(tmplist[-1])   
    del(wavelist[-1])   
    return fuslist,tmplist,wavelist 
