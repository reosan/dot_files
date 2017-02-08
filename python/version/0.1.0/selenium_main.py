#!/usr/bin/python3
import selenium
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
import re
import datetime
#import seaborn

from selenium_def import *
from selenium_class import *
from plot_def import *
from backtest_def import *
import colors as C

#============================================================
ID = 
PASSWORD = 
LOGIN_URL = 'https://demotrade.fx.dmm.com/fxcrichpresen/webrich/direct/login'
PROFILE = '/home/reosan/.mozilla/firefox/i1zq2uyh.selenium'
MAIL_ADDRESS = ''
#------------------------------------------------------------
LOT = '1'
SPAN_S = 5
SPAN_M= 9
SPAN_L = 13
SPAN_LL = 30
itr_num = SPAN_L
sec = 1.0
sec_limit = sec - sec/100.0
LOOP_MAX = 100

EWMA_S = 0.0
EWMA_M = 0.0
EWMA_L = 0.0
EWMA_LL = 0.0
ts = None
n = 0
foo = 0

def logout_except():
    count = 0
    while True:
        count += 1
        button_order_all.click()
        time.sleep(1)
        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')):
            if count > 10:
                raise Exception('CAN NOT ORDER !!!')
            continue
        else:
            count = 0
            break
    while True:
        button_logout.click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@uifield="okButton"]')))
        except selenium.common.exceptions.TimeoutException:
            if count > 10:
                raise Exception('CAN NOT click logout_OK !!!')
            continue
        else:
            break
    button_logout_OK.click()
    wait_5.until(EC.number_of_windows_to_be(1))
    window = driver.window_handles[-1]
    driver.switch_to_window(window)
    driver.quit()

#========================[START]====================================
P = Print()
try: ###$ connect DMM
    profile = webdriver.FirefoxProfile(PROFILE)
    driver = webdriver.Firefox(firefox_profile=profile)
    wait = WebDriverWait(driver, 1)
    wait_5 = WebDriverWait(driver, 5)    
    wait_10 = WebDriverWait(driver, 10)
    wait_20 = WebDriverWait(driver, 20)
    wait_50 = WebDriverWait(driver, 50)
    wait_no_except = WebDriverWait(driver, 1, ignored_exceptions=True)
    wait_5_no_except = WebDriverWait(driver, 5, ignored_exceptions=True)    
    wait_10_no_except = WebDriverWait(driver, 10, ignored_exceptions=True)
    wait_20_no_except = WebDriverWait(driver, 20, ignored_exceptions=True)    
    #driver.implicitly_wait(10)

    P.print('connecting DMM...') 
    
    driver.get(LOGIN_URL)
    driver.find_element_by_id('accountId').send_keys(ID)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('LoginWindowBtn').click()

    wait_20.until(EC.number_of_windows_to_be(2))
    window = driver.window_handles[-1]
    driver.get('http://www.google.co.jp')
    driver.switch_to_window(window)
    # driver.maximize_window()

    elem_spread = wait_get_elem_xpath(wait_50, '//div[@uifield="spread"]')
    price_bid = wait_get_elems_xpath(wait_20, '//div[@uifield="bidStreamingButton"]/div/*')    
    price_ask = wait_get_elems_xpath(wait_20, '//div[@uifield="askStreamingButton"]/div/*')
    button_order_all = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonAll"]')
    button_order_bid = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonSell"]')
    button_order_ask = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonBuy"]')    
    button_bid = wait_get_elem_xpath(wait_20, '//div[@uifield="bidStreamingButton"]')
    button_ask = wait_get_elem_xpath(wait_20, '//div[@uifield="askStreamingButton"]')
    button_slippage = wait_get_elem_xpath(wait_20, '//span[@uifield="slippageButton"]')
    text_order_Lot = wait_get_elem_xpath(wait_20, '//input[@uifield="orderQuantity"]')
    button_logout = wait_get_elem_xpath(wait_20, '//div[@class="logout label"]')
    button_logout.click()
    button_logout_OK = wait_get_elem_xpath(wait_20, '//button[@uifield="okButton"]')
    button_logout_cancel = wait_get_elem_xpath(wait_20, '//button[@uifield="cancelButton"]')
    button_logout_cancel.click()
    notice_contract_err = wait_get_elem_xpath(wait_20, '//div[@uifield="errorArea"]')
    notice_contract_OK = wait_get_elem_xpath(wait_20, '//div[@class="logout label"]')
    info_PL_today = wait_get_elem_xpath(wait_20, '//span[@uifield="dailyPlTotalJPY"]')
except:
    P.print(C.R + C.BOLD + 'CAN NOT CONNECT DMM !!!')
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise
else:
    P.print('\033[A' + '\033[K' + '\033[A') # connecting DMM を消す


if re.match(r'.*disable.*', button_order_all.get_attribute('class')):
    pos = 0
else:
    logout_except()
    raise Exception(C.Y + C.BOLD + 'POSITION IS NOT 0')



