#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS query.cgi  Version 2.00
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
    self.setPlaceHolder('userid', self.conf['uid'])
    self.setPlaceHolder('schema', self.conf['db'])
    if self.isParam("submit") :
      self.execSql()
    else :
      self.setPlaceHolder("result", "")
      self.setPlaceHolder("sql", "")
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


# メイン開始位置
wp = MainPage('templates/query.html')
wp.echo()
