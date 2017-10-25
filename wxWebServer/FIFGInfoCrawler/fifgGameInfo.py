#coding:UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

class FIFGGameInfo(object):
    def parseGameListHtmlData(self, content):
        #content = open("/Users/lynn/程序开发/python/data/footgolfrankdata.html",'r') #TODO 替换
        soup = BeautifulSoup(content,"lxml")
        result = {}
        try:
            gameListTable = soup.find(text=" World Tour Tournaments").parent.parent.find_all('a') # 定位赛事区域<a>标签
            print len(gameListTable)
            gameInfoList = []
            for aTemp in gameListTable:
                gameName = aTemp.contents[2].replace('\n','').replace('                         ','')
                gamePageLink = aTemp['href']
                gameLevelInfo = aTemp.img['src'].split('/')
                gameLevelTemp = gameLevelInfo[len(gameLevelInfo) - 1].split('.')
                gameLevel = gameLevelTemp[0]
                gameInfo = {}
                gameInfo["gameName"] = gameName
                gameInfo["gamePageLink"] = gamePageLink
                gameInfo["gameLevel"] = gameLevel
                gameInfoList.append(gameInfo)

            result["result"] = 0
            result["gameInfo"] = gameInfoList
            #print result
            print "赛事列表获取成功。"
            return result
        except Exception, Argment:
            print "赛事列表获取失败-error:" + str(Argment)
            result['result'] = -1
            return result

    def parseGameRankInfo(self, content):
        thCount = 9  # 常量刨除round的列数
        #content = open("/Users/lynn/程序开发/python/data/footgolfGameInfoData.html", 'r')  # TODO 替换
        soup = BeautifulSoup(content, "lxml")
        result = {}
        try:
            gameRankTable = soup.find('table',id="ranking_individual") # 赛事排名
            roundCount = len(gameRankTable.find_all('th')) - thCount  # 计算比赛轮数s
            # print "roundCount: " + str(roundCount)

            individualRankTR = gameRankTable.tbody.find_all("tr", attrs={"data-tipo": 'jugador'})
            print "参赛球员数：" + str(len(individualRankTR))
            rankInfoList = []
            for trTemp in individualRankTR:
                memberRankInfo = {}
                tds = trTemp.find_all("td")
                #tdText = "" + trTemp['data-id'] + ";"
                memberRankInfo["fifgId"] = trTemp['data-id']

                memberRankInfo["pos"] = tds[1].string
                # memberRankInfo["memImageUrl"] = tds[3].string
                # memberRankInfo["countryIconUrl"] = tds[4].string
                memberRankInfo["name"] = tds[5].string
                tourTemp = tds[4].find('img')
                if tourTemp == None:
                    memberRankInfo["tour"] = None
                else:
                    memberRankInfo["tour"] = "1"

                # set round data
                for i in range(1,roundCount + 1):
                    memberRankInfo["round" + str(i)] = tds[6 + i].string
                memberRankInfo["total"] = tds[6 + roundCount + 1].string
                memberRankInfo["topar"] = tds[6 + roundCount + 2].string
                memberRankInfo["roundCount"] = roundCount
                rankInfoList.append(memberRankInfo)

            result["result"] = 0
            result["gameResultInfo"] = rankInfoList
            #print result
            print "赛事结果列表获取成功。"
            return result
        except Exception, Argment:
            print "赛事结果列表获取失败-error:" + str(Argment)
            result['result'] = -1
            return result


# test
#print FIFGGameInfo().parseGameRankInfo("")
