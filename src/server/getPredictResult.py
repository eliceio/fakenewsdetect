"""
get Predict Result at demo page ver2
08.25.2017
Stackcat
"""
from django.http import HttpResponse
import json
from DB import Database
import numpy as np
import predCat
import logging


def predict(head, body_id):
    feedback_w = 0.001
    db = Database()
    stance_idx_dict = {0:'agree', 1:'disagree', 2:'discuss', 3:'unrelated'}
    # ther are previous data in DB
    try:
        predict_result = db.get_predict_result_info(head, body_id)
        idx = predict_result[0]
        stances = np.array(predict_result[3:-1])
        currentFeedback = np.array(eval(predict_result[-1])) * feedback_w
        stances += currentFeedback
        result = np.ndarray.tolist(stances)
    # new data
    except Exception as e:
        logging.exception("in getPredictResult.py. predict- except",e)
        result = predCat.get_result_stances(head, body_id)
        db.save_predict_data(head, body_id, result)
        idx = db.getMaxID()


    result_stance = stance_idx_dict[result.index(max(result))]
     
    response = HttpResponse(json.dumps({'result':result_stance, 'idx':idx}))

    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = 1000
    response['Access-Control-Allow-Headers'] = '*'
    return response

# test code for debugging
def testcode():
    h = "ndian bride marries wedding guest"
    bid = 528
    s = predict(h,bid)
    print(s)

if __name__ == "__main__":
    testcode()
