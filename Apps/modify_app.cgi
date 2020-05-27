#!/usr/bin/env python3
#!/usr/bin/env python3
#  Apps/modify_app.cgi
import WebPage as cgi
import MySQL as my
import Common

# メインクラス
class ModifyPage(cgi.WebPage) :
  # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    # Common.init_logger("c:/temp/Apps.log")
    self.__mysql = my.MySQL()
    # Common.log(self.params)
    if self.isPostback() :
      if self.isParam("confirm") and (not self.isParam("id")) :
        self.id = self.getParam("confirm")
        self.sendForm(self.id)
      elif self.isParam("id") :
        self.id = self.getParam("id")
        self.update()
      else :
        self.insert()
    else :
      self.sendForm()
    return

  # フォームを送信する。
  def sendForm(self, id = 0) :
    if id == 0 :
      if Common.is_windows() :
        self.platform = "windows"
      else :
        self.platform = "linux"
      self.embed({"message":"", "id":"", "title":"", "path":"", "interpreter":"", "platform":self.platform, "info":"", "description":"", "path2":"", "tag":""})
    else :
      sql = "SELECT id, title, path, interpreter, platform, info, description, path2 FROM Apps WHERE id = " + self.id
      rows = self.__mysql.query(sql)
      if len(rows) == 0 :
        self.embed({"message":"エラー： id が正しくありません。", "id":"", "title":"", "path":"", "interpreter":"", "platform":self.platform, "info":"", "description":"", "path2":"", "tag":""})
      else :
        row = rows[0]
        self.embed({"message":"検索されました。id = " + str(row[0]), "id":row[0], "title":row[1], "path":row[2], "interpreter":row[3], "platform":row[4], "info":row[5], "description":row[6], "path2":row[7], "tag":row[8]})
    return

  # データをテーブルに挿入する。
  def insert(self) :
    self.title = self.getParam("title")
    self.path = self.getParam("path")
    self.interpreter = self.getParam("interpreter")
    self.platform = self.getParam("platform")
    self.info = self.getParam("info")
    self.description = self.getParam("description")
    self.path2 = self.getParam("path2")
    self.tag = self.getParam("tag")
    if Common.is_windows() :
      self.path = self.path.replace("\\", "/")
      self.path2 = self.path2.replace("\\", "/")
    sql = f"INSERT INTO Apps VALUES(NULL, '{self.title}', '{self.path}', '{self.interpreter}', '{self.platform}', '{self.info}', '{self.description}', '{self.path2}', '{self.tag}', CURRENT_DATE())"
    self.__mysql.execute(sql)
    maxid = self.__mysql.getValue("SELECT max(id) FROM Apps")
    self.embed({"message":"データを挿入しました。id = " + str(maxid), "id":"", "title":self.title, "path":self.path, "interpreter":self.interpreter, "platform":self.platform, "info":self.info, "description":self.description, "path2":self.path2, "tag":self.tag})
    return

  # テーブルを更新する。
  def update(self) :
    self.id = self.getParam("id")
    self.title = self.getParam("title")
    self.path = self.getParam("path")
    self.interpreter = self.getParam("interpreter")
    self.platform = self.getParam("platform")
    self.info = self.getParam("info")
    self.description = self.getParam("description")
    self.path2 = self.getParam("path2")
    self.tag = self.getParam("tag")
    if Common.is_windows() :
      self.path = self.path.replace("\\", "/")
      self.path2 = self.path2.replace("\\", "/")
    sql = f"UPDATE Apps SET title='{self.title}', path='{self.path}', interpreter='{self.interpreter}', platform='{self.platform}', info='{self.info}', description='{self.description}', path2='{self.path2}', tag='{self.tag}', `date`=CURRENT_DATE() WHERE id={self.id}"
    self.__mysql.execute(sql)
    self.embed({"message":"データを更新しました。id = " + str(self.id), "id":self.id, "title":self.title, "path":self.path, "interpreter":self.interpreter, "platform":self.platform, "info":self.info, "description":self.description, "path2":self.path2, "tag":self.tag})
    return


# スタート
ModifyPage("./templates/modify_app.html").echo()
