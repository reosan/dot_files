#!/usr/bin/python3
# 激せまスキャルピング
DEBUG = True
Lot = '1'
sec = 1.0 # fetchの間隔(秒)
wait_for_test_lim = 2.0
sec_limit = sec - 3*sec/60.0 ####
LOOP_MAX = 30 ##
ON_OFF_slippage = True # Trueならスリッページを0.1pipsに設定する
#--------- Ubuntu ---------
ID = 
PROFILE = '/home/reosan/.mozilla/firefox/i1zq2uyh.selenium'
#--------- Fedora ---------
# ID = 
# PROFILE = '/home/reosan/.mozilla/firefox/ygljf7v2.selenium'
#--------------------------
# ビギナー
LOGIN_URL = 'https://demotrade.fx.dmm.com/fxcrichpresen/webrich/direct/login'
# シニア
# LOGIN_URL = 'https://demotrade.fx.dmm.com/fxcmdipresen/webrich/direct/login'
PASSWORD = 
MAIL_ADDRESS = ''

# EWMAのスパン
SPAN_S = 2
SPAN_M= SPAN_S + 4
SPAN_L = SPAN_S + 8
SPAN_LL = 30
itr_num = 25 - 1 # FirstFetchの繰り返し回数
#
limit_count_los = 1 ####
spread = 0.003 ####
diff_order_spread = spread
count_loop = 0
count_los = 0
limit_count_los = limit_count_los
sleep_order_loop = 0.1
#
ts = None

