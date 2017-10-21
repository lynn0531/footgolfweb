#coding:UTF-8
import urllib

class HTMLInfo(object):
    def getHtmlFromUrl(self,url):
        urlObject = urllib.urlopen(url)

        htmlInfo = urlObject.read()

        # print htmlInfo
        return htmlInfo