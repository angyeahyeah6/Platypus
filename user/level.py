from db import db
USERID = "userId"
TASKTYPE = "taskType"
LEVEL = "level"
def get_user_all_level(userId):
    user_all_level = []
    for lev in db.Level.find({USERID: userId}):
        lev.pop("_id", None)
        user_all_level.append(dict(lev))  
    return user_all_level

def get_user_single_level(userId, taskType):
    return db.Level.find_one({USERID: userId, TASKTYPE: taskType})