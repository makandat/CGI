#!/usr/bin/env python3

#  ディレクトリ一覧を Pictures テーブルへインポートする。
from Py365Lib import Common, FileSystem as fs, MySQL

# path からデータとSQLを作りPicturesテーブルに挿入する。
def InsertData(path) :
  path = path.replace("'", "''").replace("\\", "/")
  parts = path.split("/")
  n = len(parts)
  if n > 2 :
    title = parts[n-1]
    creator = parts[n-2]
  else :
    title = "title"
    creator = "creator"
  sql = f"INSERT INTO Pictures(TITLE, CREATOR, PATH, MARK, INFO, FAV, COUNT, BINDATA) VALUES('{title}', '{creator}', '{path}', '', '', 0, 0, 0)"
  print(sql)
  mysql.execute(sql)
  return

# START
# パラメータ確認
if Common.count_args() < 1 :
  Common.stop("Usage : InsPictures.py directory")
dir_parent = Common.args(0)
# MySQL に接続
mysql = MySQL.MySQL()
#  画像ファイルを含むサブディレクトリ一覧を得る。
dirlist = fs.listDirectories(dir_parent, True)
for dir in dirlist :
  dirlist2 = fs.listDirectories(dir, True)
  if len(dirlist2) == 0 :
    InsertData(dir)
  else :
    for path in dirlist2 :
      InsertData(path)
print("Done.")
 
