#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   driver.py
@Time    :   2019/2/12 20:14
@Desc    :   生成浏览器对象
'''
from  selenium import webdriver
from selenium.webdriver.chrome.options import Options
from service.settings import CHROME_PATH


_chrome_options = Options()
_chrome_options.add_argument('--headless')
_chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=_chrome_options)
# browser_with_head = webdriver.Chrome(executable_path=CHROME_PATH)
