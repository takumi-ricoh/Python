# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:05:40 2018

@author: p000495138
"""

import multiprocessing
import time

class Test1Worker(multiprocessing.Process):

    def __init__(self,interval):
        super(Test1Worker, self).__init__()
        self.interval = interval
 
    def run(self):

        while True:
            time.sleep(self.interval)
            print("Test1Woker")


class Test2Worker(multiprocessing.Process):

    def __init__(self,interval):
        super(Test2Worker, self).__init__()
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            print("Test2Woker")

def main():

    jobs = [
        Test1Worker(5),
        Test2Worker(10)
        ]
 
    for j in jobs:
        j.start() 
    for j in jobs:
        j.join() 

if __name__ == '__main__':
    main()