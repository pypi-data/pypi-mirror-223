import sys
import json

from aisrfwk.util import log
from aisrfwk.domain.base_result import Result
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from aisrfwk.util.config import config, service_port
import aisrfwk.util.redis_util as redis

from aisrfwk.util import api

sys.path.append("..")

app = Flask(__name__)


@app.route('/')
@cross_origin()
def ping():
    return jsonify('pong')


@app.route('/park', methods=['POST'])
@cross_origin()
def park():
    """
    车位排布主方法
    """
    try:
        param = request.get_data()
        json_param = json.loads(param)
        validateParam(json_param)
        res = api.pushQueue({"test": "name"})
        return Result().success(res)
    except Exception as e:
        log.info(type(e))
        log.error("车位排布任务启动失败:" + str(e))
        return Result().error(str(e))


def validateParam(param):
    """根据图纸生成方案参数校验"""
    assert param.get("projectId") is not None, '项目ID参数[projectId]必须传入'
    # assert param.get("params") is not None, '指标参数[params]必须传入'
    # assert param.get("outer") is not None, '地库退线参数[outer]必须传入'
    # assert param.get("building") is not None, '楼栋外轮廓参数[outer]必须传入'
    # assert param.get("column") is not None, '剪力墙参数[column]必须传入'
    # assert param.get("coreBarrel") is not None, '核心筒参数[coreBarrel]必须传入'


def scheduleTask():
    try:
        log.debug("数据状态检测定时任务开始运行...")
        redis.restartTodoRunTask()
        # t = Timer(60*2, scheduleTask)
        # t.start()
    except Exception as e:
        log.error("当前定时任务运行出错:{}", str(e))


def start():
    """启动web服务"""
    server_host = config.get("server.host", "0.0.0.0")
    server_port = service_port if service_port != 0 else config.get("server.port", 5000)
    log.info("当前配置.端口号:{},ip:{}", server_host, server_port)
    # scheduleTask()
    app.run(host=server_host, port=server_port)


if __name__ == '__main__':
    # 本地运行Flask
    # po = Pool(10)  # 定义一个进程池，最大进程数10
    # 启动api监听
    start()
    # 启动队列监听
    # po.close( )
    # po.join()
