"""
load data for display at demo page ver2
~08.25.2017
Stackcat
"""
import os, csv, random

# get data from CSV file
def getData(f):
    r = csv.DictReader(f)
    result = []
    for line in r:
        result.append(line)
    return result

def makeBodyDict():
    file_bodies = open("/home/fndetect/server/data/submission/test_bodies.csv", "r", encoding="utf8")
    d = getData(file_bodies)
    result = {}
    for i in d:
        result[i["Body ID"]] = i['articleBody'] 
    return result

# make candidate
def candidate():
    CANDIDATE_SIZE = 10
    file_submission = open("/home/fndetect/server/data/submission/submission.csv", "r", encoding="utf8")
    submission = getData(file_submission)
    bodies = makeBodyDict() 
    
    sample_head = random.sample(range(len(submission)), CANDIDATE_SIZE)
    sample_body = random.sample(bodies.keys(), CANDIDATE_SIZE)

    result_head = [submission[i]['Headline'] for i in sample_head]
    result_body = [[i, bodies[i]] for i in sample_body]
    
    result_head_file = open(os.path.join(os.path.dirname(__file__), "static", "candidate_head.txt"), "w", encoding='utf8')
    result_body_file = open(os.path.join(os.path.dirname(__file__), "static", "candidate_body.txt"), "w", encoding="utf8")

    for h in result_head:
        h = h.replace("\'", "`")
        result_head_file.write(h+"\n")
    for b in result_body:
        # !#@!#@ : split key
        result_body_file.write("{}!#@!#@{}\n".format(b[0], b[1].replace("\n","|")))

# test code for debugging
def candidateTest():
	testfile = open(os.path.join(os.path.dirname(__file__), "static","makeCandidateTestFile.txt"), "w", encoding="utf8")
	testfile.write("mctf")
	testfile.close()

if __name__ == "__main__":
	candidateTest()
