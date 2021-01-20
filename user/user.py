from db import db
import os,sys,inspect
import uuid
import json
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from db import db
from utils.constant import *
def login(userId):
    try:
        user_info = db.User.find_one({"userId": userId})
        if user_info != None:
            user_info.pop('_id', None)
            return True
        else:
            create_new_user(userId)
            create_new_level(userId)
            return True
    except:
        return False
        
def create_new_user(userId):
    new_user = {
    "userId": userId,
    }
    db.User.insert_one(new_user)
def create_new_level(userId):
    for c in ["classification", "ner"]:
        db.Level.insert_one({
            "userId": userId,
            "taskType": c,
            "level": 0,
            "levelPercentage": 10
        })
    return True
def add_already_label_list(userId, new_trans):
    try:
        doc = db.User.find_one({USERID: userId})
        already_label_list = []
        if doc.get(ALREADYLABELLIST) == None:
            already_label_list = [t.get(LABELID) for t in new_trans]
        else:
            already_label_list = doc.get(ALREADYLABELLIST) + [t.get(LABELID) for t in new_trans]
        doc.update({ALREADYLABELLIST: already_label_list})
        db.User.replace_one({USERID: userId}, doc)
        return True
    except:
        return False
def get_already_label_list(userId):
    doc = db.User.find_one({USERID: userId})
    already_label_list = doc.get(ALREADYLABELLIST)
    if already_label_list == None:
        return []
    return already_label_list
def get_user_info(userId):
    labeled = get_already_label_list(userId)
    info = {'MRC': 0, "NER": 0, "CLAS": 0}
    for i in labeled:
        if(i[0] == 'm'):
            info['MRC'] += 1
        elif(i[0] == 'l'):
            info['CLAS'] += 1
        if(i[0] == 'n'):
            info['NER'] += 1
    return info