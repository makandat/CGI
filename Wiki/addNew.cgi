#!/usr/bin/python3
# WIKI addNew.cgi  v1.2.0 2020-05-27
from WebPage import WebPage
from MySQL import MySQL
from DateTime import DateTime
import Text

# ページクラス
class IndexPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    if self.isParam("submit") :
      # 投稿する。
      self.postWiki()
    else :
      self.embed({"title":"", "date":"", "content":"", "info":"", "type":"", "revision":"0", "message":"", "hidden":"0"})
    return
    
  # ウィキを投稿する。
  def postWiki(self) :
    title = self.getParam("title", "")
    dt = DateTime()
    date = dt.toString()
    content = self.getParam("content", "").replace("\\", "\\\\").replace("\n", "\\n")
    info = self.getParam("info", "")
    doc_type = self.getParam("type", "")
    revision = self.getParam("revision", "0")
    self.embed({"title":title, "date":date, "content":content, "info":info, "type":doc_type, "revision":revision, "hidden":"0"})
    if title == "" or content == "" :
      self.setPlaceHolder("message", "ERROR: Title or content must not be empty.")
    else :
      sql = "INSERT INTO Wiki VALUES(null, '{0}', null, '{1}', '{2}', '{3}', '0', '{4}', '{5}')".format(title, date, content, info, doc_type, revision)
      self.__mysql.execute(sql)
      self.setPlaceHolder("message", "新規投稿の追加に成功しました。")
    return  
    
# 応答を返す。
page = IndexPage('templates/addNew.html')
page.echo()

