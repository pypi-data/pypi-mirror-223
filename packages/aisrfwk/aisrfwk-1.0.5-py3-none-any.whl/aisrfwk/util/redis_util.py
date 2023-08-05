#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-06 15:52:46
# @Author  : wangmian05
# @Link    : wangmian05@countrygraden.com.cn
# @Version : $Id$
import json
import time

from aisrfwk.redis.redis_core import re_pool, setHash, lPush
from aisrfwk.util.config import config
from aisrfwk.util import log as log
from aisrfwk.util.mail_util import sendMail

global_key = config.get("redis.global_key", "aisr-fwk")
aisr_queue_key = global_key + ":" + config.get("redis.task_queue", "task_queue")
aisr_task_status_key = global_key + ":" + config.get("redis.task_status", "task_status")
aisr_task_data_key = global_key + ":" + config.get("redis.task_data", "task_data")
aisr_send_mail_key = global_key + ":" + config.get("redis.send_mail", "send_mail")

task_status = {"todo": 1, "running": 2, "success": "3", "error": "4"}


def putTask(_task_id, content):
    data = {"status": task_status.get("todo"), "putTime": int(round(time.time() * 1000))}
    setHash(aisr_task_status_key, _task_id, json.dumps(data))
    setHash(aisr_task_data_key, _task_id, content)
    lPush(aisr_queue_key, content)


def startTask(_task_id):
    data = getTaskStatus(_task_id)
    if data is None:
        log.warning("[startTask]当前缓存中不存在此任务:{},放弃处理错误", data)
        return
    data["startTime"] = int(round(time.time() * 1000))
    data["startDate"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    re_pool.hset(aisr_task_status_key, _task_id, json.dumps(data))


def runningTask(_task_id):
    data = getTaskStatus(_task_id)
    if data is None:
        log.warning("[runningTask]当前缓存中不存在此任务:{},放弃处理错误", data)
        return
    data["status"] = task_status.get("running")
    data["runningTime"] = time.time()
    data["runningDate"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    re_pool.hset(aisr_task_status_key, _task_id, json.dumps(data))


def updateTaskStatus(_task_id, status):
    data = getTaskStatus(_task_id)
    if data is None:
        log.warning("[updateTaskStatus]当前缓存中不存在此任务:{},放弃处理错误", data)
        return
    data["status"] = status
    re_pool.hset(aisr_task_status_key, _task_id, json.dumps(data))


def getTaskStatus(_task_id):
    data = re_pool.hget(aisr_task_status_key, _task_id)
    if data is not None:
        return json.loads(data)
    else:
        return data


def restartTodoRunTask(_task_id=None):
    task_list_data = re_pool.hgetall(aisr_task_status_key)
    for tkd in task_list_data:
        key = bytes.decode(tkd)
        tk_val = json.loads(task_list_data[tkd])
        # log.info("当前key:{}结果:{}", key, tk_val)
        if _task_id is not None:
            if key == _task_id:
                h_data = re_pool.hget(aisr_task_data_key, _task_id)
                if h_data is not None and tk_val["status"] == task_status.get("todo"):
                    task_data_str = bytes.decode(h_data, "utf-8")
                    log.info("当前需要把任务:{}重新装回队列...", key)
                    lPush(aisr_queue_key, task_data_str)
        else:
            h_data = re_pool.hget(aisr_task_data_key, key)
            if h_data is not None and tk_val["status"] == task_status.get("todo"):
                task_data_str = bytes.decode(h_data, "utf-8")
                log.info("当前需要把任务:{}重新装回队列...", key)
                lPush(aisr_queue_key, task_data_str)

    return None


def overTaskStatus(_task_id):
    data = getTaskStatus(_task_id)
    if data is None:
        log.warning("[errorTaskStatus]当前缓存中不存在此任务:{},放弃处理错误", data)
        return
    # if data["status"] == task_status.get("error"):
    #     log.warning("[errorTaskStatus]任务执行过程中出现异常:{},暂时无需删除错误信息", data)
    #     return
    re_pool.hdel(aisr_task_status_key, _task_id)
    re_pool.hdel(aisr_task_data_key, _task_id)
    re_pool.delete(aisr_send_mail_key + _task_id)


def buildSendData(_task_id):
    _task_data = re_pool.hget(aisr_task_data_key, _task_id)
    _task_data_str = bytes.decode(_task_data, "utf-8")
    _pro_name = None
    _creator = None
    if _task_data is not None:
        json_data = json.loads(_task_data)
        # 项目名称
        _pro_name = json_data.get("projectName") if json_data.get("projectName") else None
        # 创建人
        _creator = json_data.get("creator") if json_data.get("creator") else None
    return _task_data_str, _pro_name, _creator


def errorTaskStatus(_task_id, _msg, send_mail=True):
    _status_data = getTaskStatus(_task_id)
    if _status_data is None:
        log.warning("[errorTaskStatus]当前缓存中不存在此任务:{},放弃处理错误", _status_data)
        return
    # 暂时打开所有错误都发送邮件功能
    # send_mail = _status_data["status"] == task_status.get("running")
    # 如果单个任务超过10个邮件就不再发了.发多了也没啥意义
    if incr(_task_id) > 10:
        send_mail = False
    _status_data["status"] = task_status.get("error")
    _status_data["errorTime"] = int(round(time.time() * 1000))
    _status_data["errorDate"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    _status_data["errorMsg"] = _msg
    re_pool.hset(aisr_task_status_key, _task_id, json.dumps(_status_data))
    # 发送邮件通知
    if send_mail:
        try:
            log.info("开始发送错误邮件...")
            _task_data_str, _pro_name, _creator = buildSendData(_task_id)
            sendMail(_msg, _task_data_str, _project_name=_pro_name, _creator=_creator)
        except Exception as e:
            log.error("邮件发送错误:{}", str(e))


def incr(taskId):
    return re_pool.incr(aisr_send_mail_key + taskId)


if __name__ == "__main__":
    queue_key = "aisr:park_task_queue"
    value = "{\"taskId\": \"1\"}"
    # data = json.loads(value)
    # for x in range(100):
    #     data["taskId"] = str(int(data["taskId"]) + int(x))
    #     value = json.dumps(data)
    #     # log.info("入队列key:" + queue_key + ",入队列value:" + value + str(x))
    #     lPush(queue_key, value)
    # msg = "TypeError: descriptor 'encode' for 'str' objects doesn't apply to a 'bytes' object"
    # taskId = "1131473191623214108672"
    # # task_data = re_pool.hget(aisr_task_data_key, taskId)
    # # task_data_str = bytes.decode(task_data, "utf-8")
    # errorTaskStatus(taskId, msg)
    # for x in range(1, 10):
    #     log.info("出队列内容:" + rPop(queue_key))
    # restartTodoRunTask("1301474280540101283840")
    # d = getHash("aisr:park_task_data","4271501943917891948544")
