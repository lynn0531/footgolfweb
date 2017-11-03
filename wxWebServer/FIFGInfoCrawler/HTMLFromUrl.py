#coding:UTF-8
import urllib
import urllib2
import json
import requests


class HTMLInfo(object):
    def getHtmlFromUrl(self,url):
        urlObject = urllib.urlopen(url)

        htmlInfo = urlObject.read()

        # print htmlInfo
        return htmlInfo

    def http_get(self):
        jsonValue = {'liga_id': '7', 'jugador_id': '2674', 'campo': 'liga'}
        jdata = urllib.urlencode(jsonValue)
        '''
        header = {'Host':'fgranks.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate, br',
            'X-Requested-With':'XMLHttpRequest',
            'Referer':'https://fgranks.com/fifg/worldtour?l=en'}
            '''
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'}

        #url = "https://fgranks.com/fifg/torneos/getDesglosePuntos?liga_id=7&jugador_id=4943&campo=liga"
        url = "https://fgranks.com/fifg/worldtour?l=en"
        dataUrl = "https://fgranks.com/fifg/torneos/getDesglosePuntos"
        s = requests.Session()
        s.get(url=url,headers=header)
        print "-------------------------------------------------------------------------------------------------"
        r = s.get(url='https://fgranks.com/fifg/torneos/getDesglosePuntos?liga_id=7&jugador_id=4943&campo=liga',
                         headers=header)

        print "结果:" + str(r.status_code) + "\n" + str(r.content)

# test
# print HTMLInfo().getHtmlFromUrl('https://fgranks.com/fifg/torneos/austria-international-austrian-footgolf-open')

#HTMLInfo().http_get()