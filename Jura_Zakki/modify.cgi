#!C:/Program Files (x86)/Python37/python.exe
#!C:/Program Files/python3/python.exe
#!/usr/bin/env python3

#  Jura_Zakki CGI  v0.1.0 2020-06-26
from WebPage import WebPage
from MySQL import MySQL
import Common

# modify.cgi ウェブページ
class ModifyPage(WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL()
    Common.init_logger("C:/temp/jura_zakki.log")
    self.setPlaceHolder("message", "")
    if self.isPostback() :
      if self.isParam("id") :
        # 修正
        self.update(self.getParam("id"))
      elif self.isParam("confirm") :
        # データ確認
        self.confirm(self.getParam("confirm"))
      else :
        # 挿入
        self.insert()
    else :
      # フォーム表示のみ
      self.embed({"id":"", "title":"", "path":"", "category":"", "tag":"", "addate":""})
    return

  # 指定された id の情報を修正
  def update(self, id) :
    UPDATE = "UPDATE JURA_ZAKKI SET title='{1}', path='{2}', category='{3}', tag='{4}', addate='{5}' WHERE id={0}"
    title = self.getParam("title").replace("'", "''")
    path = self.getParam("path")
    category = self.getParam("category")
    tag = self.getParam("tag")
    addate = self.getParam("addate")
    if not (self.isParam("title") and self.isParam("path")) :
      self.setPlaceHolder("message", "エラー：タイトルまたはURLが空欄です。")
    else :
      sql = UPDATE.format(id, title, path, category, tag, addate)
      self.__mysql.execute(sql)
      self.setPlaceHolder("message", "id " + str(id) + " が更新されました。")
    self.embed({"id":id, "title":title, "path":path, "category":category, "tag":tag, "addate":addate})
    return

  # 情報を挿入
  def insert(self) :
    INSERT = "INSERT INTO JURA_ZAKKI VALUES(NULL, '{0}', '{1}', '{2}', '{3}', '{4}')"
    id = self.getParam("id")
    title = self.getParam("title").replace("'", "''")
    path = self.getParam("path")
    category = self.getParam("category")
    tag = self.getParam("tag")
    addate = self.getParam("addate")
    if not (self.isParam("title") and self.isParam("path")) :
      self.setPlaceHolder("message", "エラー：タイトルまたはURLが空欄です。")
      id = ""
    else :
      sql = INSERT.format(title, path, category, tag, addate)
      Common.log(sql)
      self.__mysql.execute(sql)
      id = self.getMaxID()
      self.setPlaceHolder("message", "id " + str(id) + " が挿入されました。")
    self.embed({"id":id, "title":title, "path":path, "category":category, "tag":tag, "addate":addate})
    return

  # データ確認
  def confirm(self, id) :
    sql = "SELECT id, title, path, category, tag, addate FROM JURA_ZAKKI WHERE id = " + id
    rows = self.__mysql.query(sql)
    if len(rows) == 0 :
      self.embed({"id":"", "title":"Error: bad id", "path":"", "category":"", "tag":"", "addate":""})
    else :
      row = rows[0]
      self.embed({"id":row[0], "title":row[1], "path":row[2], "category":row[3], "tag":row[4], "addate":row[5]})
    return


  # id の最大値を得る。
  def getMaxID(self) :
    sql = "SELECT max(id) FROM JURA_ZAKKI"
    id = self.__mysql.getValue(sql)
    return id

# スタート
wp = ModifyPage("templates/modify.html")
wp.echo()
