#!/usr/bin/env python3
#  Apps/index.cgi
import WebPage as cgi
import MySQL as my

# メインクラス
class IndexPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = my.MySQL()
    self.setPlaceHolder('message', '')
    if self.isParam('cmdonly') :
      self.setPlaceHolder('title', 'コマンド一覧')
      self.makeContent("VW_BinFolder")
    else :
      self.setPlaceHolder('title', 'アプリ一覧')
      self.makeContent()
    return

  # 表の内容を作成する。
  def makeContent(self, cmdonly = False) :
    if cmdonly :
      sql = "SELECT id, title, path, interpreter, platform, info, description, path2, tag, DATE_FORMAT(`date`, '%Y-%m-%d') AS dt FROM VW_BinFolder"
    else :
      sql = "SELECT id, title, path, interpreter, platform, info, description, path2, tag, DATE_FORMAT(`date`, '%Y-%m-%d') AS dt FROM Apps"
    rows = self.__mysql.query(sql)
    content = ""
    for row in rows :
      content += "<tr>"
      content += cgi.WebPage.tag("td", str(row[0]))
      content += cgi.WebPage.tag("td", row[1])
      if len(row[3]) == 0 :
        content += cgi.WebPage.tag("td", row[2])
      else :
        content += ("<td><a href=\"/cgi-bin/showSource.cgi?path=" + row[2] + "\" target=\"_blank\">" + row[2] + "</a></td>")
      content += cgi.WebPage.tag("td", row[3])
      content += cgi.WebPage.tag("td", row[4])
      content += cgi.WebPage.tag("td", row[5])
      if len(row[6]) > 0 :
        content += ("<td><a href=\"/cgi-bin/Apps/showDescription.cgi?id=" + str(row[0]) + "\" target=\"_blank\">" + row[6][0:40] + "</a></td>")
      else :
        content += "<td></td>"
      if row[7] == None :
        content += "<td></td>"
      else :
        content += ("<td><a href=\"/cgi-bin/showSource.cgi?path=" + str(row[7]) + "\" target=\"_blank\">" + str(row[7]) + "</a></td>")
      content += cgi.WebPage.tag("td", row[8])
      content += cgi.WebPage.tag("td", row[9])
      content += "</tr>\n"
      self.setPlaceHolder("content", content)
    return


# スタート
IndexPage("./templates/index.html").echo()
