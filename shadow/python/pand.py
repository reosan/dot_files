#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import numpy as np
import pandas as pd
import math
import sys
import time
import threading
#import seaborn

from selenium_def import *
from selenium_class import *
from plot_def import *
from backtest_def import *
import colors as C

'''
ts = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype='f8', name='past_close')
print(ts)
#ts = ts.drop(5)
del ts[5]
print(ts)
ts = ts.append(pd.Series([10]), ignore_index=True)
#ts.reset_index(drop=True)
print(ts)
'''

LOGIN_URL = 'https://demotrade.fx.dmm.com/fxcrichpresen/webrich/direct/login'
LOGIN_URL = 'http://example.selenium.jp/reserveApp_Renewal/' # テスト用URL
PROFILE = '/home/reosan/.mozilla/firefox/i1zq2uyh.selenium'

try: 
    profile = webdriver.FirefoxProfile(PROFILE)
    driver = webdriver.Firefox(firefox_profile=profile)
    wait = WebDriverWait(driver, 1)
    wait_5 = WebDriverWait(driver, 5)    
    wait_10 = WebDriverWait(driver, 10)
    wait_20 = WebDriverWait(driver, 20)
    #driver.implicitly_wait(10)

    driver.get(LOGIN_URL)
    driver.find_element_by_id('accountId').send_keys(ID)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('LoginWindowBtn').click()

    wait_20.until(EC.number_of_windows_to_be(2))
    window = driver.window_handles[-1]
    driver.get('http://www.google.co.jp')
    driver.switch_to_window(window)

    elem_spread = wait_get_elem_xpath(wait_20, '//div[@uifield="spread"]')
    price_bid = wait_get_elems_xpath(wait_20, '//div[@uifield="bidStreamingButton"]/div/*')    
    price_ask = wait_get_elems_xpath(wait_20, '//div[@uifield="askStreamingButton"]/div/*')
    button_order_all = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonAll"]')
    button_bid = wait_get_elem_xpath(wait_20, '//div[@uifield="bidStreamingButton"]')
    button_ask = wait_get_elem_xpath(wait_20, '//div[@uifield="askStreamingButton"]')
    text_order_Lot = wait_get_elem_xpath(wait_20, '//input[@uifield="orderQuantity"]')
    button_logout = wait_get_elem_xpath(wait_20, '//div[@class="logout label"]')
except:
    print(C.R + C.BOLD + 'CAN NOT CONNECT DMM !!!' + C.RESET, file=sys.stderr)
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise


try: ###$ ts fetch
    for i in range(3):
        text_order_Lot.send_keys(Keys.BACK_SPACE)
    text_order_Lot.send_keys(LOT) 
    event = threading.Event()
    FF = FirstFetch(price_bid, count=13)
    FF.start()
    ts = FF.ts
    print(FF.ts)
except:
    print(C.R + C.BOLD + 'ERROR OCCURRED IN FirstFetch !!!' + C.RESET, file=sys.stderr)
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise
    



try: ###$ bid & ask
    F = Fetch(price_bid, ts=ts, event=event, sec=1.0)
    F.start()

    print(type(EC.element_to_be_clickable(button_order_all)))
    hoge = 0
    while True:
        event.wait()
        
        ts = F.ts
        spread = elem_spread.text
        S = ts.ewm(span=SPAN_S).mean().values[-1]
        # S = ts.ewm(span=SPAN_S).mean()[-1:].values[0]
        M = ts.ewm(span=SPAN_M).mean().values[-1]
        L = ts.ewm(span=SPAN_L).mean().values[-1]

        # WebDriverWait(driver, timeout=X, ignored_exceptions=True)
