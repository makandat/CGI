#!/usr/bin/env python3
#  クレジットカード管理 データ入力
import WebPage
import MySQL, Text

SELECT = "SELECT `date`, payment FROM smbcvisa WHERE `date` LIKE '{0}-%' ORDER BY `date`"

class ChartPage(WebPage.WebPage) :
  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL.MySQL()
    if 'year' in self.params :
      # 表示指定があるとき
      year = self.params['year'].value
      sql = Text.format(SELECT, year)
      rows = self.__mysql.query(sql)
      self.vars['data'] = self.getData(rows)
      self.vars['message'] = f"{year}年のグラフ"
    else :
      self.vars['data'] = ""
      self.vars['message'] = ""
    return

  # データを作成する。
  def getData(self, rows) :
    data = "[["
    sum = 0
    for row in rows :
      month = row[0][5:7]
      data += "["
      data += month
      data += ","
      data += str(row[1]/100)
      sum += int(row[1])
      data += "],"
    result = data[0:len(data)-1]
    result += "]]"
    self.vars['average'] = Text.money(round(sum / len(rows)))
    return result

# 応答を返す。
wp = ChartPage('templates/chart.html')
wp.echo()
