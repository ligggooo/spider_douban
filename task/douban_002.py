#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   douban_002.py
@Time    :   2019/2/12 19:36
@Desc    :
'''


def login():
    import requests
    # 使用requests登陆豆瓣
    session = requests.session()
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    data = {
        'ck': '',
        'name': 'ligggooo@sina.com.cn',
        'password': 'liggg000',
        'remember': 'false',
        'ticket': '',
    }
    from service.headers import headers
    login_session = session.post(url=login_url, data=data, headers=headers)

    my_url = 'https://www.douban.com/people/83879163/'
    text = session.get(url=my_url, headers=headers).text

    # with open('./data.html','w',encoding='utf-8') as f:
    #     f.write(text)
    # 可以看到登陆成功了
    return session

import json
import os
def save(dir,name,object,type='html'):

    if not os.path.exists(dir):
        os.mkdir(dir)
    name = os.path.join(dir,name)
    try:
        with open(name,'w',encoding='utf-8') as f:
            if type=='json':
                f.write(json.dumps(object,indent='  '))
            else:
                f.write(object)
    except Exception as e:
        print(e)

from service.driver import browser
from lxml import etree
import time
def get_movies():
    movie_action_url = 'https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85%E7%89%87&type=11&interval_id=100:90&action=playable'

    browser.get(movie_action_url)
    time.sleep(5)
    js = 'window.scrollTo(0,2000);'
    browser.execute_script(js)
    time.sleep(5)
    text = browser.page_source
    save('./data', 'data.html', text, type='html')


    tree = etree.HTML(text)

    movies = tree.xpath('//div[contains(@class,"movie-content")]')
    movies_list = []
    for movie in movies:
        try:
            href = movie.xpath('./a/@href')[0]
            img = movie.xpath('.//img/@data-original')[0]
            movies_list.append({
                'url': href,
                'img': img
                })
        except:
            break
    save('./data', 'movies', movies_list, type='json')


if __name__ == '__main__':
    # session = login()
    # get_movies()
    movies = json.load(open('./data/movies'))
    for i,movie in enumerate(movies):
        '''
        海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分
        '''
        url = movie['url']
        # url = 'https://movie.douban.com/subject/1292063/'
        browser.get(url)
        time.sleep(1)
        content = browser.find_element_by_xpath('//div[@id="content"]')
        title = content.find_element_by_xpath('.//h1').text
        info = content.find_element_by_xpath('.//div[@id="info"]')
        # rows = info.find_elements_by_xpath('./span')
        mores = info.find_elements_by_xpath('.//a[starts-with(@class,"more")]')
        for more in mores:
            more.click()

        rating = browser.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong').text

        print(title)
        browser.save_screenshot('r%s.png'%i)
        info_dict={'title':title,'detail':info.text.split('\n'),'rating':rating}

        # while rows:
        #     row = rows.pop(0)
        #     try:
        #         key,content = row.find_elements_by_xpath('./span')
        #         info_dict[key.text] = content.text
        #     except:
        #         key = row.text
        #         content = rows.pop(0).text
        #         info_dict[key] = content
        movie['info'] = info_dict
        print(info_dict)
    save('./data', 'movies', movies, type='json')
