import os,sys,inspect
import uuid
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from db import db
from utils.constant import *
def get_user_all_level(userId):
    user_all_level = []
    for lev in db.Level.find({USERID: userId}):
        lev.pop("_id", None)
        user_all_level.append(dict(lev))  
    return user_all_level

def get_user_single_level(userId, taskType):
    return db.Level.find_one({USERID: userId, TASKTYPE: taskType})

def up_level(userId, taskType, level_info, points):
    try:
        level_percentage = level_info.get("levelPercentage")
        level = level_info.get("level")
        if level_percentage + points > 100:
            level += 1
            level_percentage  = level_percentage + points - 100
        level_info.update({"levelPercentage": level_percentage, "level": level})
        db.Level.replace_one({USERID: userId, TASKTYPE: taskType}, level_info)
        doc = db.Level.find_one({USERID: userId, TASKTYPE: taskType})
        return doc
    except:
        return False

