# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:04:49 2019

@author: r00495138
"""
import re
text = "I'm a string that contains this characters {}, [], ()"
slice = "this characters \{}, \[], \(\)"
print([ m for m in re.finditer(slice, text) ])
#print([ (m.start(0), m.end(0)) for m in re.finditer(slice, text) ])

