#!/usr/bin/python3
# -*- code=utf-8 -*-
#   MySQL-IS history.cgi  Version 2.00
import WebPage as web
import MySQL


# CGI WebPage クラス
class MainPage(web.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    if self.isParam('tag') :
      self.tag = self.getParam('tag')
      self.setPlaceHolder('title', 'MySQL-IS 管理SQL履歴')
    else :
      self.tag = ''
      self.setPlaceHolder('title', 'MySQL-IS クエリーSQL履歴')
    self.showHistory(self.tag)
    return
    
  # 履歴を表示する。
  def showHistory(self, tag) :
    if tag == '' :
      sql = f"SELECT id, dtime,content, info FROM History WHERE application='MySQL-IS python3' ORDER BY id DESC"
    else :
      sql = f"SELECT id, dtime,content, info FROM History WHERE application='MySQL-IS python3' AND tag >= '{tag}' ORDER BY id DESC"
    rows = self.__mysql.query(sql)
    n = len(rows)
    if n == 0 :
      self.setPlaceHolder('message', '履歴データありません。')
      self.setPlaceHolder('result', "")
      return
    self.setPlaceHolder('message', f"{n} 件の履歴が見つかりました。");
    result = ""
    for row in rows :
      result += "<tr>"
      result += ('<td>' + str(row[0]) + '</td>')
      result += ('<td>' + str(row[1]) + '</td>')
      result += ('<td><pre>' + row[2] + '</pre></td>')
      result += ('<td>' + row[3] + '</td>')
      result += "</tr>\n"
    self.setPlaceHolder('result', result)
    return


# メイン開始位置
wp = MainPage('templates/history.html')
wp.echo()
