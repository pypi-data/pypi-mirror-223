#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : app
# @Time         : 2023/8/4 11:15
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/weixin_43354181/article/details/126753700


from meutils.pipe import *
from celery import Celery, shared_task

app = Celery(
    'MeutilsCelery',
    broker=os.getenv('REDIS_URL', 'redis://127.0.0.1:6379'),
    backend=os.getenv('REDIS_URL', 'redis://127.0.0.1:6379'),
)


@app.task(autoretry_for=(Exception,), default_retry_delay=10, retry_kwargs={'max_retries': 5})
def proxy_task(method, url, **kwargs):
    """request"""
    response = requests.request(method, url, **kwargs).json()
    return response


@shared_task(autoretry_for=(Exception,), default_retry_delay=10, retry_kwargs={'max_retries': 5})
def proxy_task_(method, url, **kwargs):
    """request"""
    response = requests.request(method, url, **kwargs).json()
    return response
