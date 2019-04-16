#!C:\Program Files (x86)\Python37\python.exe
#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS query.cgi  Version 2.01
import WebPage as web
import MySQL
#from syslog import syslog

# CGI WebPage クラス
class MainPage(web.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    # ユーザとスキーマを表示
    self.setPlaceHolder('userid', self.conf['uid'])
    self.setPlaceHolder('schema', self.conf['db'])
    # Postback かどうか?
    if self.isParam("submit") :
      # Postback なら SQL を実行する。
      self.execSql()
      # 履歴が有効か?
      if self.isParam('history') :
        if self.getParam('history') == 'history':
          # 履歴を取る。
          self.history = True
          self.setPlaceHolder('history', 'checked')
          self.setCookie('history', '1')
        else :
          # 履歴を取らない。
          self.history = False
          self.setPlaceHolder('history', '')
          self.setCookie('history', '0')
      if self.history :
        # 履歴を取るとき、クッキーを'1'にする。
        self.saveHistory()
        self.setCookie('history', '1')
      else :
        # 履歴を取らないとき、クッキーを'0'にする。
        self.setCookie('history', '0')
    else :
      # 初期表示のとき
      self.setPlaceHolder("result", "")
      self.setPlaceHolder("sql", "")
      if self.isCookie('history') :
         if self.getCookie('history') == '1' :
           self.setPlaceHolder('history', 'checked')
         else :
           self.setPlaceHolder('history', '')
    return

  # SQL を実行して結果を返す。
  def execSql(self) :
    sql = self.getParam('sql')
    self.setPlaceHolder("sql", sql)
    rows = self.__mysql.query(sql)
    fields = self.__mysql.getFieldNames()
    if len(rows) == 0 :
      self.setPlaceHolder('result', 'データがありません。')
    else :
      # 実行結果をHTMLとして返す。
      buff = "<table>"
      buff += "<tr>"
      for field in fields :
        buff += f"<th>{field}</th>"
      buff += "</tr>"
      for row in rows :
        buff += "<tr>"
        for i in range(len(row)) :
          if type(row[i]) == str :
            s = row[i].replace("&", "&amp;")
            s = row[i].replace("<", "&lt;")
          else :
            s = str(row[i])
          buff += f"<td>{s}</td>"
        buff += "</tr>\n"
      buff += "</table>\n"
      self.setPlaceHolder('result', buff)
    return

  # 履歴を取る。
  def saveHistory(self) :
    sql = self.getParam('sql').replace("'", "''")
    info = self.getParam('info').replace("'", "''")
    # 登録する。
    insert = f"INSERT INTO History(dtime,caption,content,application,tag,info) VALUES(cast(now() as datetime),'Query', '{sql}', 'MySQL-IS python3', '0', '{info}')"
    self.__mysql.execute(insert)
    return

# メイン開始位置
wp = MainPage('templates/query.html')
wp.echo()
