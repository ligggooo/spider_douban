#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   selenium001.py
@Time    :   2019/2/11 17:22
@Desc    :
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time

# 创建一个参数对象，用来控制chrome以无界面模式打开
chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# 驱动路径
path = r'F:\luffycity\课件\第7模块课件\chromedriver_win32\chromedriver.exe'

# 创建浏览器对象
browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

# 上网
url = 'http://python.jobbole.com/86415/'
browser.get(url)
imgs = browser.find_elements_by_tag_name('img')
import os
import requests
data_dir = 'douban_data_film'
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

js = 'window.scrollTo(0,document.body.clientHeight)'
browser.execute_script(js)
browser.save_screenshot('p1.png')
# js = 'window.scrollTo(0,document.body.clientHeight*2)'
browser.execute_script(js)
browser.save_screenshot('p2.png')


for img in imgs:
    img_url = img.get_attribute('src')
    img_name = img_url.split('/')[-1]
    with open(data_dir+'/'+img_name,'wb') as f:
        f.write(requests.get(img_url).content)
    print('done %s'%img_name)
    time.sleep(1)



