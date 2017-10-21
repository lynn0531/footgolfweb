#coding:UTF-8
# filename: footgolfinfo.py
from utility.mysqlaccess import MysqlAccessBase
import abc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class footgolfInfoBase(): #abstract class
    __metaclass__ = abc.ABCMeta
    def process(self, keyWord):
        mysqlAccess = MysqlAccessBase()
        try:
            querySql = self.getQuerySql(keyWord)
            print querySql
            sqlParam = self.getSqlParam(keyWord)
            print "sql param:" + str(sqlParam)
            queryData = mysqlAccess.query(querySql,sqlParam)
            resultTxt = self.getOutputData(queryData)
            print resultTxt
            return resultTxt
        except Exception, Argment:
            print "error:" + str(Argment)
            return "error"
        finally:
            mysqlAccess.close()
            print "连接已关闭"

    def getSqlParam(self, keyWord):
        return None

    @abc.abstractmethod
    def getQuerySql(self, keyWord):
        pass

    @abc.abstractmethod
    def getOutputData(self, dataSet):
        pass

class FootgolferInfoByName(footgolfInfoBase):
    def getQuerySql(self, keyWord):
        #playerName = keyWord.lower().replace('，', ',').replace(',', '').replace(' ', '').replace(' ', '')
        #print playerName
        queryRankSql = "select fr.name,fr.chinaname,fr.fifgOrg,fr.ranking,fr.score,fr.updatetime from footgolfer_rank fr where replace(replace(fr.name,',',''),' ','') like %s order by fr.ranking;"
        return queryRankSql
    def getOutputData(self, dataSet):
        infoList = []
        count = 0
        resultTxt = ""
        if len(dataSet) > 0: #有数据 显示数据更新时间
            resultTxt += "数据更新时间：" + str(dataSet[0][5])
        for i in dataSet:
            temp = "排:" + str(i[3]) + " 名:" + str(i[0]) + " 分:" + str(i[4])
            print temp
            infoList.append(temp)
            resultTxt += "\n" + temp
            count += 1
            if count >= 10:
                infoList.append("匹配记录过多，请精确查询条件。")
                resultTxt += "\n" + "匹配记录过多，请精确查询条件。"
                break;
        if count <= 0:
            resultTxt += "\n" + "未找到数据，请核实姓名。\n1.人名搜索:可输入姓名全拼进行搜索。如:wanglin \n2.特殊搜索:可以输入【中国】查询中国排名前30位的选手。目前仅支持中国。\n特殊搜索：可以输入【2017轻井泽】查询2017日本轻井泽大师赛参赛高手。\n※排名信息暂时一周更新一次。\n如果有其他好的建议可以直接联系我。"
        return resultTxt
    def getSqlParam(self, keyWord):
        return ["%" + keyWord.lower().replace('，', ',').replace(',', '').replace(' ', '').replace(' ', '') + "%"]

class FootgolferInfoByCountry(footgolfInfoBase):
    def getQuerySql(self, keyWord):
        queryRankSql = "select fr.name,fr.chinaname,fr.fifgOrg,fr.ranking,fr.score,fr.updatetime from footgolfer_rank fr where fr.fifgOrg = 'China FootGolf Association' order by fr.ranking;"
        return queryRankSql
    def getOutputData(self, dataSet):
        infoList = []
        count = 0
        resultTxt = ""
        if len(dataSet) > 0: #有数据 显示数据更新时间
            resultTxt += "数据更新时间：" + str(dataSet[0][5])
        resultTxt += "\n中国选手排名如下："
        for i in dataSet:
            temp = "中:" + str(count + 1) + " 世:" + str(i[3]) + " 名:" + str(i[0]) + " 分:" + str(i[4])
            print temp
            infoList.append(temp)
            resultTxt += "\n" + temp
            count += 1
            if count >= 30:
                infoList.append("匹配记录过多，请精确查询条件。")
                resultTxt += "\n" + "记录过多，最多显示30条。"
                break;
        if count <= 0:
            resultTxt += "\n" + "没有此国家数据，目前仅支持【中国】。"
        return resultTxt

class FootgolferInfoByGame(footgolfInfoBase):
    def getQuerySql(self, keyWord):
        queryRankSql =  "select fr.name,fr.chinaname,fr.fifgOrg,fr.ranking,fr.score,fr.updatetime from footgolfer_rank fr,footgolfer_karuizawa2017 fk7 where fr.name = fk7.name order by fr.ranking;"
        return queryRankSql
    def getOutputData(self, dataSet):
        infoList = []
        count = 0
        resultTxt = "2017日本轻井泽大师赛参赛高手(不全，持续更新)："
        for i in dataSet:
            temp = " 世:" + str(i[3]) + " 名:" + str(i[0]) + " 分:" + str(i[4])
            print temp
            infoList.append(temp)
            resultTxt += "\n" + temp
            count += 1
            if count >= 30:
                infoList.append("匹配记录过多，请精确查询条件。")
                resultTxt += "\n" + "记录过多，最多显示30条。"
                break;
        if count <= 0:
            resultTxt += "\n" + "没有此比赛数据，目前仅支持【2017轻井泽】。"
        return resultTxt

class FootgolferInfo(object):
    def getRankInfo(self, keyword):
        info = None
        if keyword == "中国":
            info = FootgolferInfoByCountry()
        elif keyword == "2017轻井泽" or keyword == "轻井泽":
            info = FootgolferInfoByGame()
        else:
            info = FootgolferInfoByName()
        result = info.process(keyword)
        return result

# test
#fi = FootgolferInfo()
#fi.getRankInfo("中国")
