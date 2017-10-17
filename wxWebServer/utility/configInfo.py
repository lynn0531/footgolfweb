#coding:UTF-8
# filename: configInfo.py
import ConfigParser

class ConfigInfo(object):
    def __init__(self, path):
        self.path = path

    def getDBInfo(self):
        conf = ConfigParser.ConfigParser()
        dbInfo = {}
        try:
            conf.read(self.path)
            dbInfo['host'] = conf.get("db", "host")
            dbInfo['port'] = conf.get("db", "port")
            dbInfo['user'] = conf.get("db", "user")
            dbInfo['pwd'] = conf.get("db", "pwd")
            dbInfo['dbname'] = conf.get("db", "dbname")
        except Exception, Argment:
            print "error:" + str(Argment)
        finally:
            return dbInfo