price_contract = 0.0
price_order = 0.0
price_open = 0.0
price_high = 0.0
price_low = 0.0
price_close = 0.0
#
n = 0
foo = 0
#============================================================
def main_loop(first_pos):
    global ts, event, sec, itr_num, limit_count_los, driver, F, DEBUG, D
    global spread, diff_order_spread, limit_count_los
    global price_open, price_high, price_low, price_close
    global price_contract, price_order
    global count_los, count_loop, wait_for_test
    global info_ask_avg_pips, info_bid_avg_pips
    
    pos = first_pos
    F.start()
    ########
    mini_elap_time_lim = 0.1 ####
    ########
    elap_time = 0.0
    mini_elap_time = 0.0
    contract = 0.0
    pips = 0.0


    pre_Close = F.ts.values[-2] # bug? #
    state = 0
    pos = False
    while True:
        loop_start = time.time()
        diff_time = loop_start - F.time
        if diff_time < 0.0:
            time.sleep(abs(diff_time))
            diff_time = 0.0
        print('diff_time:{0}, pos:{1}, state:{2}'.format(diff_time, pos, state)) ## debug ##
        ts = F.ts
        pre_Open = pre_Close
        pre_Close = Open = High = Low = ts.values[-1]
        sma13 = ts.rolling(13).mean().values
        sma21 = ts.rolling(21).mean().values

        if pos:
            if state == -1:
                if eval('pre_Close' + test + 'ema13[-1]'):
                    state = -3
                elif eval('pre_Close' + test2 + 'ema21[-1]'):
                    state = -3

            # if state == -2:
            #     pass

            if state == -3:
                if eval('pre_Close' + test2 + 'sma13[-1]'):
                    # 決済
                    button_order_all.click()
                    try:
                        wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                    except:
                        if DEBUG:
                            P.print('error order!', file=2) ##
                        try:
                            if re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできないなら
                                pos = False
                                state = -5 #### param ####
                                P.print('I try to order. but you have ordered!')
                        except:
                            P.print('error order re.match!')
                    else:
                        pos = False
                        state = -5 #### param ####
                        P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + 'ordered') ###
                    

        else:
            if state < 0:
                state += 1

            elif state == 0:
                if pre_Close > sma13[-1] > sma21[-1]: # long
                    state = 1; button = button_order_ask; test = '>'; test2 = '<'; color = C.R; info = info_ask_avg_price;
                elif pre_Close < sma13[-1] < sma21[-1]: # short
                    state = 1; button = button_order_bid; test = '<'; test2 = '>'; color = C.B; info = info_bid_avg_price;
                else:
                    pass

            if state in (1, 2):
                for sma in (sma13, sma21):
                    for i in range(1,5): ####
                        if eval('sma[-i]' + test + 'sma[-i-1]'):
                            state *= 1
                        else:
                            state = 0
                            break

            if state == 1:
                if eval('sma13[-1]' + test + 'pre_Close' + test + 'sma21[-1]'):
                    if eval('pre_Open' + test + 'pre_Close'):
                        state = 2

            elif state == 2:
                if eval('sma21[-1]' + test + 'pre_Open or sma21[-1]' + test + 'pre_Close'):
                    state = 0

                    
        while True:
            mini_loop_start = time.time()
            price = float_price(price_bid)
            if High < price:
                High = price
            if Low > price:
                Low = price

            if pos:
                if state == -3:
                    button_order_all.click()
                    try:
                        wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                    except:
                        if DEBUG:
                            P.print('error order!', file=2) ##
                        try:
                            if re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできないなら
                                pos = False
                                state = -5 ####
                                P.print('I try to order. but you have ordered!')
                        except:
                            P.print('error order re.match!')
                    else:
                        pos = False
                        state = -5 ####
                        P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + 'ordered') ###

            
            
            elif state == 2:
                if eval('price' + test + 'sma13[-1]'):
                    # 注文
                    button.click()
                    try:
                        wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                    except:
                        if DEBUG:
                            P.print('error contract!', file=2) ##
                        try:
                            if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                                pos = True
                                state = -1
                                contract = float_pips(info)
                                P.print('I try to contract. but you have ' + color + 'contracted!')
                        except:
                            P.print('error pos contract re.match!')
                    else:
                        pos = True
                        state = -1
                        contract = float_pips(info)                        
                        P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'contract')                    

            mini_elap_time = time.time() - mini_loop_start
            if mini_elap_time < mini_elap_time_lim:
                time.sleep(mini_elap_time_lim - mini_elap_time)

            elap_time = time.time() - loop_start
            if elap_time > sec - diff_time:
                break



                
            # if pos:
            #     if ask_or_bid == 1:
            #         pips = float_pips(info_ask_avg_pips)
            #     elif ask_or_bid == 2:
            #         pips = float_pips(info_bid_avg_pips)
            #     else:
            #         pos = False

            #     if pips == 0.0:
            #         count_zero += 1
            #         if count_zero > 100:
            #             pos = False
            #             count_zero = 0

            #     if pips > P_pips_lim or pips < L_pips_lim:
            #             button_order_all.click()
            #             try:
            #                 wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
            #             except:
            #                 if DEBUG:
            #                     P.print('error order!', file=2) ##
            #                 try:
            #                     if re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできないなら
            #                         kamo_pos = pos = False
            #                         P.print('I try to order. but you have ordered!')
            #                 except:
            #                     P.print('error order re.match!')
            #             else:
            #                 kamo_pos = False
            #                 pos = False
            #                 P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + 'ordered') ###
                    
                    

                    
            # elif not pos:                            
            #     if Ss > Ms > Ls or Ss < Ms < Ls:
            #         if Ss > Ms > Ls:
            #             button = button_ask; color = C.R; test = 'price < Ss'; a_o_b = 1;
            #         else:
            #             button = button_bid; color = C.B; test = 'price > Ss'; a_o_b = 2;
            #         if eval(test):
            #             button.click()
            #             try:
            #                 wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
            #             except:
            #                 if DEBUG:
            #                     P.print('error contract!', file=2) ##
            #                 try:
            #                     if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
            #                         pos = True
            #                         ask_or_bid = 0
            #                         P.print('I try to contract. but you have ' + color + 'contracted!')
            #                 except:
            #                     P.print('error pos contract re.match!')
            #             else:
            #                 pos = True
            #                 ask_or_bid = a_o_b
            #                 P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'contract')
                            
            # elap_time = time.time() - loop_start
            # if elap_time < elap_time_lim:
            #     time.sleep(elap_time_lim - elap_time)

                        
            # if time.time() - start > sec:
            #     break

            # del tts[len(tts) - 1]

