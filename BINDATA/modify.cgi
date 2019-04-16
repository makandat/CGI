#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
#  modify.cgi BINDATA の情報を修正する。
import WebPage as page
import MySQL
#from syslog import syslog

class ModifyPage(page.WebPage) :
   # コンストラクタ
  def __init__(self, template) :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    if self.isParam('submit') :
      # コールバックのとき
      self.modify()
    else :
      # コールバックでないとき
      if self.isParam('id') :
        self.showData(self.getParam('id'))
      else :
        self.setPlaceHolder('message', '')
        self.setPlaceHolder('id', '')
        self.setPlaceHolder('title', '')
        self.setPlaceHolder('original', '')
        self.setPlaceHolder('datatype', '')
        self.setPlaceHolder('info', '')
    return

  # 情報を表示する。
  def showData(self, id) :
    sql = "SELECT `title`,`original`,`datatype`,`info`, `size` FROM BINDATA WHERE `id`=" + str(id)
    rows = self.__mysql.query(sql)
    if len(rows) > 0 :
        row = rows[0]
        self.setPlaceHolder('message', '')
        self.setPlaceHolder('id', str(id))
        self.setPlaceHolder('title', row[0])
        self.setPlaceHolder('original', ModifyPage.NoneToNull(row[1]))
        self.setPlaceHolder('datatype', row[2])
        self.setPlaceHolder('info', ModifyPage.NoneToNull(row[3]))
        self.setPlaceHolder('size', ModifyPage.NoneToNull(row[4]))
    else :
        self.setPlaceHolder('message', 'エラー： id が正しくありません。')
        self.setPlaceHolder('id', str(id))
        self.setPlaceHolder('title', '')
        self.setPlaceHolder('original', '')
        self.setPlaceHolder('datatype', '')
        self.setPlaceHolder('info', '')
        self.setPlaceHolder('size', '')
    return

  # 情報を修正する。
  def modify(self) :
    UPDATESQL = "UPDATE BINDATA SET title='{1}', original='{2}', datatype='{3}', info='{4}', size={5} WHERE id={0}"
    id = self.getParam('id')
    title = self.getParam('title')
    original = self.getParam('original').replace("'", "''")
    datatype = self.getParam('datatype')
    info = self.getParam('info').replace("'", "''")
    size = self.getParam('size')
    sql = UPDATESQL.format(id, title, original, datatype, info, size)
    try :
      #syslog(sql)
      self.__mysql.execute(sql)
      self.setPlaceHolder('message', "id = " + str(id) + ' の情報が修正されました。')
    except Exception as e :
      self.setPlaceHolder('message', "id = " + str(id) + ' の情報の修正に失敗しました。' + str(e))
    self.setPlaceHolder('id', str(id))
    self.setPlaceHolder('title', title)
    self.setPlaceHolder('original', self.getParam('original'))
    self.setPlaceHolder('datatype', datatype)
    self.setPlaceHolder('info', self.getParam('info'))
    self.setPlaceHolder('size', self.getParam('size'))
    return

  @staticmethod
  def NoneToNull(s) :
    if s == None :
      return ""
    else :
      return s
    


# 応答をクライアントへ返す。
wp = ModifyPage('templates/modify.html')
wp.echo()


