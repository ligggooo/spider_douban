#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   douban_main.py
@Time    :   2019/2/12 19:36
@Desc    :
'''
from service.driver import browser
from service.headers import headers
from service import settings
from lxml import etree
from urllib import parse
import time
import requests
import json
import os


def login():
    # 使用requests登陆豆瓣，账户和密码都在settings中配置
    login_session = requests.session()
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    data = {
        'ck': '',
        'name': settings.USER['name'],
        'password': settings.USER['password'],
        'remember': 'false',
        'ticket': '',
    }

    login_res = login_session.post(url=login_url, data=data, headers=headers).text
    if json.loads(login_res).get('status') == 'success':
        print('登陆成功',login_res)

        # 下面的代码用于测试登陆成功与否
        # my_url = 'https://www.douban.com/people/83879163/'

        # text = login_session.get(url=my_url, headers=headers).text

        # with open('./data.html','w',encoding='utf-8') as f:
        #     f.write(text)
        # 可以看到登陆成功了
        return login_session
    else:
        return None


def save(data_dir, name, target, target_type='html'):
    '''
    保存文件到一个指定的文件夹下
    :param data_dir:  目标文件夹
    :param name:  目标文件名
    :param target:  保存对象
    :param target_type:  json和html两种对象的保存方式不同
    :return:
    '''
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    name = os.path.join(data_dir, name)
    try:
        with open(name, 'w', encoding='utf-8') as f:
            if target_type == 'json':
                f.write(json.dumps(target, indent='  '))
            else:
                f.write(target)
    except Exception as e:
        print(e)


def get_movies(movie_list_url, file_out, movie_type):
    file_out = movie_type + '_' + file_out
    # 获取排行榜内容
    print('获取%s分类下的电影列表...')
    browser.get(movie_list_url)
    time.sleep(5)
    # 下滚2000px
    js = 'window.scrollTo(0,2000);'
    browser.execute_script(js)
    time.sleep(5)
    text = browser.page_source
    save(settings.DATA_DIR, 'movie_list_page.html', text, target_type='html')

    tree = etree.HTML(text)

    movies = tree.xpath('//div[contains(@class,"movie-content")]')
    movies_list = []
    for movie in movies:
        try:
            href = movie.xpath('./a/@href')[0]
            img = movie.xpath('.//img/@data-original')[0]
            print('完成', href, img)
            movies_list.append({
                'url': href,
                'img': img
            })
        except:
            break
    save(settings.DATA_DIR, file_out, movies_list, target_type='json')
    print('完成电影url列表的获取,一共%s部电影' % len(movies_list))


def get_movie_info(file_in, file_out, movie_type=None):
    # 给输入输出文件加上前缀
    if movie_type:
        file_in = os.path.join(settings.DATA_DIR, movie_type + '_' + file_in)
        file_out = movie_type + '_' + file_out
    else:
        file_in = os.path.join(settings.DATA_DIR, file_in)
    movies = json.load(open(file_in))
    L = len(movies)
    for i, movie in enumerate(movies):
        '''
        海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分
        '''
        url = movie['url']
        # url = 'https://movie.douban.com/subject/1292063/' # 测试用
        browser.get(url)
        # 获取详情页
        time.sleep(1)
        # 获取详情信息 电影名称、导演、编剧、主演，类型，语言，上映日期，片长
        content = browser.find_element_by_xpath('//div[@id="content"]')
        title = content.find_element_by_xpath('.//h1').text
        info = content.find_element_by_xpath('.//div[@id="info"]')

        # 有些字段没有展开，点击这个字段后面的“更多”标签
        mores = info.find_elements_by_xpath('.//a[starts-with(@class,"more")]')
        for more in mores:
            more.click()
        # 获取评分
        rating = browser.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong').text

        print(title, '已经完成%s/共%s部' % (i + 1, L))
        browser.save_screenshot(os.path.join(settings.SCREEN_SHOT_DIR, 'r%s.png' % i))
        info_dict = {'title': title, 'detail': info.text.split('\n'), 'rating': rating}

        movie['info'] = info_dict
        print(info_dict)
    save(settings.DATA_DIR, file_out, movies, target_type='json')
    print('完成电影详情的获取')


def get_type():
    url = 'https://movie.douban.com/chart'
    # 豆瓣电影首页
    browser.get(url)
    print('获取豆瓣电影首页')
    time.sleep(2)
    # 定位分类列表下的标签
    type_list = browser.find_elements_by_xpath('//*[@id="content"]/div/div[@class="aside"]/div/div[@class="types"]//a')
    # 提取a标签的text和href位置
    url_list = [(item.get_attribute('href'), item.text) for item in type_list]
    # 疏忽选择列表
    for i, (_, _movie_type) in enumerate(url_list):
        print(i, _movie_type)
    # 接受用户输入
    while 1:
        try:
            url_index = int(input('请输入序号:').strip())
            return url_list[url_index]
        except:
            continue


if __name__ == '__main__':
    # 登陆
    session = login()
    # 获取电影类型 和 该类型的url
    movie_type_url, movie_type = get_type()
    # 获取该类型下的电影列表
    get_movies(movie_list_url=movie_type_url, file_out='movies_lv0', movie_type=movie_type)
    # 依次进入列表电影的详情页，抓取关键信息
    get_movie_info(file_in='movies_lv0', file_out='movies_lv1', movie_type=movie_type)
