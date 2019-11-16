#!/usr/bin/env python3

#  ファイル一覧を PictureAlbum テーブルへインポートでする。
from Py365Lib import Common, FileSystem as fs, MySQL

# START
# パラメータ確認
if Common.count_args() < 2 :
  Common.stop("Usage : ins_flist.py filelist album_no")
filelist = Common.args(0)
album_no = Common.args(1)
# MySQL に接続
mysql = MySQL.MySQL()
#  ファイルリストを読む。
lines = fs.readLines(filelist)
for path in lines :
  path = path.strip().replace("'", "''")
  parts = path.split("/")
  n = len(parts)
  if n > 3 :
    title = parts[n-2]
    creator = parts[n-3]
  else :
    title = "title"
    creator = "creator"
  sql = f"INSERT INTO PictureAlbum VALUES(NULL,{album_no},'{title}','{path}','{creator}','',0,0)"
  print(sql)
  mysql.execute(sql)
print("Done.")
 
