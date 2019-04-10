#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS admin.cgi  Version 2.00
import WebPage as web
import MySQL
import Text
import Common
from syslog import syslog


# CGI WebPage クラス
class MainPage(web.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.schema = self.conf['db']
    if self.isParam('submit') :
      sql = self.getParam('sql')
      if sql == "" :
        self.setPlaceHolder('message', 'SQL が空欄です。')
      else :
        self.execSQL(sql)
    else :
      self.setPlaceHolder('message', '')
    return

  # SQL を実行する。
  def execSQL(self, sql) :
    try :
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', 'SQL を実行しました。')
    except Exception as e :
      self.setPlaceHolder('message', 'Error: ' + str(e))    
    return

# メイン開始位置
wp = MainPage('templates/admin.html')
wp.echo()
