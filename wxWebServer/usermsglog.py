#coding:UTF-8
#encoding=utf-8
# filename: footgolfinfo.py
import datetime
from utility.mysqlaccess import MysqlAccessBase

class UserMsg(object):
    def recordUserTxtMsgLog(self,msgid,userid,msgtime,msgtype,msgcontent):
        mysqlAccess = MysqlAccessBase()
        try:
            ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insertSql = "insert into user_msg (msgid,wxuserid,msgtime,msgtype,msgcontent,create_time) values (%s,%s,%s,%s,%s,%s);"
            sqlParam = [msgid, userid, int(msgtime), msgtype, msgcontent, ctime]
            print insertSql
            mysqlAccess.update(insertSql, sqlParam)
            print "message log update success."
        except Exception, Argment:
            print "error:" + str(Argment)
        finally:
            mysqlAccess.close()
            print "连接已关闭"
# test
# um = UserMsg()
#um.recordUserTxtMsgLog("abc","abc","123123","text","haha test 2")