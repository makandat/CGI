#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS admin.cgi  Version 2.00
import WebPage as web
import MySQL
from syslog import syslog


# CGI WebPage クラス
class MainPage(web.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    self.schema = self.conf['db']
    # Postback か?
    if self.isParam('submit') :
      # 履歴を取るか?
      if self.isParam('history') :
        self.history = True if self.getParam('history') == 'history' else False
        if self.history :
          self.setCookie('history1', '1')
          self.setPlaceHolder('history', 'checked')
        else :
          self.setCookie('history1', '0')
          self.setPlaceHolder('history', '')
      else :
        self.history = False
        self.setCookie('history1', '0')
        self.setPlaceHolder('history', '')
      # SQL を取得し空欄かチェックする。
      sql = self.getParam('sql')
      if sql == "" :
        self.setPlaceHolder('message', 'SQL が空欄です。')
      else :
        self.execSQL(sql)
    else :
      self.setPlaceHolder('message', '')
      # 履歴クッキーがあるか?
      if self.isCookie('history1') :
        # 履歴クッキーあり
        if self.getCookie('history1') == '0' :
          # 履歴を取らない
          self.setPlaceHolder('history', '')
        else :
          # 履歴を取る
          self.setPlaceHolder('history', 'checked')
      else :
        # 履歴クッキーなし
        self.setPlaceHolder('history', '')
    return

  # SQL を実行する。
  def execSQL(self, sql) :
    try :
      sql = sql.replace("'", "''")
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', 'SQL を実行しました。')
      self.saveHistory(sql)
    except Exception as e :
      self.setPlaceHolder('message', 'Error: ' + str(e))    
    return

  # 履歴を保存する。
  def saveHistory(self, sql) :
    if self.history :
      # 履歴を History テーブルに書く。
      sql = sql.replace("'", "''").replace("'", "''")
      # 登録する。
      info = self.getParam('info')
      insert = f"INSERT INTO History(dtime,caption,content,application,tag,info) VALUES(cast(now() as datetime),'Query', '{sql}', 'MySQL-IS python3', '1', '{info}')"
      syslog(insert)
      self.__mysql.execute(insert)
    else :
      pass
    return

# メイン開始位置
wp = MainPage('templates/admin.html')
wp.echo()
