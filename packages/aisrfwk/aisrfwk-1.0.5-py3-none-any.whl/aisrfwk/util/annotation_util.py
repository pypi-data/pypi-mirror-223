import time

from aisrfwk.domain.base_aisr_task import BaseAisrTask
from aisrfwk.util import log as log


def Log(fn):
    """异步执行方法"""

    def wrapper(*args, **kwargs):
        log.info("{}方法开始执行", fn.__name__)
        method_start = time.time()
        res = fn(*args, **kwargs)
        method_end = time.time()
        methodTime = round(method_end - method_start, 2)
        log.info("{}方法执行完成,总耗时:[{}]秒...", fn.__name__, methodTime)
        return res

    return wrapper


def BussinesTask(fn):
    def wrapper(*args, **kwargs):
        log.info("{}标注", fn.__name__)
        b = BaseAisrTask()
        b.addSub(fn.__name__)

    return wrapper
