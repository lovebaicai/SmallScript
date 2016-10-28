#!/usr/bin/env python
#-*-coding:utf-8-*-

import scrapy
import json
from lagou.items import LagouItem
from scrapy import FormRequest


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = [
        'http://www.lagou.com/zhaopin/'
    ]

    joburl = 'http://www.lagou.com/jobs/positionAjax.json?'

    def start_requests(self):
        post_data = {'first': 'true', 'kd': 'python', 'pn': '1', 'city': u'上海'}
        #self.city = u'上海'
        # self.kd = 'python'
        # self.pn  = '1'
        return [FormRequest(url=self.joburl,
                            formdata=post_data, callback=self.parse)]
    
    
    def parse(self, response):
        pagecode = json.loads(response.body)['content']['positionResult']['result']
        item = LagouItem()
    #    self.totalPageCount = json.loads(response)['content']['positionResult']['totalCount'] /15 + 1
        for job in pagecode:
            item['jobname'] = job['positionName']
            item['releasetime'] = job['createTime']
            item['salary'] = job['salary']
            item['companyname'] = job['companyFullName']
            item['experience'] = job['workYear']
            item['Education'] = job['education']
            yield item
