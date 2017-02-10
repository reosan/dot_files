from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import pandas as pd
import math
import sys
import time
import threading

from def_sele import *

class Fetch(object):
    def __init__(self, price, ts=pd.Series([]), event=threading.Event(), sec=1.0, itr_num=5, DEBUG=False):
        self.DEBUG = DEBUG ##
        self.post_time = 0.0
        self.time = 0.0
        self.sec = sec 
        self.itr_num = itr_num
        self.count = 0
        self.price = price
        self.ts = ts
        self.event = event
        self.temp = 0.0
        self.thread = threading.Thread(target=self.fetch, daemon=True)
        #?self.thread.setDaemon(True)

    def start(self):
        self.event.clear()
        self.thread.start()

    def fetch(self):
        self.timer = threading.Timer(self.sec, self.fetch)
        self.timer.start()
        self.time = time.time()
        self.temp = float_price(self.price, self.DEBUG)
        self.event.clear()
        self.ts = self.ts.append(pd.Series([self.temp]), ignore_index=True)
        del self.ts[0]
        self.ts = self.ts.reset_index(drop=True)
        self.post_time = time.time()
        self.event.set()
        self.count += 1
        
    def cancel(self):
        self.timer.cancel()


class FirstFetch(Fetch):
    def start(self):
        self.event.clear()
        self.thread.start()

    def fetch(self):
        if len(self.ts) >= self.itr_num:
            print('FirstFetch completed.', file=sys.stderr)
            self.event.set()
            return
        self.timer = threading.Timer(self.sec, self.fetch)
        self.timer.start()
        self.temp = float_price(self.price, self.DEBUG)        
        self.ts = self.ts.append(pd.Series([self.temp]), ignore_index=True)
        print('\033[K' + str(len(self.ts)) + '/' + str(self.itr_num) + '\033[A', file=sys.stderr)         

        
class Print(object):
    @staticmethod
    def print(arg, file=1):
        if file in (1, 'out' ,'stdout'):
            print(str(arg) + '\033[0m', file=sys.stdout)
        elif file in (2, 'err' ,'stderr'):
            print(str(arg) + '\033[0m', file=sys.stderr)
        else:
            raise Exception('error Print.print() args is invalid!')
            
class OrderException(Exception):
    pass
