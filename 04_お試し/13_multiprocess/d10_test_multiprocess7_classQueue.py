# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 09:30:11 2018

@author: p000495138
"""

from multiprocessing import Queue
import multiprocessing
import time

class Test1Worker(multiprocessing.Process):

    def __init__(self,interval,q):
        super(Test1Worker, self).__init__()
        self.interval = interval
        self.q = q
 
    def run(self):
        while True:
            time.sleep(self.interval)
            print("Test1Woker:QueuePut") 
            self.q.put(("TEST1","TEST2"))



class Test2Worker(multiprocessing.Process):

    def __init__(self,q):
        super(Test2Worker, self).__init__()
        self.q = q
 
    def run(self):
        while True:
            data = self.q.get()
            print("Test2Woker:QueueReadValue")
            print('Queue[0]:'+data[0])
            print('Queue[1]:'+data[1] )


def main():
    q = Queue()
    jobs = [
        Test1Worker(5,q),
        Test2Worker(q)
        ]
    for j in jobs:
        j.start()

if __name__ == '__main__':
    main()