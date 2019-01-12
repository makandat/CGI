#!/usr/bin/env python3
#  クレジットカード管理
import WebPage
import MySQL, Text
from syslog import syslog


class MyPage(WebPage.WebPage) :

  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL.MySQL()
    try :
      self.vars['result'] = ""
      if 'span' in self.params :
        # 期間指定がある場合
        span = self.params['span'].value
        parts = Text.split('-', span)
        span_from = "20" + parts[0] 
        span_to = "20" + parts[1]
        self.vars['result'] = self.getResult(span_from, span_to)
        self.vars['sum'] = Text.format("この期間の支払総額 {0}円", Text.money(self.getSum(span_from, span_to)))
      else :
        # 期間指定がない場合
        span = ""
        self.vars['result'] = self.getResult()
        self.vars['sum'] = Text.format("この期間の支払総額 {0}円", Text.money(self.getSum()))
      self.vars['message'] = f"クエリー OK ({span})" if len(span) > 0 else "クエリー OK"
    except Exception as e:
      self.vars['message'] = "エラー " + str(e)

  # 一覧を得る。
  def getResult(self, span_from = '200001', span_to='210001') :
    s1 = span_from[0:4] + "-" + span_from[4:6] + "-01"
    s2 = span_to[0:4] + "-" + span_to[4:6] + "-01"
    sql = f"SELECT `date`, FORMAT(payment, 0) as pay, info FROM smbcvisa WHERE `date` >= '{s1}' AND `date` < '{s2}'";
    rows = self.__mysql.query(sql)
    buff = ""
    for row in rows :
      buff += WebPage.WebPage.table_row(row)
    return buff

  # 期間の総支払額を計算する。
  def getSum(self, span_from = '200001', span_to='210001') :
    s1 = span_from[0:4] + "-" + span_from[4:6] + "-01"
    s2 = span_to[0:4] + "-" + span_to[4:6] + "-01"
    sql = f"SELECT SUM(payment) AS Summation FROM smbcvisa WHERE `date` >= '{s1}' AND `date` < '{s2}'";
    s = self.__mysql.getValue(sql)
    return s

# 応答を返す。
wp = MyPage('templates/index.html')
wp.echo()
