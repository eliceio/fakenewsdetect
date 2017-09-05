"""
Database tool
~ 08.25.2017
Stackcat
"""
import pymysql
import logging

class Database:
    def __init__(self):
        conn = pymysql.connect(host='localhost', user='root', password='root', db='djangoDB', charset='utf8', autocommit=True)
        self.curs = conn.cursor()
    
    def get_train_result_info(self, idx):
        self.curs.execute("select * from train_result where id = " + str(idx) + ";")
        return self.curs.fetchall()[0]

    def get_db_count(self):
        self.curs.execute("select count(*) from train_result;")
        return self.curs.fetchall()[0][0]
    
    def save_feedback_ver1(self, idx, feedback):
        s = ("update train_result set feedback = '{}' where id = {};".format(str(feedback), idx))
        self.curs.execute(s)
    
    def updateFeedback(self, idx, feedback):
        s = "update predict_reslt set feedback = '{}' where id = {}".format(str(feedback), idx)
        self.curs.execute(s)
     
    def save_predict_data(self, head, body_id, stances):
        logging.exception("\nin SAVE_PREDICT_DATA \n", str(head), str(body_id), str(stances))
        s = "insert into predict_result(headline, bodyid, stance1, stance2, stance3, stance4) values('{}',{},{},{},{},{});".format(head, body_id, stances[0], stances[1], stances[2], stances[3])
        self.curs.execute(s)

    def get_predict_result_info(self, head, body_id):
        s = "select * from predict_result where headline = '{}' and bodyid = {}".format(head, body_id)
        self.curs.execute(s)
        r = self.curs.fetchall()
        logging.exception("{}--------{}".format("IN_GET_PREDICT_RESULT_INFO_UP", str(r)))
        return r[0]
         
    def getMaxID(self):
        self.curs.execute("select max(id) from predict_result")
        return self.curs.fetchall()[0]
    def get_predict_result_by_id(self, idx):
        try: 
            s = "select * from predict_result where id = {}".format(idx)
            self.curs.execute(s)
            return self.curs.fetchall()[0]
        except Exception as e:
            logging.exception(e)
            return e
         
    def save_feedback_ver2(self, idx, feedback):
        s = ("update predict_result set feedback ='{}' where id = {};".format(str(feedback), idx))
        self.curs.execute(s)

    def getFeedbackData(self):
        s = "select * from predict_result"
        self.curs.execute("select * from predict_result;")
        return self.curs.fetchall()[0]

    def uploadTrainResult(self,h, b, s1, s2, s3, s4):
        s = "INSERT INTO train_result(headline, bodyid, stance1, stance2, stance3, stance4) VALUES(%s, %s, %s, %s, %s, %s);" % (h,b,s1,s2,s3,s4)
        self.curs.execute(s)
    
    def getFeedback(self, tableName):
        s = "select feedback from %s" % (tableName)
        self.curs.execute(s)
        return self.curs.fetchall()


def test():
    db = Database()
    idx = 15
    s=db.get_predict_result_by_id(idx)
    print(s)

if __name__ == "__main__":
    test()
