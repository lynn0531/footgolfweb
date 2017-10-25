#coding:UTF-8
import urllib

class HTMLInfo(object):
    def getHtmlFromUrl(self,url):
        urlObject = urllib.urlopen(url)

        htmlInfo = urlObject.read()

        # print htmlInfo
        return htmlInfo

# test
# print HTMLInfo().getHtmlFromUrl('https://fgranks.com/fifg/torneos/austria-international-austrian-footgolf-open')