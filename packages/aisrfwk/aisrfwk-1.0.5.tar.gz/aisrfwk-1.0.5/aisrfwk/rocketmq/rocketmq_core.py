#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-14 16:30:50
# @Author  : wangmian05 (wangmian05@countrygraden.com.cn)
# @Link    : https://git.bgy.com.cn/bu00439/aisr-carbarn-ai.git
# @Version : $Id$
import json
import sys

from aisrfwk.util.config import config
from aisrfwk.util import log as log
from rocketmq.client import Producer

result_status = {"success": 0, "error": 1}

mq_message_size = 0


def buildProducer():
    producer = None
    try:
        # params_dict = {"id": task_id, "json": 0}
        # 建立MQ连接，配置标签
        producer = Producer(config.get("mq.producer", "aisr-fwk"), compress_level=9,
                            max_message_size=1024 * 1024 * 4)
        producer.set_namesrv_addr(config.get("mq.addr", "0.0.0.0:9876"))
        # 修改最大消息限制为2M
        producer.set_max_message_size(1024 * 1024 * 4)
        producer.start()
        log.info("producer start......")

    except:
        log.error("rocketmq producer start fail...{}", sys.exc_info())
        producer.shutdown()
    return producer


def sendMsg(topic, val):
    global mq_message_size
    if not bool(topic):
        log.error("消息发送失败,topic不能为空")
        return
    if not bool(val):
        log.error("消息发送失败,消息内容不能为空")
        return
    log.info("开始往topic:[{}],推送mq消息", topic)
    # log.info("开始往topic:[{}],推送mq消息:{}", topic, val)

    count = 0
    success = False
    while not success and count < 3:
        count += 1
        producer = None
        try:
            from rocketmq.client import Message, Producer
            msg = Message(topic)
            msg.set_tags('*')
            msg.set_body(val)
            # 发送信息,暂时使用同步发送
            producer = buildProducer()
            if producer:
                _p = json.dumps(producer.__dict__)
            else:
                log.error("生成者对象为空!!!")
            log.info("mq-size:{},开始发送消息:{}......", mq_message_size, val)
            # 发送一次消息本地记录一次,当数量大于一定值后归零,这个数量会影响到消息投递的队列
            # ret = producer.send_orderly(msg, mq_message_size, retry_times=30)
            ret = producer.send_sync(msg)
            log.info("消息发送完成.....")
            mq_message_size = 0 if mq_message_size > 10000000 else mq_message_size + 1
            log.info("消息是否发送成功:{},消息id:{}", mq_message_size, ret.status, ret.msg_id)
            success = True
            producer.shutdown()
        except:
            log.error("开始第[{}]此重试...消息发送失败:{}", count, sys.exc_info())
        finally:
            if producer is not None:
                producer.shutdown()

    log.info("推送mq消息完成:{}", success)
    if not success:
        log.error("重试三次都失败...不在重新发送")
        raise Exception("mq消息发送失败,重试三次都失败")
