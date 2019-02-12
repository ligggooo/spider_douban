#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   baidutranslation.py
@Time    :   2019/2/9 21:58
@Desc    :
'''
from  urllib import request,parse
from service.headers import headers
import json

# url = 'https://fanyi.baidu.com/v2transapi'
url = 'https://fanyi.baidu.com/sug'

data = {'kw': '西瓜'}
data = parse.urlencode(data).encode('ascii')

res = request.urlopen(url=url, data=data)
data_text = res.read()

print(json.loads(data_text.decode()))
