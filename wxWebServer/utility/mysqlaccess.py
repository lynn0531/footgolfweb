#coding:UTF-8
#encoding=utf-8
# filename: mysqlaccess.py
import MySQLdb
from configInfo import ConfigInfo

conf = ConfigInfo("conf/footgolf.ini")
dbInfo = conf.getDBInfo()

class MysqlAccessBase(object):
    def __init__(self):
        self.connFlg = False
        try:
            self.conn = MySQLdb.connect(host=str(dbInfo['host']), port=int(dbInfo['port']), user=str(dbInfo['user']),
                                   passwd=str(dbInfo['pwd']), db=str(dbInfo['dbname']), charset='utf8')
            self.cursor = self.conn.cursor()
            self.connFlg = True
        except MySQLdb.Error as e:
            self.connFlg = False
            print ("Mysql Error: %d %s." % (e.args[0],e.args[1]))
    # 更新数据
    def update(self, sql, sqlParam):
        updateFlg = False
        try:
            if self.connFlg:
                self.cursor.execute(sql, sqlParam)
                self.conn.commit()
                updateFlg = True
        except MySQLdb.Error as e:
            self.conn.rollback()
            updateFlg = False
            print ("Mysql Error: %s %s" % (e.args[0], e.args[1]))
        finally:
            return updateFlg
    # 获取数据集
    def query(self, sql, sqlParam):
        try:
            if self.connFlg:
                self.cursor.execute(sql, sqlParam)
                dataSet = self.cursor.fetchall()
                return dataSet
        except MySQLdb.Error as e:
            print ("Mysql Error: %s %s" % (e.args[0], e.args[1]))
    # 关闭mysql连接
    def close(self):
        try:
            if self.connFlg:
                if type(self.cursor) == 'object':
                    self.cursor.close()
                if type(self.conn) == 'object':
                    self.conn.close()
        except MySQLdb.Error as e:
            print ("Mysql Error: %d %s." % (e.args[0], e.args[1]))
