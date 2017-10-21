#coding:UTF-8
from apscheduler.schedulers.blocking import BlockingScheduler
from saveFootgolfInfo import SaveInfoData

def myJob():
    print "start."
    SaveInfoData().saveFootgolfRankData()

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', day_of_week='mon-sun', hour='3', minute="1", second="*/60")
    sched.start()