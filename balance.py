from db import db
def get_balance(taskId, taskType, userId):
    if taskType == "classification":
        number = db.Classifiction.count_documents({"labelerId": userId, "taskId": taskId})
        task_info = db.Task.find_one({"taskId":taskId})
        total_earn = number * task_info.get("payRule")
    return total_earn

