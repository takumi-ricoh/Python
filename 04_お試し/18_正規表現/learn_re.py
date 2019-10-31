# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:10:13 2019

@author: r00495138
"""

import re

#ライブラリ登録
lib = "@f22@|[Sensor{0}]|027:28.020 |Tar=,{1},Cur=,{2},Sen=,{3},Air=,{4},"
#lib = "@f22@|[Sensor#0#|027:28.020 |Tar=,#1#,Cur=,#2#,Sen=,#3#,Air=,#4#,"
lib_word = {}


#パターン登録
#PATTERN = r'([-0-9]*\.?[-0-9]+)'

#1文字ずつ抽出
#PATTERN = r"\d"  #任意の数字
#PATTERN = r"\D"  #任意の数字以外
#PATTERN = r"\s"  #任意の空白
#PATTERN = r"\S"  #任意の空白以外
#PATTERN = r"\w"  #任意の英数字
#PATTERN = r"\W"  #任意の英数字以外
#PATTERN = r"\A"   #文字列の先頭
#PATTERN = r"\Z"   #文字列の末尾
#PATTERN = r"."    #任意の一文字
#PATTERN = r"^"    #文字列の先頭
#PATTERN = r"$"   #文字列の末尾
#PATTERN  = r"\d*"   #0回以上の繰り返し
#PATTERN  = r"\d+"   #1回以上の繰り返し
#PATTERN  = r"\d?"   #0回or1回
PATTERN  = r'\d{3}'   #m回の繰り返し
#PATTERN  = r"\d{2,3}"   #m～n回の繰り返し
#PATTERN  = r"[a-f]"   #集合

#{数字}部を抽出
#PATTERN  = r"{\d+}"
#PATTERN  = r'{\d+}'

#検出内容
data = "@f22@|[Sensor1|027:28.020 |Tar=,060,Cur=,157,Sen=,157,Air=,000,"


#結果
find = re.findall(PATTERN,data)
#find = re.finditer(PATTERN,lib)
#find = re.match(PATTERN,lib)
#find = re.search(PATTERN,lib)

#find.group()
for i in find:
    print(i)