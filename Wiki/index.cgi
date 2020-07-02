#!/usr/bin/python3
# WIKI index.cgi  v1.2.0 2020-05-27
from WebPage import WebPage
from MySQL import MySQL

SELECT = "SELECT id, title, ifnull(author, ''), `date`, ifnull(info, ''), revision, `type` FROM Wiki WHERE hidden='0' ORDER BY id DESC"
SELECT2 = "SELECT id, title, ifnull(author, ''), `date`, ifnull(info, ''), revision, `type` FROM Wiki WHERE hidden='0' AND {0} ORDER BY id DESC"


# ページクラス
class IndexPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    self.setPlaceHolder('message', "")
    content_list = self.getWikiList()
    self.setPlaceHolder('content_list', content_list)
    if self.isParam("word") :
      word = self.getParam("word")
      content_list = self.getWikiList(word)
    else :
      content_list = self.getWikiList()
    self.setPlaceHolder('content_list', content_list)
    return

  # 投稿リストを作成する。
  def getWikiList(self, word="") :
    buff = ""
    rows = []
    if word == "" :
      rows = self.__mysql.query(SELECT)
    else :
      criteria = "title like '%{0}%' or content like '%{0}%' or info like '%{0}%' or `date` like '%{0}%'".format(word)
      rows = self.__mysql.query(SELECT2.format(criteria))
    for row in rows :
      buff += IndexPage.table_row(row)
      buff += "\n"
    return buff
    
  # HTML テーブル行を作成する。
  @staticmethod
  def table_row(row) :
    buff = "<tr>"
    for i in range(len(row)) :
      id = row[0]
      if i == 0 :
        buff += "<td style=\"text-align:center;\">"
        buff += f"<a href=\"modify.cgi?id={id}\" target=\"_blank\">{id}</a>"
      elif i == 1 :
        buff += "<td>"
        buff += f"<a href=\"showContent.cgi?id={id}\" target=\"_blank\">{row[1]}</a>"
      else :
        buff += "<td>"
        buff += str(row[i])
      buff += "</td>"
    buff += "</tr>\n"
    return buff


# 応答を返す。
page = IndexPage('templates/index.html')
page.echo()
