import time
from abc import abstractmethod
from aisrfwk.util import log


# from aisrfwk.util import rocketmq_util

class BaseAisrTask:
    son_implements = []

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls._instance = super(BaseAisrTask, cls).__new__(cls)
    #     return cls._instances
    # def __int__(self,c):
    #     print(c)

    def addSub(self, class_name):
        self.son_implements.append(class_name)

    @abstractmethod
    def run(self, data):
        try:
            log.info("当前为基类业务逻辑方法,如需接入业务处理.请自行创建业务处理方法,同时继承BaseAisrTask")
            # rocketmq_util.sendResultToServer()
            time.sleep(1)
            # rocketmq_util.sendTaskOverToServer()
        except BaseException as e:
            log.info("基类业务处理发生异常:{}", e)
        pass
