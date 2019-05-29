#!/usr/bin/env python3
#!C:\Program Files (x86)\Python37\python.exe
#  YJFX 資産・取引管理
#    insert.cgi
from WebPage import WebPage
import Text
import Common
from MySQL import MySQL

INSERT = "INSERT INTO YJFX_Asset(`date`, asset, profit_loss) VALUES('{0}', {1}, {2})"
UPDATE = "UPDATE YJFX_Asset SET `date`='{1}', asset={2}, profit_loss={3} WHERE id = {0}"
SELECT = "SELECT * FROM YJFX_Asset WHERE id = {0}"

# CGI WebPage クラス
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    Common.init_logger("C:/temp/Logger.log")
    self.__mysql = MySQL()
    try :
      if self.isParam('insert') :
        Common.log("insert/update")
        # 挿入または修正の時
        date = self.getParam('date')
        if date == "" :
          self.setPlaceHolder('message', "日付が空欄です。")
          return
        asset = self.getParam('asset').replace(",", "")
        if asset == "" :
          self.setPlaceHolder('message', "資産が空欄です。")
          return
        profit = self.getParam('profit').replace(",", "")
        if profit == "" :
          self.setPlaceHolder('message', "損益が空欄です。")
          return
        if self.isParam('id') :
          # id がある場合は修正
          id = self.getParam('id')
          sql = Text.format(UPDATE, id, date, asset, profit)
        else :
          # id がない場合は追加
          sql = Text.format(INSERT, date, asset, profit)
        self.__mysql.execute(sql)
        self.setPlaceHolder('message', "クエリー OK " + self.getParam('date'))
        self.clearForm()
      elif self.isParam('confirm') :
        Common.log("confirm")
        # データ確認の時
        id = self.getParam('id')
        if id == "" :
          self.setPlaceHolder('message', "id が空欄です。")
          return
        sql = Text.format(SELECT, id)
        rows = self.__mysql.query(sql)
        if len(rows) == 0 :
          self.setPlaceHolder('message', "id が正しくありません。")
          return
        row = rows[0]
        date = row[1]
        asset = row[2]
        profit = row[3]
        self.setPlaceHolder('id', id)
        self.setPlaceHolder('date', date)
        self.setPlaceHolder('asset', asset)
        self.setPlaceHolder('profit', profit)
        self.setPlaceHolder('message', "")
      else :
        Common.log("undefined")
        self.setPlaceHolder('message', "")
        self.clearForm()
    except Exception as e :
      self.setPlaceHolder('message', "クエリー NG " + str(e))
      self.clearForm()
    return

  # フォームをクリアする。
  def clearForm(self) :
    self.embed({'id':'', 'date':'', 'asset':'', 'profit':''})
    return

# メイン開始位置
wp = MainPage('templates/insert.html')
wp.echo()

