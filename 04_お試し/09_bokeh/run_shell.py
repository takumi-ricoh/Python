# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 20:40:22 2018

@author: p000495138
"""

import subprocess

cmd = 'bokeh serve --show d04_bokeh_realtime3.py'
returncode = subprocess.Popen(cmd, shell=True)
