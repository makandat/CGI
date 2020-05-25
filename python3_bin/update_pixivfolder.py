#!/usr/bin/python3

# Pictures/Pixiv フォルダの "[Pixiv] ..." の名前を変更したことに伴うデータベースの修正

from Py365Lib import Common, FileSystem as fs, Text, MySQL


# START
# 対象のフォルダ一覧を得る。
mysql = MySQL.MySQL()
rows = mysql.query("SELECT id, path FROM Pictures WHERE path LIKE '%[Pixiv]%'")

for row in rows :
  id = row[0]
  newpath = row[1].replace("[Pixiv] ", "")
  sql = "UPDATE Pictures SET path = '{0}' WHERE id = {1}".format(newpath, id)
  print(sql)
  mysql.execute(sql)

print("Done.")
