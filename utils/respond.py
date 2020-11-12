def return_success():
    return {"success": 1}


def return_success_with_data(data):
    dict_data = {"data": data, "success": 1}
    return dict_data

def return_failed():
    return {"success": 0}

def return_failed_with_msg(msg):
    return {"success": 0, "msg": msg}