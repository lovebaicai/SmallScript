#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline()

results = ['http://item.yunhou.com/10403000059.html', 'http://item.yunhou.com/10000000083.html']

for info in results:
    r.rpush('start_urls', ('{}').format(info))
