#coding:UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import copy
import time

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
                if aTemp.find('img') == None:
                    gameName = None
                    gameLevel = None
                else:
                    gameName = aTemp.contents[2].replace('\n','').replace('                         ','')
                    gameLevelInfo = aTemp.img['src'].split('/')
                    gameLevelTemp = gameLevelInfo[len(gameLevelInfo) - 1].split('.')
                    gameLevel = gameLevelTemp[0]
                gamePageLink = aTemp['href']


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
        noToparCount = 8
        #content = open("/Users/lynn/程序开发/python/data/footgolfGameInfoData.html", 'r')  # TODO 替换
        soup = BeautifulSoup(content, "lxml")
        result = {}
        try:
            gameRankTable = soup.find('table',id="ranking_individual") # 赛事排名
            toparTh = gameRankTable.find("th",text="To Par")
            if toparTh == None:
                roundCount = len(gameRankTable.find_all('th')) - noToparCount  # 计算比赛轮数s
            else:
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
                if toparTh == None:
                    memberRankInfo["topar"] = None
                else:
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

    def parseGamePlayerWholeResult(self, content, fifgId):
        soup = BeautifulSoup(content, "lxml")
        #print soup.prettify()
        result = {}
        try:
            wholeResultInfoList = []  #所有比赛的list
            gameTables = soup.find_all("table") # 赛事名称
            #gameName = self.utilCutGameName(game1sth4.contents[0])
            #print gameName

            iIndex = 0
            gameData = {} # 单个比赛的数据
            gameOnDayDataList = [] #单个比赛的每轮列表
            gameOnDataData = {}
            for tableTemp in gameTables:
                # 判断前一个tag是否是H4，如果是则切换比赛，如果是table则继续记录当前比赛
                preTag = self.utilGetPreNotNoneTag(tableTemp)
                if preTag.name == "h4": # 新的比赛数据
                    #print "new" + preTag.contents[0]
                    if iIndex != 0:
                        gameData["roundGameInfoList"] = gameOnDayDataList
                        gameData['gameEndDate'] = gameOnDayDataList[0]["gameDate"]
                        gameData["gameStartDate"] = gameOnDayDataList[len(gameOnDayDataList) - 1]["gameDate"]
                        wholeResultInfoList.append(copy.deepcopy(gameData))  # 将比赛数据插入列表

                    # 初始化数据结构
                    gameData = {}
                    gameOnDayDataList = []  # 单个比赛的每轮列表
                    gameOnDataData = {}
                    gameData["fifgId"] = fifgId
                    gameData["gameName"] = self.utilCutGameName(preTag.contents[0])  # 存赛事名称
                    gameData["gameId"] = "" # TODO  存赛事编号
                    gameData["gameCourse"] = tableTemp.h4.contents[0]  # 存球场名称
                    trs = tableTemp.tbody.find_all("tr")
                    tds = trs[1].find_all("td")
                    gameData["par1"] = tds[0].string
                    gameData["par2"] = tds[1].string
                    gameData["par3"] = tds[2].string
                    gameData["par4"] = tds[3].string
                    gameData["par5"] = tds[4].string
                    gameData["par6"] = tds[5].string
                    gameData["par7"] = tds[6].string
                    gameData["par8"] = tds[7].string
                    gameData["par9"] = tds[8].string
                    gameData["par10"] = tds[9].string
                    gameData["par11"] = tds[10].string
                    gameData["par12"] = tds[11].string
                    gameData["par13"] = tds[12].string
                    gameData["par14"] = tds[13].string
                    gameData["par15"] = tds[14].string
                    gameData["par16"] = tds[15].string
                    gameData["par17"] = tds[16].string
                    gameData["par18"] = tds[17].string

                elif preTag.name == "table": # 同一赛事的不同轮次
                    # print "old"
                    pass
                else:
                    print "error"
                # 存放比赛信息
                trss = tableTemp.tbody.find_all("tr")
                tdss = trss[2].find_all("td")

                iIndex += 1


                if tdss[0].string.strip() == "" or tdss[0].string.strip() == "&nbsp":
                    continue

                gameDate = tableTemp.thead.td.contents[1].replace('(',"").replace(')',"").strip()
                gameDateTemp = time.strptime(gameDate,"%d-%m-%Y")
                gameOnDataData["gameDate"] = time.strftime("%Y-%m-%d",gameDateTemp)  # 存比赛日期
                gameOnDataData["hole1"] = tdss[0].string
                gameOnDataData["hole2"] = tdss[1].string
                gameOnDataData["hole3"] = tdss[2].string
                gameOnDataData["hole4"] = tdss[3].string
                gameOnDataData["hole5"] = tdss[4].string
                gameOnDataData["hole6"] = tdss[5].string
                gameOnDataData["hole7"] = tdss[6].string
                gameOnDataData["hole8"] = tdss[7].string
                gameOnDataData["hole9"] = tdss[8].string
                gameOnDataData["hole10"] = tdss[9].string
                gameOnDataData["hole11"] = tdss[10].string
                gameOnDataData["hole12"] = tdss[11].string
                gameOnDataData["hole13"] = tdss[12].string
                gameOnDataData["hole14"] = tdss[13].string
                gameOnDataData["hole15"] = tdss[14].string
                gameOnDataData["hole16"] = tdss[15].string
                gameOnDataData["hole17"] = tdss[16].string
                gameOnDataData["hole18"] = tdss[17].string
                gameOnDayDataList.append(copy.copy(gameOnDataData))

            print wholeResultInfoList



            result["result"] = 0
            result["gamePlayerWholeResultInfo"] = wholeResultInfoList
            #print result
            print "球员%s列表获取成功。" % fifgId
            return result
        except Exception, Argment:
            print "赛事结果列表获取失败-error:" + str(Argment)
            result['result'] = -1
            return result
    def utilCutGameName(self, text):
        cutIndex = text.index('-  Type')
        gameName = text[0:cutIndex]
        return gameName
    def utilGetPreNotNoneTag(self,content):
        temp = copy.deepcopy(content)
        iIndex = 0
        while iIndex < 50:
            if temp.previous_sibling == None or temp.previous_sibling == "":
                continue
            if temp.previous_sibling.name == "h4" or temp.previous_sibling.name == "table":
                return temp.previous_sibling
            temp = temp.previous_sibling
        return None




# test
#print FIFGGameInfo().parseGameRankInfo("")


#content = open("/Users/lynn/程序开发/python/data/popup1.html", 'r')  # TODO 替换
#FIFGGameInfo().parseGamePlayerWholeResult(content,"4943")
