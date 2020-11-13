import os,sys,inspect
import uuid
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from db import db
from utils.constant import *
TASKID = "taskId"
LABELERID = "labelerId"
USERID = "userId"
TRUEANSWER = "trueAnswer"
PREDANSWER = "predAnswer"
LABELID = "labelId"

def to_transaction(data, transId):
    taskType = data.get(TASKTYPE)
    taskId = data.get(TASKID)
    userId = data.get(USERID)
    labelId = data.get(LABELID)
    if transId == None:
        transId = "transId" + str(uuid.uuid4().hex[:8])
    else:
        transId = transId
    new_trans = {
        TRANSACTIONID: transId,
        TASKID: taskId,
        LABELID: labelId,
        TASKTYPE: taskType,
        USERID : userId,
        PREDANSWER : data.get(NEROBJECT)
    }
    return transId, new_trans
