# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 19:41:37 2018

@author: p000495138
"""

import itertools

def make_key(words):
    key = list(itertools.product(words["key1"],words["key2"],words["key3"]))
    return key

class Cfg():
    def __init__(self,sensor_cfg):
        
        self.SENPOS = sensor_cfg.SENPOS
        self.SENNUM = sensor_cfg.SENNUM

        self.F22_W   = {"key1":["f22"], "key2":["Sen1","Sen3"], "key3":["Tar","Cur"]}
        self.F26_W   = {"key1":["f26"], "key2":["Heater1"], "key3":["Duty"]}

        self.THERMOPILE_W   = {"key1":["sensor"], "key2":["obj"],       "key3":["obj" + str(i) for i in range(self.SENNUM)]}
        self.COUPLE_W       = {"key1":["sensor"], "key2":["couple"],    "key3":["couple1","couple2"]}

        self.F22_KEY            = make_key(self.F22_W)
        self.F26_KEY            = make_key(self.F26_W)
        self.THERMOPILE_KEY     = make_key(self.THERMOPILE_W)
        self.COUPLE_KEY         = make_key(self.COUPLE_W)

        self.MACHINE_KEY   = self.F22_KEY + self.F26_KEY
        self.SENSOR_KEY    = self.THERMOPILE_KEY + self.COUPLE_KEY
        self.DIST_KEY      = make_key({"key1":["sensor"],"key2":["obj"],"key3":[""]})