#============================================================
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#
import numpy as np
import pandas as pd
import math
import sys
import time
import threading
import re
import datetime
import traceback
#
from selenium_def import *
from selenium_class import *
import colors as C
#============================================================
def logout():
    count = 0
    while True:
        count += 1
        button_logout.click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@uifield="okButton"]')))
        except selenium.common.exceptions.TimeoutException:
            if count > 10:
                raise Exception('CAN NOT click button_logout !!! in logout()')
            continue
        else:
            break
    button_logout_OK.click()
#========================[START]====================================
P = Print()
# DMMへのログイン処理
try:
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

    wait_for_test = WebDriverWait(driver, wait_for_test_lim, poll_frequency=sec_limit/10.0)    
    #
    P.print('connecting DMM...', file='err') 
    #
    driver.get(LOGIN_URL)
    driver.find_element_by_id('accountId').send_keys(ID)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('LoginWindowBtn').click()
    #
    wait_20.until(EC.number_of_windows_to_be(2))
    window = driver.window_handles[-1]
    driver.close()
    driver.switch_to_window(window)
    #
    wait_get_elem_xpath(wait_50, '//div[@uifield="spread"]') ##
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
    info_bid_avg_price = wait_get_elem_xpath(wait_20, '//span[@uifield="bidAvgExecutionPrice"]')
    info_ask_avg_price = wait_get_elem_xpath(wait_20, '//span[@uifield="askAvgExecutionPrice"]')
    info_bid_avg_pips = wait_get_elem_xpath(wait_20, '//span[@uifield="bidEvaluationPips"]')
    info_ask_avg_pips = wait_get_elem_xpath(wait_20, '//span[@uifield="askEvaluationPips"]')    
except:
    P.print(C.R + C.BOLD + 'CAN NOT CONNECT DMM !!!', file='err')
    try:
        logout()
    except:
        driver.quit()
        raise
    raise
else:
    P.print('\033[A' + '\033[K' + '\033[A', file='err') # connecting DMM を消す

    
# ログイン直後のポジションチェック
if re.match(r'.*disable.*', button_order_all.get_attribute('class')):
    pos = False
else:
    pos = True


P.print('first position: {0}'.format(pos))


# ロット、スリッページの設定
try:
    for i in range(3):
        text_order_Lot.send_keys(Keys.BACK_SPACE)
    text_order_Lot.send_keys(Lot)
    if ON_OFF_slippage:
        button_slippage.click()
except:
    P.print(C.R + 'CAN NOT SETTING DMM !!!', file='err')
    logout()
    raise


# FirstFetch
ts = pd.Series([])
event = threading.Event()
FF = FirstFetch(price_bid, ts=ts, itr_num=itr_num, event=event, sec=sec, DEBUG=DEBUG)
while True:
    try:
        event.clear() #
        FF.start()
        event.wait(timeout=(itr_num*sec+60.0))
    except:
        P.print(C.R + C.BOLD + 'ERROR OCCURRED IN FirstFetch !!!', file='err')
        ts = FF.ts
        traceback.print_exc()
    else:
        P.print(FF.ts)
        break

    
ts = FF.ts    
del FF


D = datetime.timezone(datetime.timedelta(hours=9))


# メインループ
while True:
    try:
        F = Fetch(price_bid, ts=ts, event=event, sec=sec, itr_num=itr_num, DEBUG=DEBUG)
    ###############################    
        main_loop(pos)
    ###############################
        F.cancel()
        del F
    except KeyboardInterrupt:
        P.print(C.R + C.BOLD + 'KEYBOARD INTERRUPT !!!', file='err')
        F.cancel()
        del F
        logout()
        raise
    except:
        P.print(C.R + C.BOLD + 'ERROR OCCURRED IN MAIN LOOP !!!', file='err')
        ts = F.ts
        traceback.print_exc()
        error_time = time.time() - F.time
        time.sleep(sec - error_time)        


# ログアウト処理
try:
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
except:
    P.print(C.R + C.BOLD + 'CAN NOT LOGOUT !!!', file='err')
    logout()
    raise
else:
    P.print('logout complete.', file='err')

    
# driver.quit()
try: 
    driver.quit()
except:
    P.print(C.R + C.BOLD + 'CAN NOT DRIVER.QUIT() !!!', file='err')
    raise
else:
    P.print('driver.quit()', file='err')


