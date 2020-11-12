import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from db import db

def get_question(taskId):
    try:
        question = db.Question.find_one({"taskId": taskId})
        question_list = question.get("questionList")
        return question_list
    except:
        return []