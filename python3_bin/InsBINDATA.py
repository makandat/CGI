#!/usr/bin/python3
#  サムネール画像を BINDATA テーブルに挿入する。

from Py365Lib import Common, FileSystem as fs, Text, MySQL
import os, math

# 定数定義
if Common.is_windows() :
  SAVEDIR = "c:/temp/" # 注意：変更が必要
else :
  SAVEDIR = "/home/user/Pictures/Small" # 注意：変更が必要

INSERT = "INSERT INTO BINDATA(`title`, `original`, `datatype`, `data`, `info`, `size`, `sn`) VALUES('{0}', '{1}', '{2}', {3}, '', {4}, {5})"

# バイナリーファイルをヘキサに変換する。
def bin2hex(filePath) :
  buff = "0x"
  b = fs.readBinary(filePath)
  buff += b.hex()
  return buff

# バイナリーファイル filePath をテーブル BINDATA に挿入する。
def insertBinaries(filePath) :
  ext = fs.getExtension(filePath)
  size = fs.getFileSize(filePath)
  name = fs.getFileName(filePath)
  filePath = filePath.replace("\\", "/")
  hexa = bin2hex(filePath)
  sn = mysql_client.getValue("SELECT max(sn) FROM BINDATA") + 1
  sql = Text.format(INSERT, name, filePath, ext, hexa, size, sn)
  mysql_client.execute(sql)
  lastId = mysql_client.getValue("SELECT max(id) FROM BINDATA")
  return lastId



#  Start up
# パラメータ確認・取得
if Common.count_args() == 0 :
  filePath = Common.readline("サムネール画像ファイルのパスを入力します。> ")
else :
  filePath = Common.args(0)

# MySQL クライアントを構築
mysql_client = MySQL.MySQL()
# データ挿入
last = insertBinaries(filePath)

print(f"BINDATA テーブルの id = {last} に挿入しました。")
