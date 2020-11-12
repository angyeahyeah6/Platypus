from db import db
# import label_type.classification as Classification
import label as Label
import uuid
from utils.constant import *
def get_all_task():
    all_tasks = []
    for task in db.Task.find({STATE: 1},{TASKID:1, TASKOWNERID:1, TASKOWNERNAME:1, TASKTITLE: 1, TASKTYPE: 1}):
        task.pop('_id', None)
        all_tasks.append(dict(task))
    return all_tasks
def get_task_by_task_type(taskType):
    tasks = []
    for t in db.Task.find({STATE: 1, TASKTYPE: taskType}):
        t.pop('_id', None)
        tasks.append(dict(t))
    return tasks
def get_task_type(taskId):
    task = db.Task.find_one({"taskId": taskId})
    return task.get("taskType")

def get_single_task(taskId):
    single_task = db.Task.find_one({"taskId": taskId})
    if single_task != None:
        single_task.pop("_id", None)
        return single_task
def get_self_uncheck_task(userId):
    tasks = []
    for t in db.Task.find({TASKOWNERID: userId, STATE: 0},{"taskIcon": 1, TASKID: 1, TASKTITLE:1, TASKTYPE:1, STATE:1}):
        t.pop('_id', None)
        tasks.append(dict(t))
    return tasks
def add_task(data):
    try:
        new_task={
            TASKID: "taskId" + str(uuid.uuid4().hex[:8]),
            TASKTITLE: data.get(TASKTITLE),
            STARTDATE: data.get(STARTDATE),
            ENDDATE: data.get(ENDDATE),
            TASKOWNERNAME: data.get(TASKOWNERNAME),
            TASKOWNERID : data.get(TASKOWNERID),
            TASKTYPE: data.get(TASKTYPE),
            PAYRULE: data.get(PAYRULE),
            "leastPayLimitPage": data.get("leastPayLimitPage"),
            "description": data.get("description"),
            "rating": 5,
            "ratingPeople": 0,
            STATE: 1,
            "examplePic": data.get("examplePic"),
            "taskIcon": data.get("taskIcon")
        }
        db.Task.insert_one(new_task)
        if data.get(TASKTYPE) == CLASSIFICATION:
            for ed in data.get("labeledDataList"):
                Label.add_example_data(new_task.get("taskId"), data.get("taskType"), ed)
            for ul in data.get("unlabeledDataList"):
                Label.add_unlabel_data(new_task.get("taskId"), data.get("taskType"), ul)
        return True
    except:
        return False

def add_rating(taskId, rating):
    task = db.Task.find_one({"taskId": taskId})
    total_rating = float(task.get("rating")) * int(task.get("ratingPeople"))  + rating
    task.update({"rating": total_rating, "ratingPeople": int(task.get("ratingPeople")) + 1})
    return True