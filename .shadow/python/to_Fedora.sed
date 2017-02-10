    # profile = webdriver.FirefoxProfile(PROFILE)
    # driver = webdriver.Firefox(firefox_profile=profile)
    # wait = WebDriverWait(driver, 1)
    # wait_5 = WebDriverWait(driver, 5)    
    # wait_10 = WebDriverWait(driver, 10)
    # wait_20 = WebDriverWait(driver, 20)
    # wait_50 = WebDriverWait(driver, 50)
    # wait_no_except = WebDriverWait(driver, 1, ignored_exceptions=True)
    # wait_5_no_except = WebDriverWait(driver, 5, ignored_exceptions=True)    
    # wait_10_no_except = WebDriverWait(driver, 10, ignored_exceptions=True)
    # wait_20_no_except = WebDriverWait(driver, 20, ignored_exceptions=True)    
    # #driver.implicitly_wait(10)

    # P.print('connecting DMM...') 
    
    # driver.get(LOGIN_URL)
    # driver.find_element_by_id('accountId').send_keys(ID)
    # driver.find_element_by_id('password').send_keys(PASSWORD)
    # driver.find_element_by_id('LoginWindowBtn').click()

    # wait_20.until(EC.number_of_windows_to_be(2))
    # window = driver.window_handles[-1]
    # driver.get('http://www.google.co.jp')
    # driver.switch_to_window(window)
    # # driver.maximize_window()
    
/waiting.../d

s|elem_spread|wait_get_elem_xpath(wait_5, '//div[@uifield="spread"]')|
s|price_bid|wait_get_elems_xpath(wait_5, '//div[@uifield="bidStreamingButton"]/div/*')|    
s|price_ask|wait_get_elems_xpath(wait_5, '//div[@uifield="askStreamingButton"]/div/*')|
s|button_order_all|wait_get_elem_xpath(wait_5, '//button[@uifield="orderButtonAll"]')|
s|button_order_bid|wait_get_elem_xpath(wait_5, '//button[@uifield="orderButtonSell"]')|
s|button_order_ask|wait_get_elem_xpath(wait_5, '//button[@uifield="orderButtonBuy"]')|    
s|button_bid|wait_get_elem_xpath(wait_5, '//div[@uifield="bidStreamingButton"]')|
s|button_ask|wait_get_elem_xpath(wait_5, '//div[@uifield="askStreamingButton"]')|
s|button_slippage|wait_get_elem_xpath(wait_5, '//span[@uifield="slippageButton"]')|
s|text_order_Lot|wait_get_elem_xpath(wait_5, '//input[@uifield="orderQuantity"]')|
s|button_logout|wait_get_elem_xpath(wait_5, '//div[@class="logout label"]')|
s|button_logout_OK|wait_get_elem_xpath(wait_5, '//button[@uifield="okButton"]')|
s|button_logout_cancel|wait_get_elem_xpath(wait_5, '//button[@uifield="cancelButton"]')|
s|notice_contract_err|wait_get_elem_xpath(wait_5, '//div[@uifield="errorArea"]')|
s|notice_contract_OK|wait_get_elem_xpath(wait_5, '//div[@class="logout label"]')|
s|info_PL_today|wait_get_elem_xpath(wait_5, '//span[@uifield="dailyPlTotalJPY"]')|
