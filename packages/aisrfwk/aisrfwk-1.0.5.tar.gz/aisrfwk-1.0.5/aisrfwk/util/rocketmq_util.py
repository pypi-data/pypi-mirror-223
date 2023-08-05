#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-14 16:30:50
# @Author  : wangmian05 (wangmian05@countrygraden.com.cn)
# @Link    : https://git.bgy.com.cn/bu00439/aisr-carbarn-ai.git
# @Version : $Id$
import json

from aisrfwk.rocketmq.rocketmq_core import sendMsg
from aisrfwk.util.config import config
from aisrfwk.util import log as log

system_name = config.get("system.name")

aisr_result_plan = config.get("mq.topic")

result_status = {"success": 0, "error": 1}


def sendErrorToServer(task_id, msg):
    """
    推送任务执行失败到mq
    """
    result_topic = aisr_result_plan
    msg = {
        "taskId": task_id,
        "status": result_status.get("error"),
        "msg": msg
    }
    sendMsg(result_topic, json.dumps(msg))
    log.info("[rocketmq]{}方案出错,错误消息发送成功...", system_name)


def sendResultToServer(content={}):
    """
    推送任务执行成功,附带结果数据到mq
    """
    result_topic = aisr_result_plan
    # 推入mq的数据.java端只取非坐标类的数据.坐标类的数据通过redis获取
    content["status"] = result_status.get("success")
    content["lastPlan"] = False
    sendMsg(result_topic, json.dumps(content))
    log.info("[rocketmq]{}方案数据消息发送成功...", system_name)


def sendTaskOverToServer(content={}, status="success"):
    """
    发送方案生成结束的标志消息去的到后端
    """
    result_topic = aisr_result_plan
    content["status"] = result_status.get("error") if status != "success" else result_status.get("success")
    content["lastPlan"] = True
    sendMsg(result_topic, json.dumps(content))

    log.info("[rocketmq]{}方案生成结束消息发送成功,内容:{}...", system_name, json.dumps(content))
