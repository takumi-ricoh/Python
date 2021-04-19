# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:23:35 2020

@author: p000495138
"""

import numpy as  np


class GetCalc:
    
    def __init__(self,data):
        self.data = data
        
    def get_sum(self):
        return np.sum(self.data)
    
    def get_var(self):
        return np.var(self.data)


