# -*- coding: utf-8 -*-
"""
パラメータ
"""

import serial
import pandas as pd
import numpy as np

#%%設定関数
def get_config():    
    #%% 初期値SPパラメータ
    df0 = pd.read_csv("sp_param.csv",engine="python")
    df0 = df0.rename(df0["説明2"])
    
    #%% 設定用パラメータ
    param = df0["初期値"]
    param = param.rename(df0["説明2"])
    
    #%% 値変更param["係数a/紙1/幅1"] = 95
    
    #係数a
    param["係数a/紙1/幅1"] = 95
    param["係数a/紙1/幅2"] = 95
    param["係数a/紙1/幅3"] = 95
    param["係数a/紙2/幅1"] = 95
    param["係数a/紙2/幅2"] = 95
    param["係数a/紙2/幅3"] = 95
    param["係数a/紙3/幅1"] = 95
    param["係数a/紙3/幅2"] = 95
    param["係数a/紙3/幅3"] = 95
    for idx,i in param.iteritems():
        if "係数a" in idx:
            param[idx] = 90
    #係数b
    param["係数b/紙1/幅1"] = 0.01
    param["係数b/紙1/幅2"] = 0.01
    param["係数b/紙1/幅3"] = 0.01
    param["係数b/紙2/幅1"] = 0.01
    param["係数b/紙2/幅2"] = 0.01
    param["係数b/紙2/幅3"] = 0.01
    param["係数b/紙3/幅1"] = 0.01
    param["係数b/紙3/幅2"] = 0.01
    param["係数b/紙3/幅3"] = 0.01
    for idx,i in param.iteritems():
        if "係数b" in idx:
            param[idx] = 0.01

    #判定1閾値
    param["判1/ﾓｰﾄﾞ1/紙1/幅1"] = 200
    param["判1/ﾓｰﾄﾞ1/紙1/幅2"] = 200
    param["判1/ﾓｰﾄﾞ1/紙2/幅1"] = 200
    param["判1/ﾓｰﾄﾞ1/紙2/幅2"] = 200
    param["判1/ﾓｰﾄﾞ1/紙3/幅1"] = 200
    param["判1/ﾓｰﾄﾞ1/紙3/幅2"] = 200
    param["判1/ﾓｰﾄﾞ2/紙1/幅1"] = 200
    param["判1/ﾓｰﾄﾞ2/紙1/幅2"] = 200
    param["判1/ﾓｰﾄﾞ2/紙2/幅1"] = 200
    param["判1/ﾓｰﾄﾞ2/紙2/幅2"] = 200
    param["判1/ﾓｰﾄﾞ2/紙3/幅1"] = 200
    param["判1/ﾓｰﾄﾞ2/紙3/幅2"] = 200
    for idx,i in param.iteritems():
        if "判1" in idx:
            param[idx] = 200

    #判定2閾値
    param["ﾓｰﾄﾞ1/P1"] = 1
    param["ﾓｰﾄﾞ1/P2"] = 0.75
    param["ﾓｰﾄﾞ1/閾値"] = 500
    param["ﾓｰﾄﾞ2/P1"] = 1
    param["ﾓｰﾄﾞ2/P2"] = 0.75
    param["ﾓｰﾄﾞ2/閾値"] = 500
    
    #%%ステップ設定
    param2 = param/df0["ステップ"]
    param2 = np.int32(param2)
    
    #%% コマンド生成
    spn1 = df0["大分類"].astype("str")
    spn2 = df0["小分類"].astype("str")
    spn3 = df0["細分類"].astype("str")
    spn  = "spw"+" "+spn1+" "+spn2+" "+spn3+" "
    spn  = spn.rename(df0["説明2"])
    
    commands = spn + param2.astype("str")
    
    return commands

