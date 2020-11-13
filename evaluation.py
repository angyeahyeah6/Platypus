from db import db
import numpy as np


def simple_accuracy(true_answer, label_answer):
    true_answer = np.array(true_answer)
    label_answer = np.array(label_answer)
    return np.sum(true_answer == label_answer)/len(true_answer)

def blue_accuracy(true_answer_list, pred_answer_list):
    accuracy = 0
    cnt = 0
    for true, pred in zip(true_answer_list, pred_answer_list):
        for n in true.keys():
            rignt_num = len(list(set(true[n]).intersection(pred[n])))
            all_num = len(list(set(true[n]).union(pred[n])))
            if all_num == 0:
                continue
            accuracy += rignt_num/all_num
            cnt += 1
    return accuracy/cnt


    