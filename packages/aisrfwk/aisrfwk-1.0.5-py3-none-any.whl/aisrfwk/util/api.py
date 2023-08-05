import json

from aisrfwk.util import log as log, genid, redis_util
from aisrfwk.util import redis_util as redis


# 新任务处理加入队列
def pushQueue(content):
    log.info("push new task:{}", str(content)[0:100])
    task_id = buildTaskId(content)
    content["taskId"] = task_id
    redis_util.putTask(task_id, json.dumps(content))
    return {"taskId": task_id}


def buildTaskId(content):
    worker = genid.IdWorker(1, 1, 0)
    pro_id = content.get("projectId")
    if pro_id:
        task_id = str(pro_id) + str(worker.get_id())
    else:
        task_id = str(worker.get_id())
    content["taskId"] = task_id
    return task_id
