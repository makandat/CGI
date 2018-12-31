# -*- code=utf-8 -*-
# Version 0.51  2018-09-15
import datetime as dt
import time

# 日付時刻クラス
class DateTime :
    # コンストラクタ
    def __init__(self, s="") :
        if s == "" :
            self.__dtime = dt.datetime.now()
        else :
            self.__dtime = dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        self.__jst = dt.timezone(dt.timedelta(hours=+9), 'JST')

    @property
    def timestamp(self) :
        return self.__dtime.timestamp().real

    # 現在の日時
    @staticmethod
    def now() :
        jst = dt.timezone(dt.timedelta(hours=+9), 'JST')
        return dt.datetime.now(jst)

    @staticmethod
    def utc() :
        return dt.datetime.utcnow()

    # 現在のオブジェクトの文字列表現を返す。
    def toString(self, f="") :
        if f == "":
            return self.__dtime.strftime("%Y-%m-%d %H:%M:%S")
        else :
            return self.__dtime.strftime(f)

    # 現在のオブジェクトの日付部分を文字列として返す。
    def toDateString(self, f="") :
        if f == "" :
            return self.__dtime.strftime("%Y-%m-%d")
        else :
            return self.__dtime.strftime(f)

    # 現在のオブジェクトの時刻部分を文字列として返す。
    def toTimeString(self, f="") :
        if f == "" :
            return self.__dtime.strftime("%H-%M-%S")
        else :
            return self.__dtime.strftime(f)

    # 日付部分と時刻部分
    @property
    def year(self) :
        return self.__dtime.year

    @property
    def month(self) :
        return self.__dtime.month

    @property
    def day(self) :
        return self.__dtime.day

    @property
    def hour(self) :
        return self.__dtime.hour

    @property
    def minute(self) :
        return self.__dtime.minute

    @property
    def second(self) :
        return self.__dtime.second
    
    @property
    def dayOfweek(self) :
        return self.__dtime.weekday()
    
    # 演算
    def addWeeks(self, weeks) :
        self.__dtime += dt.timedelta(weeks=weeks)

    def addDays(self, days) :
        self.__dtime += dt.timedelta(days=days)

    def addHours(self, hours) :
        self.__dtime += dt.timedelta(hours=hours)

    def addMinutes(self, minutes) :
        self.__dtime += dt.timedelta(minutes=minutes)

    def addSeconds(self, seconds) :
        self.__dtime += dt.timedelta(seconds=seconds)


