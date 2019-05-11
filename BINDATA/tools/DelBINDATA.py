#!/usr/bin/env python3
#  BINDATA テーブルのデータ削除
import MySQL as mysql
import Text, Common
import FileSystem as fs
from pprint import pprint

DELETE = "DELETE FROM BINDATA WHERE id={0}"
SELECT = "SELECT id, title FROM BINDATA WHERE id={0}"


# メイン
client = mysql.MySQL()
id = 0
if Common.count_args() == 0 :
  id = Common.readline("対象の id を入力します。")
  if id == "" :
    Common.stop(1, "実行を中止しました。")
else :
  id = Common.args(0)
sql = SELECT.format(id)
rows = client.query(sql)
if len(rows) == 0:
  Common.stop(2, "対象のデータがありません。")
row = rows[0]
title = row[1]
a = Common.readline("id =  {0};  title = '{1}' を削除します。(y/n) ".format(id, title))
if a == 'y' :
  sql = DELETE.format(id)
  client.execute(sql)
  Common.stop(0, "id = {0} のデータを削除しました。")
else :
  Common.stop(1, "実行を中止しました。")
