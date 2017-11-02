#coding:UTF-8
from apscheduler.schedulers.blocking import BlockingScheduler
from saveFootgolfInfo import SaveInfoData
from saveGameInfo import SaveGameInfoData

def myJob():
    print "start update ranking info."
    SaveInfoData().saveFootgolfRankData()
def updateGameInfoJob():
    print "start update game info."
    SaveGameInfoData().saveFootgolfGamesData()

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', day_of_week='mon-sun', hour='3', minute="1", second="*/60")
    sched.add_job(updateGameInfoJob, 'cron', day_of_week='sun', hour='4', minute="1", second="*/60")
    sched.start()