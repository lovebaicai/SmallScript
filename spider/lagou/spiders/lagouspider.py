#!/usr/bin/env python

import scrapy
import json
from scrapy.item import Item


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = [
    'http://www.lagou.com/jobs/positionAjax.json?px=new&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    ]

    def start_requests(self):
        post_data = {'first':'true','kd':'python','pn':'1'}
        # 查询特定关键词的内容，通过request
        return [scrapy.http.FormRequest(self.myurl,
                            formdata=post_data, callback=self.parse)]
    
    
    def parse(self, response):
        pagecode = json.loads(response)['content']['positionResult']['result']
        item = Item() 
        self.totalPageCount = json.loads(response)['content']['positionResult']['totalCount'] /15 + 1;
        for job in pagecode:
            item['jobname'] = job['positionName']
            item['releasetime'] = job['createTime']
            item['salary'] = job['salary']
            item['companyname'] = job['companyFullName']
            item['experience'] = job['workYear']
            item['Education'] = job['education']
            yield item
