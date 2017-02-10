#!/usr/bin/python3
# highとlowの幅によって???
# openとcloseも使う???
# openとlow(high)の関係からトレンドを判断???
# pos_count の値によって損切りの挙動をコントロールする???
# Fetchにタイマーを設定する???
# mailを送るようにする???
# 買い(売り)待ちの時間が長いのはもったいない。特に急なトレンドの時。???
# http.client.CannotSendRequest: Request-sent をどうにかする!!!!!!!!!!!!!!!!!!!!!!!
# 下降トレンドのときに現在の値がSを越えたら買い、一定の利益が生まれたところで売る???



DEBUG = True
Lot = '1'
sec = 2.0 # fetchの間隔(秒)
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
itr_num = SPAN_L - 1 # FirstFetchの繰り返し回数
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
    
    pos = first_pos
    F.start()
    ########
    trend_kamo_pos_lim = 100 ####
    trend_pos_lim = 100 ####
    ########
    trend_kamo_count = 0
    trend_count = 0
    kamo_pos = False
    pos = False
    tts = None
    while True:
        start = time.time()
        ts = F.ts
        while True:
            time.sleep(0.01)
            #loop_start = time.time() ## 最大0.32ぐらいは確認できた。
            price = float_price(price_bid)
            tts = ts.append(pd.Series([price]), ignore_index=True)
            Ss = tts.rolling(SPAN_S).mean().values[-1]
            Ms = tts.rolling(SPAN_M).mean().values[-1]
            Ls = tts.rolling(SPAN_L).mean().values[-1]

            
            if Ss > Ls > Ms or Ss < Ls < Ms:
                trend_kamo_count += 1
                
                if kamo_pos:
                    pass
                else:
                    if Ss > Ls > Ms:
                        button = button_ask; color = C.R;
                    else:
                        button = button_bid; color = C.B;
                    if trend_kamo_count > trend_kamo_pos_lim:
                        button.click()
                        try:
                            wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                        except:
                            if DEBUG:
                                P.print('error contract!', file=2) ##
                            try:
                                if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                                    kamo_pos = True
                                    P.print('I try to contract. but you have ' + color + 'contracted!')
                            except:
                                P.print('error kamo_pos contract re.match!')
                        else:
                            kamo_pos = True
                            kamo_pos_pirce = 'foo'
                            P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'contract')

                            
            if Ss > Ms > Ls or Ss < Ms < Ls:
                trend_count += 1

                if pos:
                    pass
                else:
                    if Ss > Ms > Ls:
                        button = button_ask; color = C.R; test = 'price < Ss';
                    else:
                        button = button_bid; color = C.B; test = 'price > Ss';
                    if trend_count > trend_pos_lim:
                        if eval(test):
                            button.click()
                            try:
                                wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                            except:
                                if DEBUG:
                                    P.print('error contract!', file=2) ##
                                try:
                                    ### このままだとスキャルピングできない!!!!!!!!!!!!!!!!
                                    if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                                        pos = True
                                        P.print('I try to contract. but you have ' + color + 'contracted!')
                                except:
                                    P.print('error pos contract re.match!')
                            else:
                                pos = True
                                pos_price = 'hoge' ####
                                P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'contract')

                                
            if Ls > Ss > Ms or Ls < Ss < Ms:
                if trend_kamo_count > 0:
                    trend_kamo_count -= 1
                if trend_count > 0:
                    trend_count -= 1

                if not pos and (trend_kamo_count > trend_kamo_pos_lim or trend_count > trend_pos_lim):
                    pass

                else:
                    trend_kamo_count = trend_count = 0
                    if kamo_pos or pos:
                        if Ms > Ss > Ls:
                            color_order = C.B;
                        else:
                            color_order = C.R;
                        button_order_all.click()
                        try:
                            wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                        except:
                            if DEBUG:
                                P.print('error order!', file=2) ##
                            try:
                                if re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできないなら
                                    kamo_pos = pos = False
                                    P.print('I try to order. but you have ' + color_order + 'ordered!')
                            except:
                                P.print('error order re.match!')
                        else:
                            kamo_pos = False
                            pos = False
                            P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color_order + 'ordered') ###

            #print(time.time() - loop_start) ##

                        
            if time.time() - start > sec:
                break

            del tts[len(tts) - 1]
                    
        '''                    
        #ポジが0なら。。。
        if pos == 0:
           #買う？売る?
            if S > M > L or S < M < L:
                if S > M > L:
                    next_pos = 1; color = C.R; test = 'price > S - spread'; button = button_ask;
                elif S < M < L:
                    next_pos = 2; color = C.B; test = 'price < S + spread'; button = button_bid;                    
                P.print(str(count_loop) + ' ' + color + 'S' + C.RESET + ': {0:6.3f}'.format(S))
                while True:
                    if (time.time() - start) > sec_limit:
                        break
                    price = float_price(price_bid, DEBUG)
                    if eval(test):
                        continue
                    button.click()
                    try:
                        wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
                    except selenium.common.exceptions.TimeoutException:
                        if DEBUG:
                            P.print('error contract!', file=2) ##
                        continue
                    else:
                        pos = next_pos
                        price_contract = price
                        P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'contract')
                        break
            #そのまま?    
            else:
                P.print(str(count_loop) + ' ' + 'S' + C.RESET + ': {0:6.3f}'.format(S))
                continue
           
        #ポジションを持っているなら。。。
        elif pos in (1, 2):
            if pos == 1:
                color = C.R; color_order = C.B; test = 'S > M'; test2 = 'price < S + diff_order_spread'; elem_price_contract = price_ask_contract
            elif pos == 2:
                color = C.B; color_order = C.R; test = 'S < M'; test2 = 'price > S - diff_order_spread'; elem_price_contract = price_bid_contract
            P.print(str(count_loop) + ' ' + color + C.BOLD + 'S' + C.RESET + ': {0:6.3f}'.format(S)) ###
            #継続?
            if eval(test): ###
                continue
            #決済する?
            else:
                price = float_price(price_bid, DEBUG)
                price_open = price
                price_high = price
                price_low = price
                price_contract = float(elem_price_contract.text)
                while True:
                    # waitに間に合うようにチェック
                    if (time.time() - start) > sec_limit:
                        count_los += 1
                        break
                    # 損切り???
                    if count_los >= limit_count_los: ####
                        try:
                            main_loop_order(pos)
                        except OrderException:
                            break
                        else:
                            continue
                    # 急なトレンドによって損切りが発生したと仮定して、ポジションを反転させる
                    ####
                    price = float_price(price_bid, DEBUG)
                    # highとlowを更新
                    if price_high < price:
                        price_high = price
                    if price_low > price:
                        price_low = price
                    # orderするかチェック
                    if eval(test2): ###
                        continue
                    else:
                        try:
                            main_loop_order(pos)
                        except OrderException:
                            break
                        else:
                            continue
        else:
            raise Exception('pos == 3 ???')
        '''

