#coding:UTF-8
import pinyin

def to_pinyin(str):
    if str == None:
        return ""
    else:
        return pinyin.get(str,format='strip',delimiter="")
