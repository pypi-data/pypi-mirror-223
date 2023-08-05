#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-06 15:52:46
# @Author  : wangmian05
# @Link    : wangmian05@countrygraden.com.cn
# @Version : $Id$
import json
import time
import redis
from aisrfwk.util.config import config
from aisrfwk.util import log as log
from aisrfwk.util.mail_util import sendMail

env_prefix = config.get("env") + ":" if "env" in config and len(config.get("env")) > 0 else ""
global_key = config.get("redis.global_key","aisr-fwk")

task_status = {"todo": 1, "running": 2, "success": "3", "error": "4"}

conn_pool = redis.ConnectionPool(host=config.get("redis.host"), port=config.get("redis.port"),
                                 db=config.get("redis.db"), password=config.get("redis.passwd"))
re_pool = redis.Redis(connection_pool=conn_pool, health_check_interval=30, socket_keepalive=30)


def setStr(key, val):
    return re_pool.set(global_key +":"+ key, val)


def getStr(key):
    return str(re_pool.get(global_key +":"+ key))


def setHash(key, hkey, hval):
    return re_pool.hset(key, hkey, hval)


def getHash(key, hkey):
    return str(re_pool.hget(key, hkey))


def lPush(key, val):
    return re_pool.lpush(key, str(val))


def rPop(key):
    sss = re_pool.rpop(key)
    return str(sss.decode("utf-8")) if sss is not None else ''


# 先进先出.阻塞队列出的内容为元组类型,0=队列key,1=队列值
def bRpop(key):
    tup = re_pool.brpop(key, timeout=30)
    if tup is None:
        return
    val = tup[1]
    return str(val.decode("utf-8")) if val is not None else ''
