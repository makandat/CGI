#!C:/Program Files (x86)/Python37/python.exe
#!C:/Program Files/python3/python.exe
#!/usr/bin/env python3

#  Jura_Zakki CGI  v0.1.0 2020-06-26
from WebPage import WebPage
from MySQL import MySQL
import Common

# index.cgi ウェブページ
class MainPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    Common.init_logger("C:/temp/jura_zakki.log")
    self.__mysql = MySQL()
    reverse = self.isParam("reverse")
    findWord = ""
    if self.isParam("word") :
      findWord = self.getParam("word")
    self.queryContent(reverse, findWord)
    return

  # 記事一覧を得る。
  def queryContent(self, reverse, findWord) :
    sql = "SELECT id, title, path, category, tag, addate FROM JURA_ZAKKI"
    if len(findWord) > 0 :
      sql += f" WHERE instr(title, '{0}') OR instr(category, '{0}') OR instr(tag, '{0}')".format(findWord)
    Common.log(sql)
    if reverse :
      sql += " ORDER BY id ASC"
    else :
      sql += " ORDER BY id DESC"
    Common.log(sql)
    sql += " LIMIT 1000"
    Common.log(sql)
    rows = self.__mysql.query(sql)
    content = ""
    for row in rows :
      line = ""
      line += WebPage.tag("td", row[0])
      url = f"<a href=\"{row[2]}\" target=\"_blank\">" + row[1] + "</a>"
      line += WebPage.tag("td", url)
      line += WebPage.tag("td", row[3])
      line += WebPage.tag("td", row[4])
      line += WebPage.tag("td", row[5])
      line = WebPage.tag("tr", line)
      content += line
    self.setPlaceHolder("content", content)
    return

# スタート
wp = MainPage("templates/index.html")
wp.echo()
