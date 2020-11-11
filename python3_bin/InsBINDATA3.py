#!/usr/bin/env python3

#  画像ファイルのサムネールを作成し、BINDATA テーブルに挿入する。
#  さらに、そのサムネールを Pictures または Videos テーブル、Album テーブルに、 Music テーブル関連付ける。
# (使用法) InsBINDATA3 画像ファイルのパス Picturesテーブルの対象id
# (バージョン) 1.3.0

from PIL import Image, ImageFilter
from Py365Lib import Common, FileSystem as fs, Text, MySQL
import os, math


# 定数定義
NEWSIZE = 64
if Common.is_windows() :
  SAVEDIR = "c:/temp/" # 注意：Windows では変更が必要
else :
  SAVEDIR = "/home/user/Pictures/Small" # 注意：Windows では変更が必要
INSERT = "INSERT INTO BINDATA(`title`, `original`, `datatype`, `data`, `info`, `size`) VALUES('{0}', '{1}', '{2}', {3}, '', {4})"
UPDATE = "UPDATE {0} SET bindata = {1} WHERE id = {2}"


# バイナリーファイルをヘキサに変換する。
def bin2hex(filePath) :
  buff = "0x"
  b = fs.readBinary(filePath)
  buff += b.hex()
  return buff


# サムネール画像を取得する。
def saveThumb(filePath) :
  im = Image.open(filePath)
  # print(im.format, im.size, im.mode)
  if im.size[0] > im.size[1] :
    w = NEWSIZE
    h = math.floor(NEWSIZE * (im.size[1] / im.size[0]))
  else :
    w = math.floor(NEWSIZE * (im.size[0] / im.size[1])) 
    h = NEWSIZE
  newsize = (w, h)
  newim = im.resize(newsize, Image.LANCZOS)
  newPath = SAVEDIR + fs.getFileName(filePath)
  newim.save(newPath)
  return newPath


# バイナリーファイル filePath をテーブル BINDATA に挿入する。
def insertBinaries(filePath, origin) :
  ext = fs.getExtension(filePath)
  size = fs.getFileSize(filePath)
  parts = origin.split("/")
  n = len(parts)
  if n > 3 :
    name = parts[n-3] + " " + parts[n-2]
  else :
    name = origin
  filePath = filePath.replace("\\", "/")
  filePath = filePath.replace("'", "''")
  hexa = bin2hex(filePath)
  sql = Text.format(INSERT, name, origin, ext, hexa, size)
  mysql_client.execute(sql)
  lastId = mysql_client.getValue("SELECT max(id) FROM BINDATA")
  return lastId


# Pictures or Videos or Album テーブルを更新する。
def updateTable(tableName, bid, pid) :
  sql = UPDATE.format(tableName, bid, pid)
  mysql_client.execute(sql)
  return


#  Start up
# パラメータ確認・取得
if Common.count_args() == 0 :
  filePath = Common.readline("画像ファイルのパスを入力します。> ")
else :
  filePath = Common.args(0)

nargs = Common.count_args()

if nargs == 1 :
  pid = Common.readline("Pictures テーブルの対象 id を入力します。> ")
  nargs = 2
else :
  pid = Common.args(1)

if nargs == 2 :
  tableName = "Pictures"
else :
  if Common.args(2) == "V" :
    tableName = "Videos"
  elif Common.args(2) == 'P' :
    tableName = "Pictures"
  elif Common.args(2) == 'A' :
    tableName = "Album"
  elif Common.args(2) == 'M' :
    tableName = "Music"
  else :
    tableName = "Pictures"

print("> InsBINDATA3.py " + filePath + ", " + pid + ", " + tableName)
if not fs.exists(filePath) :
  Common.stop(9, "画像ファイルが見つかりません。")

# MySQL クライアントを構築
mysql_client = MySQL.MySQL()


# サムネール画像を作成する。
newPath = saveThumb(filePath)

# サムネール画像を BINDATA テーブルに挿入する。
bid = insertBinaries(newPath, filePath)

# Pictures テーブルを更新する。
updateTable(tableName, bid, pid)

# 終わり
print(tableName + " and BINDATA Updated.")
