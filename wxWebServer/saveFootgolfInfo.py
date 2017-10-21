#coding:UTF-8
#encoding=utf-8
from utility.mysqlaccess import MysqlAccessBase
from FIFGInfoCrawler.HTMLFromUrl import HTMLInfo
from FIFGInfoCrawler.fifgRankInfo import FIFGRankInfo
import datetime


class SaveInfoData(object):
    def deleteOldData(self, mysqlAccess, delParam):
        delBackInfo = "delete from footgolf_info.backup_footgolfer_rank where updatetime = %s;"
        mysqlAccess.update(delBackInfo,[delParam])
        print "旧数据已删除。"

    def copyDataToRankTable(self, mysqlAccess, updatedate):
        delRankInfoSql = "delete from footgolf_info.footgolfer_rank;"
        copySql = "insert into footgolf_info.footgolfer_rank select * from footgolf_info.backup_footgolfer_rank bfr " \
                  "where bfr.updatetime = %s;"
        mysqlAccess.update(delRankInfoSql, None)
        mysqlAccess.update(copySql, [updatedate])
        print "数据更新到查询表，已经可用。"

    def saveFootgolfRankData(self):
        mysqlOb = MysqlAccessBase()
        try:
            htmlContext = HTMLInfo().getHtmlFromUrl("https://fgranks.com/fifg/worldtour?l=en")  # 获取页面html数据
            dataSet = FIFGRankInfo().parseRankHtmlData(htmlContext) # 解析html生成排名数据
            # print dataSet["result"]
            if int(dataSet["result"]) < 0:
                return "error"
            ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cdate = datetime.datetime.now().strftime("%Y-%m-%d")

            self.deleteOldData(mysqlOb,cdate)

            sql = "insert into footgolf_info.backup_footgolfer_rank (Name,ranking,score,updatetime,fifgorg,remark,create_time) " \
                  "values(%s,%s,%s,%s,%s,%s,%s);"
            print sql
            sqlParams = []
            for temp in dataSet["RankInfo"]:
                param = []
                param.append(temp["name"])
                param.append(int(temp["pos"]))
                param.append(float(temp["score"]))
                param.append(cdate)
                param.append(temp["association"])
                param.append(temp["sysId"])
                param.append(ctime)
                sqlParams.append(param)
            # print sqlParams
            mysqlOb.updateMany(sql,sqlParams) # 插入球员信息

            # 更新履历
            logSql = "insert into footgolf_info.footgolf_updatelog (updatetime,create_time) values (%s,%s);"
            mysqlOb.update(logSql,[cdate,ctime])

            self.copyDataToRankTable(mysqlOb, cdate)
            mysqlOb.commit()
            print "footgolf Rank Info update success."
        except Exception, Argment:
            mysqlOb.rollback()
            print "error:" + str(Argment)
            print "已回滚"
        finally:
            mysqlOb.close()
            print "DB连接关闭"


# test
# SaveInfoData().saveFootgolfRankData()