# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:11:14 2017

@author: p000495138
"""

from msvcrt import getch
import time

try:
   while True:
       key = ord(getch()) #ord葉キーボードを数値とする。    
       print(key)
       time.sleep(1)
except KeyboardInterrupt:
    print("end")
