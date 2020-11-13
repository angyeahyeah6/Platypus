import os,sys,inspect
import uuid
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from db import db
from utils.constant import *

def to_transaction(data, transId):
    labelIdList = data.get(LABELIDLIST)
    taskType = data.get(TASKTYPE)
    taskId = data.get(TASKID)
    userId = data.get(USERID)
    classification = data.get(CLASSIFICATION)
    if transId == None or transId == "":
        transId = "transId" + str(uuid.uuid4().hex[:16])
    else:
        transId = transId
    new_trans = []
    for lb in labelIdList:
        new_trans.append({
            TRANSACTIONID: transId,
            TASKID: taskId,
            LABELID: lb,
            PREDANSWER: classification,
            TASKTYPE: taskType,
            USERID: userId
        })
    return transId, new_trans