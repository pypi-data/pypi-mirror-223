import sys
import time

from aisrfwk.domain.base_aisr_task import BaseAisrTask
# from aisrfwk.util import log, redis_util, rocketmq_util
from aisrfwk.util.exception_util import formatException


class BusinessDemo(BaseAisrTask):

    def run(self, data):
        start_time = time.time()

        task_id = None
        try:
            # log.info("业务方法处理逻辑")
            print("xxxx")
            # 过程中处理结果发送到服务端
            # rocketmq_util.sendResultToServer()
        except BaseException as e:
            _msg = "车位排布任务失败,请检查底图和图层选择后再次重试!"
            _err_msg = "【严重】车位排布任务失败,内圈车位排布过程中出现异常:"
            # log.error(_err_msg + "{}", str(e))
            # exc_text = _err_msg + "<br />" + formatException(sys.exc_info())
            # redis_util.errorTaskStatus(task_id, exc_text)
            # rocketmq_util.sendErrorToServer()
        # 处理结束后发送消息到后端服务
        time.sleep(1)
        # rocketmq_util.sendTaskOverToServer()

        end_time = time.time()
        # log.info("所有车位排布生成完成,总耗时:[{}]秒", round(end_time - start_time, 2))
