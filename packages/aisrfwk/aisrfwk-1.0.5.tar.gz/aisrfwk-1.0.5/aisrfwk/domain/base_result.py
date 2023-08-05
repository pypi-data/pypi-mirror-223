#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-09-08 10:13:01
# @Author  : wangmian05
# @Link    : wangmian05@countrygraden.com.cn
# @Version : $Id$
# 统一返回结果
res_success_msg = "算法服务请求成功"
res_error_msg = "算法服务请求失败"

result_status = {"success": 0, "error": 1}


class Result:
    # 状态
    status = None
    # 状态
    message = None
    # 状态
    result = None

    def __init__(self, status=result_status.get("success"), message="", result={}):
        self.status = status
        self.message = message
        self.result = result

    def success(self, result):
        self.status = result_status.get("success")
        self.message = res_success_msg
        self.result = result
        return self.__dict__

    def error(self, msg):
        self.status = result_status.get("error")
        self.message = "{}:{}".format(res_error_msg, msg)
        self.result = {}
        return self.__dict__
