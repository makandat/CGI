#!/usr/bin/env python3
#  クレジットカード管理 データ入力
from WebPage import WebPage
from MySQL import MySQL
import Text

SELECT = "SELECT `date`, payment FROM smbcvisa WHERE `date` LIKE '{0}-%' ORDER BY `date`"

class ChartPage(WebPage) :
  # コンストラクタ
  def __init__(self, tepmlate) :
    super().__init__(tepmlate)
    self.__mysql = MySQL()
    if 'year' in self.params :
      # 表示指定があるとき
      year = self.getParam('year')
      sql = Text.format(SELECT, year)
      rows = self.__mysql.query(sql)
      self.setPlaceHolder('data', self.getData(rows))
      self.setPlaceHolder('message', f"{year}年のグラフ")
    else :
      self.setPlaceHolder('data', "")
      self.setPlaceHolder('message', "")
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
    self.setPlaceHolder('average', Text.money(round(sum / len(rows))))
    return result

# 応答を返す。
wp = ChartPage('templates/chart.html')
wp.echo()
