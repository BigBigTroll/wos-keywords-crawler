import datetime

from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

# 开始运行
# 这个搜索链接的页数无所谓,循环中会切除
search = 'https://www.webofscience.com/wos/alldb/summary/e15a75de-d79c-4692-9916-7a1d64ee4538-8fd4631f/relevance/1'

paper_num = 294
page_num = 6

# 打开一个
driver = webdriver.Firefox()
# driver.maximize_window()

# links_wos_list_index = []
links_wos_list = []
links_wos_text = []

# 计数 每页
for i in range(0, page_num):
    # 前一个tab
    window_before = driver.window_handles[0]

    link_of_pagination = search[0:-1] + str(i + 1)
    # Send GET request for the given http protocol (link)
    driver.execute_script("window.open('" + link_of_pagination + "', '_blank');")

    time.sleep(13)

    # 切换至新的tab
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    # 第一次打开wos点击cookie页
    if i == 0:
        time.sleep(5)
        # Find consent cookies by button ID
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        time.sleep(2)
        consent_button = driver.find_element(By.ID, value='onetrust-accept-btn-handler')
        consent_button.click()  # click on accept cookies
        # Find "Remind Later" cookie, if prompted, and click on "remind later"
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'pendo-button-f8b7283d')))
            remind_button = driver.find_element(By.ID, value='pendo-button-f8b7283d')
            remind_button.click()
        # If the cookie was not prompted, then just proceed
        except TimeoutException:
            pass

    # Loop through all papers in the current page (50 in total)
    for j in range(1, 51):
        try:
            # Find Div element containing the paper records
            paper_div = driver.find_element(By.XPATH,
                                            '/html/body/app-wos/main/div/div/div[2]/div/'
                                            'div/div[2]/app-input-route/app-base-summary-component/'
                                            'div/div[2]/app-records-list/app-record[{}]/div/div/div[2]/'
                                            'div[1]/app-summary-title/h3/a'.format(j))
            driver.execute_script("arguments[0].scrollIntoView(true);", paper_div)
            href_text = paper_div.get_attribute('text')
            href_value = paper_div.get_attribute('href')
            # Defining the XPATH for the button of the iterating paper
            links_wos_list.append(href_value)
            links_wos_text.append(href_text)
            print(href_value+'\t'+href_text)
        except NoSuchElementException:
            if (i * 50 + j) == (paper_num + 1):
                print("网址收录结束")
                break
            else:
                print('第' + str(i * 50 + j) + '没找到')
                continue
        time.sleep(random.uniform(1, 2))

    # 关闭标签页
    driver.close()
    # switch to parent window
    driver.switch_to.window(driver.window_handles[0])


print(11111)
