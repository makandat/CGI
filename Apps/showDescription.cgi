#!/usr/bin/env python3
#  Apps/index.cgi
import WebPage as cgi
import MySQL as my
import Common

# メインクラス
class ShowPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    # Common.init_logger("c:/temp/Apps.log")
    self.__mysql = my.MySQL()
    self.id = self.getParam("id")
    sql = "SELECT title FROM Apps WHERE id=" + str(self.id)
    # Common.log(sql)
    self.title = self.__mysql.getValue(sql)
    self.setPlaceHolder('title', self.title)
    self.setPlaceHolder('message', '')
    self.makeContent()
    return

  # 内容を作成する。
  def makeContent(self) :
    sql = f"SELECT description FROM Apps WHERE id={self.id}"
    description = self.__mysql.getValue(sql)
    self.setPlaceHolder("content", description)
    return

# START
ShowPage("./templates/showDescription.html").echo()
