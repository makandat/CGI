#!/usr/bin/env python3
# WIKI showContent.cgi  v1.2.1 2020-07-01
from WebPage import WebPage
from MySQL import MySQL
from DateTime import DateTime
import Text
import Common
import markdown


SELECT = "SELECT id, title, author, date, content, info, type, revision FROM Wiki WHERE id={0}"

# ページクラス
class ShowPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    #Common.init_logger("C:/temp/showContent.log")
    if self.isParam("id") :
      id = self.getParam("id")
      rows = self.__mysql.query(SELECT.format(id))
      if len(rows) == 0 :
        self.embed({"title":"Unknown", "message":"エラー： id が正しくありません。", "prop":"", "content":""})
        return
      row = rows[0]
      content_rows = row[4].split("\r")
      content = "".join(content_rows)
      data = {"title":row[1], "author": "" if row[2] == None else row[2], "date": str(row[3]), "content":content, "info":row[5], "type":row[6], "revision":row[7]}
      doctype = row[6]
      if doctype.lower() == "text" :
        self.showAsText(id, data)
      elif doctype.lower() == "html" :
        self.showAsHTML(id, data)
      else :
        self.showAsMarkup(id, data)
    else :
      self.embed({"title":"Unknown", "message":"エラー： id が指定されていません。", "prop":"", "content":""})
    return
    
  # 内容を平文として表示する。
  def showAsText(self, id, data) :
    prop = "<span style='font-weight:bold;color:black;'>" + data["title"] + "</span> revision=" + str(data["revision"]) + " date=" + str(data["date"]) + " doctype=" + data["type"]
    content = WebPage.escape(data["content"])
    self.embed({"title":data["title"], "message":f"id={id}の内容が表示されました。", "prop":prop, "content":content});
    self.setPlaceHolder("display_pre", "block")
    self.setPlaceHolder("display_div", "none")
    return
    
  # 内容をHTMLとして表示する。
  def showAsHTML(self, id, data) :
    content = data["content"].replace("\n", "")
    prop = "<span style='font-weight:bold;color:black;'>" + data["title"] + "</span>, revision=" + str(data["revision"]) + ", date=" + str(data["date"]) + ", doctype=" + data["type"]
    self.embed({"title":data["title"], "message":f"id={id}の内容が表示されました。", "prop":prop, "content":content});
    self.setPlaceHolder("display_pre", "none")
    self.setPlaceHolder("display_div", "block")
    return

  # 内容をMarkupとして表示する。
  def showAsMarkup(self, id, data) :
    prop = "<span style='font-weight:bold;color:black;'>" + data["title"] + "</span>, revision=" + str(data["revision"]) + ", date=" + str(data["date"]) + ", doctype=" + data["type"]
    content = ShowPage.markup(WebPage.escape(data["content"]))
    self.embed({"title":data["title"], "message":f"id={id}の内容が表示されました。", "prop":prop, "content":content});
    self.setPlaceHolder("display_pre", "none")
    self.setPlaceHolder("display_div", "block")
    return
  
  # マークアップ言語を HTML にする。
  @staticmethod
  def markup(data) :
    lines = data.split("\n")
    md = markdown.Markdown()
    html = md.convert(data)
    return html
    
# 応答を返す。
page = ShowPage('templates/showContent.html')
page.echo()
