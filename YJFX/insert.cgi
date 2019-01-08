#!/usr/bin/env python3
#  YJFX 資産・取引管理

import WebPage as page
import Text
import MySQL

INSERT = "INSERT INTO YJFX_Asset(`date`, asset, profit_loss) VALUES('{0}', {1}, {2})"
UPDATE = "UPDATE YJFX_Asset SET `date`='{1}', asset={2}, profit_loss={3} WHERE id = {0}"

# CGI WebPage クラス
class MainPage(page.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    try :
      if 'date' in self.params :
        date = self.params['date'].value
        asset = self.params['asset'].value
        profit = self.params['profit'].value
        if 'id' in self.params :
          # id がある場合は修正
          id = self.params['id'].value
          sql = Text.format(UPDATE, id, date, asset, profit)
        else :
          # id がない場合は追加
          sql = Text.format(INSERT, date, asset, profit)
        self.__mysql.execute(sql)
        self.vars['message'] = "クエリー OK " + self.params['date'].value
      else :
        self.vars['message'] = ""
    except Exception as e :
      self.vars['message'] = "クエリー NG " + str(e)
    return

# メイン開始位置
wp = MainPage('templates/insert.html')
wp.echo()

