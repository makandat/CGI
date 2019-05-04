#!/usr/bin/env python3
#  YJFX 資産グラフ
from WebPage import WebPage
from MySQL import MySQL
import Text


SELECT = "SELECT id, (asset+profit_loss) as eval_asset FROM YJFX_Asset"
SELECT2 = "SELECT min(`date`) AS `begin`, max(`date`) AS `end` FROM YJFX_Asset"


# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = MySQL()
    rows = self.__mysql.query(SELECT)
    self.setPlaceHolder('data', self.getHtml(rows))
    self.getInterval()
    return

  # グラフデータを作成する。
  def getHtml(self, rows) :
    buff = "[["
    for row in rows :
      id = row[0]
      eval_asset = row[1]/1000
      buff += f"[{id}, {eval_asset}],"
    buff = buff[0:len(buff)-1]
    buff += "]]"
    return buff

  # 期間を求める。
  def getInterval(self) :
    rows = self.__mysql.query(SELECT2)
    self.setPlaceHolder('begin', rows[0][0])
    self.setPlaceHolder('end', rows[0][1])
    return

# メイン開始位置
wp = MainPage('templates/asset_plot.html')
wp.echo()
