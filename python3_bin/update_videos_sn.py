#!/usr/bin/python3
#  Pictures の sn フィールドを更新する。
from Py365Lib import Common, MySQL

mysql = MySQL.MySQL()

rows = mysql.query("SELECT id FROM Videos ORDER BY id ASC")

i = 1
for row in rows:
  id =row[0]
  sql = f"UPDATE Videos SET sn = {i} WHERE id = {id}"
  print(sql)
  mysql.execute(sql)
  i += 1

print("Done.")

