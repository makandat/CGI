#!/usr/bin/python3
#!C:\Program Files (x86)\Python37\python.exe
#  extract.cgi  BINDATA テーブルから指定された id の画像を取り出す。
import sys
import WebPage as page
import MySQL
import Text
#from syslog import syslog

class Extract(page.WebPage) :
   # コンストラクタ
  def __init__(self, template="") :
    super().__init__(template)
    self.__mysql = MySQL.MySQL()
    if self.isParam('id') :
      id = self.getParam('id')
    else :
      id = 11  # for debug (folder.png)
    self.sendImage(id)
    return

  # 画像データを転送する。
  def sendImage(self, id) :
    sql = f"SELECT datatype, hex(data) as hex FROM BINDATA WHERE id={id}"
    rows = self.__mysql.query(sql)
    row = rows[0]
    datatype = row[0]
    data = row[1]
    if datatype == ".jpg" :
      mime = b"Content-Type: image/jpeg"
    elif datatype == ".png" :
      mime = b"Content-Type: image/png"
    elif datatype == ".gif" :
      mime = b"Content-Type: image/gif"
    else :
      return
    Extract.binout(mime, data)
    return

  # ヘキサ文字列をバイナリに変換し出力
  @staticmethod
  def binout(mime, data) :
    i = 0
    n = len(data)
    mime1 = bytearray(mime + b"\n\n")
    buff = list()
    for c in data :
      if  i % 2 == 1 :
        b = 16 * Extract.nibble(c0) + Extract.nibble(c)
        buff.append(b)
      else :
        c0 = c
      i += 1
    sys.stdout.buffer.write(mime1 + bytes(buff))
    #with open("/home/user/temp/dump.bin", "wb") as f :
    #  f.write(buff)
    return

  # ニブルに変換する。
  @staticmethod
  def nibble(c) :
    n = ord(c)
    if n >= 0x3a :
      n -= 0x41
      n += 10
    else :
      n -= 0x30
    return n



Extract()
