#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  YJFX 資産・取引管理
#    insert.cgi
from WebPage import WebPage
import Text
from MySQL import MySQL

INSERT = "INSERT INTO YJFX_Asset(`date`, asset, profit_loss) VALUES('{0}', {1}, {2})"
UPDATE = "UPDATE YJFX_Asset SET `date`='{1}', asset={2}, profit_loss={3} WHERE id = {0}"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    try :
      if self.isParam('date') :
        date = self.getParam('date')
        asset = self.getParam('asset')
        profit = self.getParam('profit')
        if self.isParam('id') :
          # id がある場合は修正
          id = self.getPara,('id')
          sql = Text.format(UPDATE, id, date, asset, profit)
        else :
          # id がない場合は追加
          sql = Text.format(INSERT, date, asset, profit)
        self.__mysql.execute(sql)
        self.setPlaceHolder('message', "クエリー OK " + self.getParam('date'))
      else :
        self.setPlaceHolder('message', "")
    except Exception as e :
      self.setPlaceHolder('message', "クエリー NG " + str(e))
    return

# メイン開始位置
wp = MainPage('templates/insert.html')
wp.echo()

