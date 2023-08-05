#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-07 17:07:08
# @Author  : wangmian05
# @Link    : wangmian05@countrygraden.com.cn
# @Version : $Id$
import json
import multiprocessing
import sys
import threading
import time

from aisrfwk.domain.base_aisr_task import BaseAisrTask
from aisrfwk.redis import redis_core
from aisrfwk.util import log, redis_util
from aisrfwk.util.config import config
from aisrfwk.util.exception_util import formatException, BaseAisrException
from aisrfwk.util.proces_util import pool

exec_count = 0
count_lock = multiprocessing.Lock()

system_name = config.get("system.name")


def __runningTask(content, model):
    """
    任务执行器
    """
    data = None
    try:
        try:
            data = json.loads(content)
            task_id = data.get("taskId")
            log.info("consumer start task:{}...", task_id)
            redis_util.runningTask(task_id)
            if model:
                model.run(data)
            else:
                BaseAisrTask().run(data)
            redis_util.overTaskStatus(task_id)
            log.info("consumer task over success:{}...", task_id)
        except BaseAisrException as bae:
            log.error("【严重】{}任务处理失败,业务异常{}:", system_name, sys.exc_info())
            task_id = data.get("taskId")
            _exc_text = "【严重】" + system_name + "任务处理失败,业务自定义异常:<br />" + formatException(sys.exc_info())
            redis_util.errorTaskStatus(task_id, _exc_text)
        except BaseException as e1:
            log.error("【严重】{}任务处理失败,未知异常{}:", system_name, sys.exc_info())
            task_id = data.get("taskId")
            _exc_text = "【严重】" + system_name + "任务处理失败,发生未知异常:<br />" + formatException(sys.exc_info())
            redis_util.errorTaskStatus(task_id, _exc_text)
            # rocketmq_util.sendErrorToServer(task_id, "【严重】车位排布任务处理过程中发生严重错误")
    except BaseException as e:
        log.error("【超级严重】当前进程发生错误,导致任务不执行,请检查任务状态:{}", sys.exc_info())


def __handleTask(content, model):
    """
    任务分发器
    """
    task_id = None
    data = None
    try:
        data = json.loads(content)
        task_id = data.get("taskId")
        log.info("consume queue task:{} running...", task_id)
        redis_util.startTask(task_id)
        pool.asyncProcess(__runningTask, content, model)
    except:
        log.error("{} queue error.redis队列数据读取解析失败:{}", system_name, sys.exc_info())
        if task_id is not None:
            _exc_text = "【严重】" + system_name
            "队列发生严重异常,redis队列数据读取解析失败:<br />" + formatException(sys.exc_info())
            redis_util.errorTaskStatus(task_id, _exc_text)
            redis_util.overTaskStatus(task_id)
            project_id = data.get("projectId") if data is not None else 0
            # rocketmq_util.sendErrorToServer(task_id, project_id, "【严重】车位排布任务进程池处理过程发生严重异常")


def __listener_task(model):
    """
    任务监听器
    """
    log.info("queue consumer start...", )
    while True:
        try:
            log.debug("queue consumer start...", )
            content = redis_core.bRpop(redis_util.aisr_queue_key)
            if content is None:
                continue
            global exec_count
            count_lock.acquire()
            exec_count += 1
            count_lock.release()
            log.info("listener start,todo:[{}] task", exec_count)
            __handleTask(content, model)
        except:
            log.debug("this rpop throw exception,retry rpop:{}", sys.exc_info())
            time.sleep(5)
            continue
        # 所有任务队列的时候都需要停顿500毫秒.给其他机器一点机会
        time.sleep(0.5)


# 线程启动方法
def start(__model=None):
    # 此处单独开一个线程监听队列任务.不能使用进程的方式,否则会导致mq发送消息是出现发送失败
    threading.Thread(target=__listener_task, args=[__model]).start()


if __name__ == "__main__":
    start()
