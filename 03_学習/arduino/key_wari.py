# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:16:05 2017

@author: p000495138
"""

import os
import sys
import signal
import time

pid = os.fork()

if pid == 0:
    i = 1
    while True:
        print(i)
        time.sleep(1)
        i = i + 1
    sys.exit()
else:
    while True:
        c = sys.stdin.read(1)
        if c == ' ':
            os.kill( pid, signal.SIGTERM )
            sys.exit()