#coding:UTF-8
#encoding=utf-8
from utility.mysqlaccess import MysqlAccessBase
from FIFGInfoCrawler.HTMLFromUrl import HTMLInfo
from FIFGInfoCrawler.fifgGameInfo import FIFGGameInfo
from utility.numStr import NumStrUtil
import datetime


class SaveGameInfoData(object):
    def deleteOldData(self, mysqlAccess):
        delGameInfoSql = "delete from footgolf_info.footgolf_gameInfo;"
        mysqlAccess.update(delGameInfoSql,None)
        delGameResultInfoSql = "delete from footgolf_info.footgolf_gameResultInfo;"
        mysqlAccess.update(delGameResultInfoSql, None)
        print "旧赛事数据已删除。"

    def saveFootgolfGamesData(self):
        mysqlOb = MysqlAccessBase()
        try:
            fifgGameInfo = FIFGGameInfo()
            numStr = NumStrUtil()
            htmlContext = HTMLInfo().getHtmlFromUrl("https://fgranks.com/fifg/worldtour?l=en")  # 获取页面html数据
            dataSet = fifgGameInfo.parseGameListHtmlData(htmlContext) # 解析html生成排名数据

            if int(dataSet["result"]) < 0:
                raise Exception("game list get error.")
            ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d")

            self.deleteOldData(mysqlOb)

            gameInfoSql = "insert into footgolf_info.footgolf_gameInfo " \
                          "(game_id,game_name,game_level,game_link,updatetime,create_time) values " \
                          "(%s,%s,%s,%s,%s,%s);"
            gameResultInfoSql = "insert into footgolf_info.footgolf_gameResultInfo " \
                                "(game_id,fifg_id,player_name,pos,round_count,round1,round2," \
                                "round3,round4,round5,topar,total,updatetime,create_time) " \
                                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            sqlGameInfoParams = []
            gameResultParams = []
            index = 0
            for temp in dataSet["gameInfo"]:
                index += 1
                param = []
                gameId = "game" + str(index)
                param.append(gameId)   # game id
                param.append(temp["gameName"])  # game name
                param.append(temp["gameLevel"])   # game level
                param.append(temp["gamePageLink"])   #game page link
                param.append(cdate)
                param.append(ctime)
                sqlGameInfoParams.append(param)

                # get game reslut info data
                gameRankContext = HTMLInfo().getHtmlFromUrl(str(temp["gamePageLink"]))

                gameResultData = fifgGameInfo.parseGameRankInfo(gameRankContext)
                if int(gameResultData["result"]) < 0:
                    raise Exception("game result data get error.")
                for resultTemp in gameResultData["gameResultInfo"]:
                    unitParam = []
                    unitParam.append(gameId)
                    unitParam.append(resultTemp["fifgId"])
                    unitParam.append(resultTemp["name"])
                    unitParam.append(resultTemp["pos"])
                    roundCount = int(resultTemp["roundCount"])
                    unitParam.append(str(roundCount))
                    for roundIdx in range(1,6):
                        if roundIdx <= roundCount: # 该比赛轮次内
                            unitParam.append(numStr.convertToInt(resultTemp["round" + str(roundIdx)],None))
                        else:
                            unitParam.append(None)
                    unitParam.append(numStr.convertToInt(resultTemp["topar"],None))
                    unitParam.append(numStr.convertToInt(resultTemp["total"],None))
                    unitParam.append(cdate)
                    unitParam.append(ctime)
                    gameResultParams.append(unitParam)

            # print sqlParams
            mysqlOb.updateMany(gameInfoSql, sqlGameInfoParams) # 插入球员信息
            mysqlOb.updateMany(gameResultInfoSql,gameResultParams)




            mysqlOb.commit()
            print "footgolf game Info update success."
        except Exception, Argment:
            mysqlOb.rollback()
            print "game info update error:" + str(Argment)
            print "已回滚"
        finally:
            mysqlOb.close()
            print "DB连接关闭"


# test
#SaveInfoData().saveFootgolfGamesData()