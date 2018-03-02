#/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import httplib
import md5
import urllib
import random

appid = '' 
secretKey = ''
httpClient = None
fromLang = 'zh'
toLang = 'en'

infos = [] # 待翻译
results = {}

def make_file(filename):
    num = 0
    with open(filename, 'w+') as f:
        for info in infos:
            myurl = '/api/trans/vip/translate'
            q = info.strip()
            salt = random.randint(32768, 65536)
            sign = appid+q+str(salt)+secretKey
            m1 = md5.new()
            m1.update(sign)
            sign = m1.hexdigest()
            myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
            try:
                httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
                httpClient.request('GET', myurl)
                response = httpClient.getresponse()
                result = json.loads(response.read())['trans_result'][0]['dst'].encode('utf-8')
                results["data"] = result
                line = json.dumps(results)
                f.write(line + '\n')
                num += 1
                if num % 1000 == 0:
                    print('success {}'.format(num))
            except Exception, e:
                print e
            finally:
                if httpClient:
                    httpClient.close()

if __name__ == "__main__":
    filename = 'trans.json'
    make_file(filename)
