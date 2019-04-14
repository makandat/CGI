#!C:\Program Files (x86)\Python37\python.exe
# -*- code=utf-8 -*-
import WebPage as page
import MySQL
import Common
#from syslog import syslog

SELECT = f"SELECT DISTINCT creator FROM Pictures "

# CGI WebPage クラス
class MainPage(page.WebPage) :

  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    # Common.init_logger("C:/temp/PyLogger.log")
    self.__mysql = MySQL.MySQL()
    if self.isParam('filter') :
     self.filter()
    else :
      self.all()
    self.setPlaceHolder("message", "クエリー OK")
    return

  # 条件に合う作者を列挙
  def filter(self) :
    filt = self.getParam('filter')
    where = f"WHERE creator LIKE '%{filt}%' OR `path` LIKE '%{filt}%' OR info LIKE '%{filt}%' OR mark='{filt}'"
    sql = SELECT + where + " ORDER BY creator"
    rows = self.__mysql.query(sql)
    list = self.makelist(rows)
    self.setPlaceHolder('list', list)
    return

  # すべての作者を列挙
  def all(self) :
    sql = SELECT + " ORDER BY creator"
    rows = self.__mysql.query(sql)
    list = self.makelist(rows)
    self.setPlaceHolder('list', list)
    return

  # リストを作成
  def makelist(self, rows) :
    list = ""
    for row in rows :
      creator = row[0]
      anchor = "<a href=\"index.cgi?creator=" + creator + "\">" + creator + "</a>"
      list += page.WebPage.tag("li", anchor)
    return list

# メイン開始位置
wp = MainPage('templates/creators.html')
wp.echo()
