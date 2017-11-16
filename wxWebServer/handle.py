# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import footgolfinfo
import usermsglog
import web

class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and (recMsg.MsgType == 'text' or recMsg.MsgType == "voice"):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                print "get footgolfinfo start"
                fgInfo = footgolfinfo.FootgolferInfo()
                print "footgolfinfo instance success."
                content = fgInfo.getRankInfo(recMsg.Content)
                print "get footgolfinfo end " + content
                umlog = usermsglog.UserMsg()
                umlog.recordUserTxtMsgLog(recMsg.MsgId,recMsg.FromUserName,recMsg.CreateTime,recMsg.MsgType,recMsg.Content)
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif isinstance(recMsg, receive.Msg) and (recMsg.MsgType == 'event'):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                event = recMsg.Event
                print "event:" + event
                welcomeMsg = "欢迎加入足球高尔夫公众号，下面为排名查询功能介绍：\n"\
                             "1.人名搜索:可输入姓名全拼进行搜索。如:wanglin \n" \
                             "2.特殊搜索:可以输入【中国】查询中国排名前30位的选手。目前仅支持中国。可语音输入。\n" \
                             "※排名信息每日更新。\n如果有其他好的建议可以直接在公众号回复。"
                if event == 'subscribe': # 关注
                    replyMsg = reply.TextMsg(toUser,fromUser,welcomeMsg)
                    return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            print "error:" + Argment
            return Argment
