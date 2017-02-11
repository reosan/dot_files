from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import math
import sys
import time
import threading
#import seaborn

import colors as C

def wait_get_elem_xpath(wait, xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_get_elems_xpath(wait, xpath):
    return wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

def float_price(price):
    f = ret = 0.0
    while True:
        try:
            f = price[0].text + price[1].text + price[2].text
            ret =  float(f)
        except:
            print(C.K + 'error float_price!' + C.RESET) ##
            continue
        else:
            return ret

def print_price(price, label="", color=""):
    print( '\033[1;' + color + 'm' + label + '\033[0m' + ':' + str(float_price(price)) )

def fetch(price):
    timer_fetch = threading.Timer(0.5, fetch, [price])
    timer_fetch.start()
    foo = float_price(price)
    print(foo)


def print_raise():
    print(sys.exc_info()[2])
    print(sys.exc_info()[1])
    print(sys.exc_info()[0])

def pos_to_position(pos):
    if pos == 0:
        return 'flat'
    elif pos == 1:
        return C.R + 'long' + C.RESET
    elif pos == 2:
        return C.B + 'short' + C.RESET
    elif pos == 3:
        return C.R + 'cr' + C.RESET + 'o' + C.B + 'ss' + C.RESET
    else:
        raise Exception('POSITION ERROR')
    

    
    
    
