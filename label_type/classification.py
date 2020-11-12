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
        transId = "transId" + str(uuid.uuid4().hex[:8])
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
# def get_answer_pair(taskId, labelIdList, transId):
#     true_answer_list = []
#     pred_answer_list = []
#     for labelId in labelIdList:
#         ans = db.Label.find_one({LABELID: labelId, EXAMPLE: True})
#         true_answer_list.append(ans.get(TRUEANSWER))
#         label = db.Transaction.find_one({LABELID: labelId, TRANSACTIONID: transId})
#         pred_answer_list.append(label.get(PREDANSWER))
#     return true_answer_list, pred_answer_list

# def saveAnswer(data):
#     try:
#         userId = data[USERID]
#         classification = data["classification"]
#         for labelId in data.get("labelIdList"):
#             tmp_img = db.Classification.find_one({LABELID: labelId})
#             if tmp_img.get(EXAMPLE) == False:
#                 tmp_img.update({PREDANSWER: classification, LABELERID: userId, ALREADYLABEL: True})
#             db.Classification.replace_one({LABELID: labelId},tmp_img)
#         return True
#     except:
#         return False
# def get_label(taskId, labelCount):
#     return get_unlabel(taskId, labelCount) + get_example(taskId, labelCount)

# def get_unlabel(taskId, labelCount):
#     return_ques = []
#     cursor = db.Classification.find({TASKID: taskId, ALREADYLABEL:False, EXAMPLE:False})
#     cnt = 0
#     for l in cursor:
#         if cnt > labelCount/2:
#             break
#         cnt += 1
#         return_ques.append({LABELID: l.get(LABELID), IMAGEPATH: l.get(IMAGEPATH)})
#     print(return_ques)
#     return return_ques

# def get_example(taskId, labelCount):
#     return_ques = []
#     cursor = db.Classification.find({TASKID: taskId, EXAMPLE:True})
#     cnt = 0
#     for l in cursor:
#         if cnt > labelCount/2:
#             break
#         cnt += 1
#         return_ques.append({LABELID: l.get(LABELID), IMAGEPATH: l.get(IMAGEPATH)})
#     print(return_ques)
#     return return_ques


# def add_example_data(taskId, data):
#     new_label={
#         "labelId": "labelId" + str(uuid.uuid4().hex[:8]),
#         "trueAnswer": data.get("category"),
#         "predAnswer": "",
#         "imagePath": data.get("unlabeledData"),
#         "taskId": taskId,
#         "labelerId":"",
#         "example":True
#     }
#     db.Classification.insert_one(new_label)
#     return True

# def add_unlabel_data(taskId, data):
#     new_label={
#         "labelId": "labelId" + str(uuid.uuid4().hex[:8]),
#         "trueAnswer": "",
#         "predAnswer": "",
#         "imagePath": data,
#         "alreadyLabel":False,
#         "taskId": taskId,
#         "labelerId":"",
#         "example":False
#     }
#     db.Classification.insert_one(new_label)
#     return True