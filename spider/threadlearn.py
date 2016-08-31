#!/usr/bin/env python
#-*- coding:utf-8 -*-
import threading
import datetime
import urllib2
import time
import Queue

share = Queue.Queue()
worker_thread_num = 3

class MyThread(threading.Thread):
    
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.func()

def worker():
    global share
    while not share.empty():
        item = share.get()
        print 'Processing: ', item
        time.sleep(1)

def main():
    global share
    threads = []
    for task in xrange(5):
        share.put(task)
    for i in xrange(worker_thread_num):
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main



