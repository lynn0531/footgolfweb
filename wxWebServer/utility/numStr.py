#coding:UTF-8
class NumStrUtil(object):
    def convertToInt(sefl,str,default):
        try:
            intData = int(str)
            return intData
        except Exception, Argment:
            return default