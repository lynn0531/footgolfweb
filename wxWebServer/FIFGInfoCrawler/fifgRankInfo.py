#coding:UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

class FIFGRankInfo(object):
    def parseRankHtmlData(self, content):
        # htmlData = open("/Users/lynn/程序开发/python/data/footgolfrankdata.html",'r')
        #diagnose("<html>data</html>")
        soup = BeautifulSoup(content,"lxml")
        result = {}
        try:
            individualRankTable = soup.find("table",id='ranking_individual')

            individualRankTR = individualRankTable.tbody.find_all("tr", attrs={"data-tipo":'jugador'})
            print len(individualRankTR)
            rankInfoList = []
            for trTemp in individualRankTR:
                memberRankInfo = {}
                tds = trTemp.find_all("td")
                tdText = "" + trTemp['data-id'] + ";"
                memberRankInfo["sysId"] = trTemp['data-id']
                memberRankInfo["teamId"] = tds[0].string
                memberRankInfo["association"] = tds[1].string
                memberRankInfo["pos"] = tds[2].string
                # memberRankInfo["memImageUrl"] = tds[3].string
                # memberRankInfo["countryIconUrl"] = tds[4].string
                memberRankInfo["name"] = tds[5].string
                if tds[6].string == "-":
                    memberRankInfo["score"] = str(0)
                else:
                    memberRankInfo["score"] = tds[6].string.replace(',', '')
                rankInfoList.append(memberRankInfo)
                for tdTemp in tds:
                    tdText += str(tdTemp.string) + ";"
                # print tdText
            #print rankInfoList
            result["result"] = 0
            result["RankInfo"] = rankInfoList
            return result
        except Exception, Argment:
            print "error:" + str(Argment)
            result['result'] = -1
            return result
# test
#fifg = FIFGRankInfo()
#fifg.parseRankHtmlData("")