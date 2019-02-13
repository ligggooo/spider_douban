#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   proxy.py
@Time    :   2019/2/12 18:01
@Desc    :   准备代理ip池
'''
import random


class Proxy:
    def __init__(self):
        self.proxy_pool =[]

    def pick_one(self):
        if self.is_empty:
            self.update()
        if self.is_empty:
            return None
        return random.choice(self.proxy_pool)

    def update(self):
        self.proxy_pool = steal_proxies()

    @property
    def is_empty(self):
        return len(self.proxy_pool) == 0

from lxml import etree
import requests



def steal_proxies_old():
    ## 这个网站对页面元素做了混淆处理，除了插入不可见元素外，还对端口号加了密

    # url = 'http://www.goubanjia.com/'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    # }
    # data_html = requests.get(url=url,headers=headers).text
    with open('data.html','r',encoding='utf-8') as f:
        # f.write(data_html)
        data_html = f.read()
    tree = etree.HTML(data_html)
    # //*[@id="services"]/div/div[2]/div/div/div/table/tbody/tr
    ele_proxy_list = tree.xpath('//*[@id="services"]/div/div[2]/div/div/div/table/tbody/tr')
    for ele in ele_proxy_list:
        # print(ele.xpath('./td[1]//text()'))
        ip_port = ''.join(ele.xpath('./td[1]//*[not(contains(@style,"none"))]//text()'))
        print(ip_port)

def steal_proxies():
    proxy_list = []
    from service.driver import browser

    url = 'http://www.goubanjia.com/'
    browser.get(url)
    # js = 'document.getElementBy(“test”).scrollIntoView();'

    browser.maximize_window()
    js = 'window.scrollTo(0,1300)'
    browser.execute_script(js)
    # browser.save_screenshot('hah.png')
    ele_proxy_list = browser.find_elements_by_xpath('//*[@id="services"]/div/div[2]/div/div/div/table/tbody/tr/td[1]')
    for ele in ele_proxy_list:
        # print(ele.xpath('./td[1]//text()'))
        ip_port = ele.text
        # print(ip_port)
        proxy_list.append(ip_port)
    return proxy_list

proxy_pool = Proxy()

# 测试

if __name__ == '__main__':
    proxy = Proxy()
    print(proxy.pick_one())
    print(proxy.pick_one())
    print(proxy.pick_one())
    # steal_proxies()