try: ###$ ts fetch
    for i in range(3):
        text_order_Lot.send_keys(Keys.BACK_SPACE)
    text_order_Lot.send_keys(LOT)
    button_slippage.click()
    event = threading.Event()
    FF = FirstFetch(price_bid, itr_num=itr_num, event=event, sec=sec)
    FF.start()
    event.wait(timeout=(itr_num*sec+60.0))
    ts = FF.ts
    P.print(FF.ts)
except:
    P.print(C.R + C.BOLD + 'ERROR OCCURRED IN FirstFetch !!!')
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise
    

try: ###$ bid & ask
    
    F = Fetch(price_bid, ts=ts, event=event, sec=sec, itr_num=itr_num)
    F.start()

    loop_count = 0
    los_count = 0
    price_ordered = 0.0

############################################################
###########################################################

        # WebDriverWait(driver, timeout=X, ignored_exceptions=True)
        # EC.element_to_be_clickable()
        # :before ????
        # <div class="executedNotification label" uifield="executedNotification" style="display: none;">



    while True:
        
        loop_count += 1
        if loop_count > LOOP_MAX:
            break

        P.print('waiting...')
        event.wait()

        start = time.time()
        
        ts = F.ts
        spread = float(elem_spread.text) / 100.0 # pips 表示から円になおす
        S = ts.ewm(span=SPAN_S).mean().values[-1]
        # S = ts.ewm(span=SPAN_S).mean()[-1:].values[0]
        M = ts.ewm(span=SPAN_M).mean().values[-1]
        L = ts.ewm(span=SPAN_L).mean().values[-1]

        #ポジが0なら。。。
        if pos == 0:

           #買う？
            if S > M > L:
                P.print(str(loop_count) + ' ' + C.Y + 'S' + C.RESET + ': {0:6.3f}'.format(S, loop_count))
                
                while True:
                    if (time.time() - start) > sec_limit:
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price > S - spread:
                        continue
                    button_ask.click()
                    try:
                        wait.until(EC.visibility_of(notice_contract_OK))
                    except  selenium.common.exceptions.TimeoutException:
                        continue
                    else:
                        pos = 1
                        price_ordered = price
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.R + 'contract')
                        break
            #売る?
            elif S < M < L:
                P.print(str(loop_count) + ' ' + C.Y + 'S' + C.RESET + ': {0:6.3f}'.format(S, loop_count))                

                while True:
                    if (time.time() - start) > sec_limit:
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price < S + spread:
                        continue
                    button_bid.click()
                    try:
                        wait.until(EC.visibility_of(notice_contract_OK))
                    except  selenium.common.exceptions.TimeoutException:
                        continue
                    else:
                        pos = -1
                        price_ordered = price
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.B + 'contract')                        
                        break
            #そのまま?    
            else:
                P.print(str(loop_count) + ' ' + 'S' + C.RESET + ': {0:6.3f}'.format(S, loop_count))
                continue
           
        #1(long, 買)なら。。。
        if pos == 1:
            P.print(str(loop_count) + ' ' + C.R + 'S' + C.RESET + ': {0:6.3f}'.format(S, loop_count))
            #継続?
            if S > M:
                continue
            #決済する?
            else:
                while True:
                    if (time.time() - start) > sec_limit:
                        los_count += 1
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price < S + spread:
                        continue
                    button_order_all.click()
                    time.sleep(0.5)
                    if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                        continue
                    else:
                        pos = 0
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.R + 'ordered')
                        break
          
        #-１(short, 売)なら。。。
        if pos == -1:
            P.print(str(loop_count) + ' ' + C.B + 'S' + C.RESET + ': {0:6.3f}'.format(S, loop_count))
            #継続?
            if S < M:
                continue
            #決済する?
            else:
                while True:
                    if (time.time() - start) > sec_limit:
                        los_count += 1
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price > S - spread:
                        continue
                    button_order_all.click()
                    time.sleep(0.5)
                    if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                        continue
                    else:
                        pos = 0
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.B + 'ordered')                        
                        break
            
###########################################################
###########################################################
    
    F.cancel()
    del FF, F
except:
    P.print(C.R + C.BOLD + 'ERROR OCCURRED IN LOOP !!!')
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise


try: ###$ logout
    while True:
        button_order_all.click()
        time.sleep(1)
        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')):
            continue
        else:
            break
    while True:
        button_logout.click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@uifield="okButton"]')))
        except selenium.common.exceptions.TimeoutException:
            continue
        else:
            break
    button_logout_OK.click()
    wait_5.until(EC.number_of_windows_to_be(1))
    window = driver.window_handles[-1]
    driver.switch_to_window(window)
except:
    P.print(C.R + C.BOLD + 'CAN NOT LOGOUT !!!')
    logout_except()
    raise
else:
    P.print('logout complete.')

wait_5.until(EC.number_of_windows_to_be(1))
window = driver.window_handles[-1]
driver.switch_to_window(window)

try: ###$ driver.quit()
    driver.quit()
except:
    P.print(C.R + C.BOLD + 'CAN NOT DRIVER.QUIT() !!!')
    raise
else:
    P.print('driver.quit()')


