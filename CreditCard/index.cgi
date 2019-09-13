#!/usr/bin/env python3
#  クレジットカード管理  v1.01 2019-09-13
from WebPage import WebPage
from MySQL import MySQL
import Text
#from syslog import syslog


class MyPage(WebPage) :

  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL()
    try :
      self.embed({"result":"", "card":"SMBC VISA", "sum":""})
      if self.isParam('span') :
        # 期間指定がある場合
        span = self.getParam('span')
        parts = Text.split('-', span)
        span_from = "20" + parts[0] 
        span_to = "20" + parts[1]
        s = self.getResult(span_from, span_to)
        if s == None :
          self.setPlaceHolder('result', "")
        else :
          self.setPlaceHolder('result', self.getResult(span_from, span_to))
        self.setPlaceHolder('sum', Text.format("この期間の支払総額 {0}円", Text.money(self.getSum(span_from, span_to))))
      else :
        # 期間指定がない場合
        span = ""
        s = self.getResult()
        if s == None :
          self.setPlaceHolder('result', "")
        else :
          self.setPlaceHolder('result', self.getResult())
        self.setPlaceHolder('sum', Text.format("この期間の支払総額 {0}円", Text.money(self.getSum())))
      self.setPlaceHolder('message', f"クエリー OK ({span})" if len(span) > 0 else "クエリー OK")
    except Exception as e:
      self.setPlaceHolder('message', "エラー " + str(e))

  # 一覧を得る。
  def getResult(self, span_from = '200001', span_to='210001') :
    s1 = span_from[0:4] + "-" + span_from[4:6] + "-01"
    s2 = span_to[0:4] + "-" + span_to[4:6] + "-31"
    sql = f"SELECT `date`, FORMAT(payment, 0) as pay, info FROM smbcvisa WHERE `date` >= '{s1}' AND `date` < '{s2}'";
    rows = self.__mysql.query(sql)
    buff = ""
    if len(rows) == 0 :
      return None
    for row in rows :
      buff += WebPage.table_row(row)
    return buff

  # 期間の総支払額を計算する。
  def getSum(self, span_from = '200001', span_to='210001') :
    n = self.__mysql.getValue("SELECT count(*) FROM smbcvisa")
    if n == 0 :
      return 0
    s1 = span_from[0:4] + "-" + span_from[4:6] + "-01"
    s2 = span_to[0:4] + "-" + span_to[4:6] + "-01"
    sql = f"SELECT SUM(payment) AS Summation FROM smbcvisa WHERE `date` >= '{s1}' AND `date` < '{s2}'";
    s = self.__mysql.getValue(sql)
    return s

# 応答を返す。
wp = MyPage('templates/index.html')
wp.echo()
