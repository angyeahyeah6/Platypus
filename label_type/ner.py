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
# def get_answer_pair(taskId, labelIdList, transId):
#     answer_list = []
#     for labelId in labelIdList:
#         ans = db.Label.find_one({TASKID: taskId, LABELID: labelId})
#         label = db.Transaction.find_one({TASKID: taskId, TRANSACTIONID: transId})
#         answer_list.append((ans.get(TRUEANSWER), label.get(PREDANSWER)))
#     return answer_list

# def saveAnswer(data):
#     try:
#         userId = data.get(USERID)
#         # taskId = data.get(TASKID)
#         labelId = data.get(LABELID)
        
#         tmp_label = db.Ner.find_one({"labelId": labelId})
#         tmp_label.update({PREDANSWER: data.get("NERObject"), ALREADYLABEL: True, LABELERID: userId})
#         db.Ner.replace_one({"labelId": labelId},tmp_label)
#         return True
#     except:
#         return False
# def get_unlabel(taskId):
#     document = db.Ner.find_one({TASKID: taskId, ALREADYLABEL:False})
#     new_ner = {
#         "labelId": document.get("labelId"), 
#         "targetParagraph":document.get("targetParagraph")
#     }
#     return new_ner
