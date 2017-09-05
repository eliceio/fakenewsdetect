"""
views.py
~08.25.2017
Stackcat
"""


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from DB import Database
import csv
import random
import os
import json
import numpy as np 
import math
import getPredictResult as gpr
import makeCandidate 
import logging
import tensorflow as tf
from django.core.cache import cache


# get Data in CSV file
def getData(f):
    r = csv.DictReader(f)
    result = []
    for line in r:
        result.append(line)
    return result

# main page. demo ver1 
def index(request):   
    feedback_w = 0.001
    file_bodies = open("/home/fndetect/server/data/submission/test_bodies.csv","r",encoding="utf-8")
    bodies = getData(file_bodies)
     
    db = Database()
    cnt = db.get_db_count()
    randomIdx = random.randint(0, cnt) 
    stance_label = ["agree", "disagree", "discuss", "unrelated"]

    data = db.get_train_result_info(randomIdx)
    title = data[1]
    bodyID = data[2]
    stances = np.array(data[3:-1])

    # feedback processing
    currentFeedback = np.array(eval(data[-1])) * feedback_w
    stances += currentFeedback
    stances = np.ndarray.tolist(stances)

    body = ''
    for i in bodies:
        if i['Body ID'] == str(bodyID):
            body = i['articleBody'].replace("\n","|")
            break
    stance = stance_label[stances.index(max(stances))]

    return render(request, 'demo/index.html', {'idx':randomIdx, 'title':title,'body':body,'stance':stance, 'body_id':bodyID})

### Stack -- demo.ver2
def ver2(request):
    # if you want reset candidate data, remove the comment symbol below.
    # you can reset candidate data on demo page too.
    # makeCandidate.candidate()
    return render(request, 'demo/ver2.html')

def resetCandidate(request):
    makeCandidate.candidate()
    return render(request, 'demo/ver2.html')

# there are two kind of method to nomalize data.
# we using common normalize
def normalize_log(stances):
    maxprob = max(stances)
    for i in range(len(stances)):
        stances[i] -= maxprob
        stances[i] = math.exp(stances[i])
    nor_const = 1. / float(sum(stances))
    for i in range(len(stances)):
        stances[i] *= nor_const
    return stances

# we using it!
def normalize(stances):
    return [float(i)/sum(stances) for i in stances]

# "csrf_exempt" is required for POST communication
@csrf_exempt
def receiveData(request): 
    title = request.POST.get('title')
    body_id = request.POST.get('body_id')
     
    #result = HttpResponse("{},{}".format(title, body_id))
    result = gpr.predict(title, body_id)
    return  result

@csrf_exempt
def feedback_ver2(request):
    try:
        db = Database()
        feedback = request.POST.get('feedback')
        high_mode = str(request.POST.get("high_mode"))
        idx = eval(request.POST.get("idx"))
        logging.exception(feedback, "--", high_mode, "--", idx)      
        stance_dict = {"agree":0, "disagree":1, "discuss":2, "unrelated":3}
        #data = db.get_predict_result_info(title, body_id)
        data = db.get_predict_result_by_id(idx)
        
        currentFeedback = eval(data[-1])

        if("High-Mode" in high_mode):
            currentFeedback[stance_dict[feedback]] += 100
        else:
            currentFeedback[stance_dict[feedback]] += 1
        
        db.save_feedback_ver2(idx,currentFeedback)
        if "High-Mode" in high_mode :
            return HttpResponse("High True")
        else:
            return HttpResponse(high_mode)
    except Exception as e:
        logging.exception("IN FEEDBACK_VER2----------------------------------------", e)
        return HttpResponse(str(e))

### Cat -- demo.ver2

@csrf_exempt
def feedback(request):
    if request.is_ajax():
        db = Database()
        article_id = request.POST.get('idx')
        feedback = request.POST.get("feedback")
        high_mode = request.POST.get("high_mode")
        data = db.get_train_result_info(article_id)
        stance_dict = {"agree":0, "disagree":1, "discuss":2, "unrelated":3}
        
        title = data[1]
        bodyID = data[2]
        currentFeedback = eval(data[-1])
        currentFeedback[stance_dict[feedback]] += 1
        db.save_feedback_ver1(article_id, currentFeedback)                
    return HttpResponseRedirect("/")

# test code for debugging
def testcode():
    try:
        db = Database()
        title = "This Third Boob Is Probably Only Real in Our Hearts"
        body_id = 910
        feedback = 'agree'
        high_mode = "High-Mode"
        stance_dict = {"agree":0, "disagree":1, "discuss":2, "unrelated":3}
        data = db.get_predict_result_info(title, body_id)
        print("data:{}".format(data))
        currentFeedback = eval(data[-1])
        idx = data[0]
        currentFeedback[stance_dict[feedback]] += 3
        print(currentFeedback)
        db.save_feedback_ver2(idx, currentFeedback)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    testcode()
