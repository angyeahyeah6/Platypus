from db import db
from utils.constant import *
import uuid
import label_type.classification as Classification
import label_type.ner as Ner
import user.user as User
import math
def saveAnswer(data):
    try:
        userId = data.get(USERID)
        taskType = data.get(TASKTYPE)
        if taskType == None:
            return False
        # taskId = data.get(TASKID)
        transId = data.get(TRANSACTIONID)
        if taskType == "classification":
            # labelIdList = data.get(LABELIDLIST)
            transId, new_trans = Classification.to_transaction(data, transId)
            db.Transaction.insert_many(new_trans)
            if not User.add_already_label_list(userId, new_trans):
                return False
        elif taskType == "ner":
            # labelId = data.get(LABELID)
            transId, new_trans = Ner.to_transaction(data, transId)
            db.Transaction.insert_one(new_trans)
            if not User.add_already_label_list(userId, [new_trans]):
                return False
        # update_already_label(transId, taskId, taskType, labelIdList)
        return {TRANSACTIONID:transId}
    except:
        return False
def get_answer_pair(taskId, transId):
    true_answer_list = []
    pred_answer_list = []
    cursor = db.Transaction.find({TRANSACTIONID:transId})
    for tr in cursor:
        labelId = tr.get(LABELID)
        exp = db.Label.find_one({TASKID:taskId, LABELID: labelId})
        if exp.get(EXAMPLE) == False:
            continue
        pred_answer_list.append(tr.get(PREDANSWER))
        true_answer_list.append(exp.get(TRUEANSWER))
    return true_answer_list, pred_answer_list

def update_already_label(transId, taskId, taskType, labelIdList):
    for lb in labelIdList:
        doc = db.Label.find_one({TASKID:taskId, LABELID:lb, TASKTYPE: taskType})
        if doc.get(EXAMPLE) == False:
            doc.update({ALREADYLABEL:True, TRANSACTIONID: transId})
            db.Label.replace_one({TASKID:taskId, LABELID:lb}, doc)
    return True

def get_label(userId, taskId, taskType, labelCount):
    # already_label_list = []
    already_label_list = User.get_already_label_list(userId)
    if taskType == CLASSIFICATION:
        example_cnt = math.ceil(labelCount/2)
        example_label = get_label_from_db(taskId, taskType, example_cnt, already_label_list, True)
        unlabel_cnt = (example_cnt - len(example_label)) + math.floor(labelCount/2)
        return example_label + get_label_from_db(taskId, taskType, unlabel_cnt, already_label_list, False)
    elif taskType == NER:
        return get_label_from_db(taskId, taskType, labelCount, already_label_list, example=True)

def get_label_from_db(taskId, taskType, labelCount, already_label_list, example=True):
    return_ques = []
    if example == True:
        question_list = db.Question.find_one({"taskId": taskId}).get("questionList")
        cursor = db.Label.aggregate([{ 
            "$match": 
            {"$or": [{TASKID: taskId, TASKTYPE:taskType, EXAMPLE:example, TRUEANSWER:question_list[0]}, {TASKID: taskId, TASKTYPE:taskType, EXAMPLE:example, TRUEANSWER: question_list[1]}]} }, 
            { "$sample": { "size": labelCount*2 } }])
    else:
        cursor = db.Label.aggregate([{ "$match": {TASKID: taskId, TASKTYPE:taskType, EXAMPLE:example} }, { "$sample": { "size": labelCount*2 } }])
    for l in cursor:
        if l.get(LABELID) in already_label_list:
            continue
        if labelCount == 0:
            break
        labelCount -= 1
        if taskType == "classification":
            return_ques.append({LABELID: l.get(LABELID), IMAGEPATH: l.get(IMAGEPATH)})
        elif taskType == "ner":
            return_ques.append({LABELID: l.get(LABELID), TARGETPARAGRAPH: l.get(TARGETPARAGRAPH
            )})
    return return_ques

# def get_example(taskId, taskType, labelCount, page):
#     return_ques = []
#     cursor = db.Label.find({TASKID: taskId, TASKTYPE:taskType, EXAMPLE:True})
#     cnt = 1
#     for l in cursor:
#         if cnt < page:
#             cnt += 1
#             continue
#         if len(return_ques) >= int(labelCount/2)+1:
#             break
#         if taskType == "classification":
#             return_ques.append({LABELID: l.get(LABELID), IMAGEPATH: l.get(IMAGEPATH)})
#         elif taskType == "ner":
#             return_ques.append({LABELID: l.get(LABELID), TARGETPARAGRAPH: l.get(TARGETPARAGRAPH
#             )})
#     return return_ques

def add_example_data(taskId, taskType, data):
    new_label={
        "labelId": "labelId" + str(uuid.uuid4().hex[:16]),
        "taskId": taskId,
        "taskType": taskType,
        "trueAnswer": data.get("category"),
        "imagePath": data.get("unlabeledData"),
        "example":True
    }
    db.Label.insert_one(new_label)
    return True

def add_unlabel_data(taskId, taskType, data):
    new_label={
        "labelId": "labelId" + str(uuid.uuid4().hex[:8]),
        "taskId": taskId,
        "trueAnswer": "",
        "alreadyLabel":False,
        "example":False
    }
    if taskType == CLASSIFICATION:
        new_label.update({IMAGEPATH: data})
    elif taskType == NER:
        new_label.update({TARGETPARAGRAPH: data})
    db.Label.insert_one(new_label)
    return True
