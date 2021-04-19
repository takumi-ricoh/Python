# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:52:02 2019

@author: r00495138
"""

import re

#%%正規表現用
class RegularExpression:
    
    def __init__(self,form):
        self._form  = form
        self._form2 = self._preprocessing(self._form)
    
    #前段階
    def _preprocessing(self,raw):
        reform = raw.replace("|","\|")
        reform = reform.replace("[","\[")
        reform = reform.replace("]","\]")
        reform = reform.replace("$","\$")    
        #reform = re.sub(r'{\d+}', r'(\\w+)', reform)
        reform = re.sub(r'{\d+}', r'(.+)', reform)
        return reform
    
    #マッチング  
    def matching(self,src):
        #マッチング
        #m = re.fullmatch(self.form2, src)        
        m = re.search(self._form2,src)
        if m==None:
            return None
        else:
            return list(m.groups())

#%%データ読み出し
FILENAME = "engine.log"
with open(FILENAME,encoding="utf-8") as f:
    l_strip = [s.strip() for s in f.readlines()]

#%%ログフォーム登録(ユーザ)
form1 = "@f22@|[Sensor1]|{0} |Tar=,{1},Cur=,{2},Sen=,{3},Air=,{4},"
form2 = "@f30@|[Sensor1]|{0} |PreTar=,{1},ReTar=,{2},env_temp=,{3},env_hum=,{4},env=,{5},rep=,{6},press_fb=,{7},image=,{8},first=,{9},curl=,{10},"
form3 = "@f06@|[Motor0]|{0} |Vel=,{1},mm/s,"
form4 = "[ProcessData] Kind={0},Length={1},Width={2},Thick={3},Color={4},Dpi={5}"
form5 = "@f01@|[FeedPermit1]|{0} |,OK,"
form6 = "@fu@|PD|{0} |K={1},T={2},W={3},L={4},C={5},V={6},"
form7 = "[K]MBD,DrvDuty={0},n={1},DrvDutyAve={2},TnrSplyAbility={3}>700,Thresh={4},Value={5},EnvThresh={6},EnvValue={7}"

forms = [form1,form2,form3,form4,form5,form6,form7]

#%%実行
Forms = [RegularExpression(form) for form in forms]
res   = [[],[],[],[],[],[],[]]

for src in l_strip:
    for idx,Form in enumerate(Forms):
        tmp = Form.matching(src)
        if tmp is not None:
            res[idx].append(tmp)