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
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
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
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            print "error:" + Argment
            return Argment
