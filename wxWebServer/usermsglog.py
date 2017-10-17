#coding:UTF-8
#encoding=utf-8
# filename: footgolfinfo.py
import MySQLdb
import datetime
from utility.configInfo import ConfigInfo

class UserMsg(object):
    def recordUserTxtMsgLog(self,msgid,userid,msgtime,msgtype,msgcontent):
        conf = ConfigInfo("conf/footgolf.ini")
        dbInfo = conf.getDBInfo()
        conn = MySQLdb.connect(host=str(dbInfo['host']), port=int(dbInfo['port']), user=str(dbInfo['user']),
                               passwd=str(dbInfo['pwd']), db=str(dbInfo['dbname']), charset='utf8')
        try:
            ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insertSql = "insert into user_msg (msgid,wxuserid,msgtime,msgtype,msgcontent,create_time) values ('%s','%s','%s','%s','%s','%s');" % (msgid,userid,int(msgtime),msgtype,msgcontent,ctime)
            print insertSql

            cur = conn.cursor()
            count = cur.execute(insertSql)
            conn.commit()
            print str(count)
        except Exception, Argment:
            print "error:" + str(Argment)
        finally:
            cur.close()
            conn.close()
            print "连接已关闭"
# test
# um = UserMsg()
# um.recordUserTxtMsgLog("abc","abc","123123","text","haha test 2")