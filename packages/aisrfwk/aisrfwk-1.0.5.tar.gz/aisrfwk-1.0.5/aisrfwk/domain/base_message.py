#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-08 10:13:01
# @Author  : wangmian05
# @Link    : wangmian05@countrygraden.com.cn
# @Version : $Id$
# 统一返回结果
status_success = 0
status_error = 1


class Result:
    # 任务id
    taskId = None
    # 状态
    status = None
    # 消息
    msg = None

    def __init__(self, taskId, status=status_success, message=""):
        self.taskId = taskId
        self.status = status
        self.message = message

    def success(self, taskId):
        self.taskId = taskId
        self.status = status_success
        return self.__dict__

    def error(self, taskId, msg):
        self.taskId = taskId
        self.status = status_error
        self.msg = msg
        return self.__dict__
