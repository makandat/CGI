#!/usr/bin/env python3
#  YJFX 資産グラフ
import WebPage as page
import Text, MySQL


SELECT = "SELECT id, (asset+profit_loss) as eval_asset FROM YJFX_Asset"
SELECT2 = "SELECT min(`date`) AS `begin`, max(`date`) AS `end` FROM YJFX_Asset"


# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    rows = self.__mysql.query(SELECT)
    self.vars['data'] = self.getHtml(rows)
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
    self.vars['begin'] = rows[0][0]
    self.vars['end'] = rows[0][1]
    return

# メイン開始位置
wp = MainPage('templates/asset_plot.html')
wp.echo()
