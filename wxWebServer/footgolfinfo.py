#coding:UTF-8
# filename: footgolfinfo.py
import MySQLdb
from utility.configInfo import ConfigInfo

class FootgolferInfo(object):
    def getRankInfoByName(self,playerName):
        conf = ConfigInfo("conf/footgolf.ini")
        dbInfo = conf.getDBInfo()
        conn = MySQLdb.connect(host=str(dbInfo['host']), port=int(dbInfo['port']), user=str(dbInfo['user']),
                               passwd=str(dbInfo['pwd']), db=str(dbInfo['dbname']), charset='utf8')
        playerName = playerName.lower().replace('，', ',').replace(',','').replace(' ','').replace(' ','')
        print playerName
        queryRankSql = "select fr.name,fr.chinaname,fr.fifgmember,fr.rank,fr.point,fr.updatetime from footgolfer_rank fr where replace(replace(fr.name,',',''),' ','') like '%s%s%s';" % ('%',playerName,'%')
        print queryRankSql
        try:
            cur = conn.cursor()

            tempData = cur.execute(queryRankSql)
            dataSet = cur.fetchmany(tempData)
            infoList = []
            count = 0
            resultTxt = ""
            for i in dataSet:
                temp = "排:" + str(i[3]) + " 名:" + str(i[0]) + " 分:" + str(i[4])
                print temp
                infoList.append(temp)
                resultTxt += "\n" + temp
                count += 1
                if count >= 3 :
                    infoList.append("匹配记录过多，请精确查询条件。")
                    resultTxt += "\n" + "匹配记录过多，请精确查询条件。"
                    break;
            # print infoList[0]
            if count <= 0:
                resultTxt += "\n" + "未找到数据，请核实姓名。\n1.人名搜索:可输入姓名全拼进行搜索。如:wanglin \n2.特殊搜索:可以输入【中国】查询中国排名前30位的选手。目前仅支持中国。\n特殊搜索：可以输入【2017轻井泽】查询2017日本轻井泽大师赛参赛高手。\n※排名信息暂时一周更新一次。\n如果有其他好的建议可以直接联系我。"
            return resultTxt
        except Exception, Argment:
            print "error:" + Argment
            return "服务器错误，请稍后再试。"
        finally:
            cur.close()
            conn.close()
            print "连接已关闭"

    def getRankInfoByCountry(self,playerName):
        conf = ConfigInfo("conf/footgolf.ini")
        dbInfo = conf.getDBInfo()
        conn = MySQLdb.connect(host=str(dbInfo['host']), port=int(dbInfo['port']), user=str(dbInfo['user']),
                               passwd=str(dbInfo['pwd']), db=str(dbInfo['dbname']), charset='utf8')
        playerName = playerName.lower().replace('，', ',')
        print playerName
        queryRankSql = "select fr.name,fr.chinaname,fr.fifgmember,fr.rank,fr.point,fr.updatetime from footgolfer_rank fr where fr.fifgmember = 'China FootGolf Association' order by fr.rank;"
        print queryRankSql
        try:
            cur = conn.cursor()

            tempData = cur.execute(queryRankSql)
            dataSet = cur.fetchmany(tempData)
            infoList = []
            count = 0
            resultTxt = "中国选手排名如下："
            for i in dataSet:
                temp = "中:" + str(count + 1) + " 世:" + str(i[3]) + " 名:" + str(i[0]) + " 分:" + str(i[4])
                print temp
                infoList.append(temp)
                resultTxt += "\n" + temp
                count += 1
                if count >= 30 :
                    infoList.append("匹配记录过多，请精确查询条件。")
                    resultTxt += "\n" + "记录过多，最多显示30条。"
                    break;
            # print infoList[0]
            if count <= 0:
                resultTxt += "\n" + "没有此国家数据，目前仅支持【中国】。"
            return resultTxt
        except Exception, Argment:
            print "error:" + Argment
            return "服务器错误，请稍后再试。"
        finally:
            cur.close()
            conn.close()
            print "连接已关闭"
    def getRankInfoByKaruizawa2017(self):
        conf = ConfigInfo("conf/footgolf.ini")
        dbInfo = conf.getDBInfo()
        conn = MySQLdb.connect(host=str(dbInfo['host']), port=int(dbInfo['port']), user=str(dbInfo['user']),
                               passwd=str(dbInfo['pwd']), db=str(dbInfo['dbname']), charset='utf8')
        queryRankSql = "select fr.name,fr.chinaname,fr.fifgmember,fr.rank,fr.point,fr.updatetime from footgolfer_rank fr,footgolfer_karuizawa2017 fk7 where fr.name = fk7.name order by fr.rank;"
        print queryRankSql
        try:
            cur = conn.cursor()

            tempData = cur.execute(queryRankSql)
            dataSet = cur.fetchmany(tempData)
            infoList = []
            count = 0
            resultTxt = "2017日本轻井泽大师赛参赛高手(不全，持续更新)："
            for i in dataSet:
                temp = " 世:" + str(i[3]) + " 名:" + str(i[0]) + " 分:" + str(i[4])
                print temp
                infoList.append(temp)
                resultTxt += "\n" + temp
                count += 1
                if count >= 30 :
                    infoList.append("匹配记录过多，请精确查询条件。")
                    resultTxt += "\n" + "记录过多，最多显示30条。"
                    break;
            # print infoList[0]
            if count <= 0:
                resultTxt += "\n" + "没有此比赛数据，目前仅支持【2017轻井泽】。"
            return resultTxt
        except Exception, Argment:
            print "error:" + Argment
            return "服务器错误，请稍后再试。"
        finally:
            cur.close()
            conn.close()
            print "连接已关闭"
    def getRankInfo(self, keyword):
        if keyword == "中国":
            return self.getRankInfoByCountry(keyword)
        elif keyword == "2017轻井泽" or keyword == "轻井泽":
            return self.getRankInfoByKaruizawa2017()
        else:
            return self.getRankInfoByName(keyword)

fi = FootgolferInfo()
fi.getRankInfo("轻井泽")