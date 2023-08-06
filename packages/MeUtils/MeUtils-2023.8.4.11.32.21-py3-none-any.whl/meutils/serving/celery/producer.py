#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : producer
# @Time         : 2023/8/4 11:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.serving.celery.app import proxy_task, proxy_task_



proxy_task.delay(1,2)
proxy_task_.delay(1,2)