def main_loop_order(pos):
    global button_order_all, DEBUG, D, count_los
    global wait_for_test
    
    if pos == 1:
        color_order = C.B
    elif pos == 2:
        color_order = C.R
    button_order_all.click()
    try:
        wait_for_test.until(EC.element_to_be_clickable((By.XPATH, '//span[@uifield="notification"]')))
    except selenium.common.exceptions.TimeoutException:
        if DEBUG:
            P.print('error order!', file=2) ##
    else:
        pos = 0
        count_los = 0
        P.print(datetime.datetime.now(D).strftime('%Y-%m-%d %H:%M:%S') + ' ' + color_order + 'ordered') ###
        raise OrderException

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
#import seaborn
#
from selenium_def import *
from selenium_class import *
import colors as C
#============================================================
def logout_except():
    count = 0
    while True:
        count += 1
        button_logout.click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@uifield="okButton"]')))
        except selenium.common.exceptions.TimeoutException:
            if count > 10:
                raise Exception('CAN NOT click button_logout !!! in logout_except()')
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
    logout_except()
    raise
else:
    P.print('\033[A' + '\033[K' + '\033[A', file='err') # connecting DMM を消す

    
# ログイン直後のポジションチェック
if re.match(r'.*disable.*', button_order_all.get_attribute('class')):
    pos = 0
elif not re.match(r'.*disable.*', button_order_ask.get_attribute('class')) and re.match(r'.*disable.*', button_order_bid.get_attribute('class')): # askだけクリック可
    pos = 1
elif not re.match(r'.*disable.*', button_order_bid.get_attribute('class')) and re.match(r'.*disable.*', button_order_ask.get_attribute('class')): # bidだけクリック可
    pos = 2
elif not re.match(r'.*disable.*', button_order_ask.get_attribute('class')) and not re.match(r'.*disable.*', button_order_bid.get_attribute('class')): # ask、bidの両方クリック可
    pos = 3
else:
    logout_except()
    raise Exception(C.Y + C.BOLD + 'CAN NOT DITECT POSITION')


P.print('first position: {0}'.format(pos_to_position(pos)))


# ロット、スリッページの設定
try:
    for i in range(3):
        text_order_Lot.send_keys(Keys.BACK_SPACE)
    text_order_Lot.send_keys(Lot)
    if ON_OFF_slippage:
        button_slippage.click()
except:
    P.print(C.R + 'CAN NOT SETTING DMM !!!', file='err')
    logout_except()
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


# メインループ
try:
    F = Fetch(price_bid, ts=ts, event=event, sec=sec, itr_num=itr_num, DEBUG=DEBUG)
    D = datetime.timezone(datetime.timedelta(hours=9))
###############################    
    main_loop(pos)
###############################
    F.cancel()
    del F
except:
    P.print(C.R + C.BOLD + 'ERROR OCCURRED IN LOOP !!!', file='err')
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise

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
    wait_5.until(EC.number_of_windows_to_be(1))
    window = driver.window_handles[-1]
    driver.switch_to_window(window)
except:
    P.print(C.R + C.BOLD + 'CAN NOT LOGOUT !!!', file='err')
    logout_except()
    raise
else:
    P.print('logout complete.', file='err')

wait_5.until(EC.number_of_windows_to_be(1))
window = driver.window_handles[-1]
driver.switch_to_window(window)

try: ###$ driver.quit()
    driver.quit()
except:
    P.print(C.R + C.BOLD + 'CAN NOT DRIVER.QUIT() !!!', file='err')
    raise
else:
    P.print('driver.quit()', file='err')


