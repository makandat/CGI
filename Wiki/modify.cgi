#!/usr/bin/env python3
# WIKI modify.cgi  v1.00 2019-10-27
from WebPage import WebPage
from MySQL import MySQL
from DateTime import DateTime
import Text, cgi
import Common

SELECT = "SELECT id, title, `date`, content, info, revision, `type` FROM Wiki WHERE id={0}"
UPDATE = "UPDATE Wiki SET title='{1}', content='{2}', revision='{3}', `type`='{4}' WHERE id={0}'"

# ページクラス
class ModifyPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    #Common.init_logger("/home/user/log/modify.log")
    #form = cgi.FieldStorage()
    #ids = form["pid"]
    if self.getMethod() == "POST" :
      id = self.getParam("pid")
      self.update(id)
    else :
      id = self.getParam("id")
      self.getContent(id)
    return
    
  # id で指定された記事内容をフォームに表示する。
  def getContent(self, id) :
    rows = self.__mysql.query(SELECT.format(id))
    if len(rows) == 0 :
      self.embed({"message":"エラー： id が正しくありません。", "id":"", "title":"", "content":"", "info":"", "revision":"", "type0":"", "type1":"", "type2":""})
    else :
      row = rows[0]
      title = row[1]
      date = row[2]
      content = row[3].replace("\\n", "\n")
      info = row[4]
      revision = row[5]
      doctype = row[6]
      type0 = "selected" if doctype == "text" else ""
      type1 = "selected" if doctype == "html" else ""
      type2 = "selected" if doctype == "markup" else ""
      self.embed({"message":f"id={id} の情報が検索されました。", "id":id, "title":title, "content":content, "info":info, "revision":revision, "type0":type0, "type1":type1, "type2":type2})
    return
    
  # 情報を更新する。
  def update(self, id) :
    title = self.getParam("title")
    content = self.getParam("content")
    content1 = content.replace("\n", "\\n")
    info = self.getParam("info")
    revision = self.getParam("revision")
    doctype = self.getParam("type")
    type0 = "selected" if doctype.lower() == "text" else ""
    type1 = "selected" if doctype.lower() == "html" else ""
    type2 = "selected" if doctype.lower() == "markup" else ""
    sql = f"UPDATE Wiki SET `title`='{title}', `content`='{content1}', `info`='{info}', `revision`='{revision}', `type`='{doctype}' WHERE id={id}"
    self.__mysql.execute(sql)
    self.embed({"message":f"id={id} の情報が更新されました。", "id":id, "title":title, "content":content, "info":info, "revision":revision, "type0":type0, "type1":type1, "type2":type2})
    return
    
# 応答を返す。
page = ModifyPage('templates/modify.html')
page.echo()
