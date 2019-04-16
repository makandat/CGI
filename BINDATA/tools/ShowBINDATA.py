#!/usr/bin/env python3
#  BINDATA テーブルの内容
import MySQL as mysql
import Text, Common
from pprint import pprint

SELECT = "SELECT id, title, original, datatype, isnull(data) as not_null, info, size FROM BINDATA"


client = mysql.MySQL()
if Common.count_args() > 0 :
  datatype = Common.args()[0]
  sql = SELECT + " WHERE datatype='{0}'".format(datatype)
else :
  sql = SELECT + " ORDER BY id DESC LIMIT 400"
rows = client.query(sql)
for row in rows :
  pprint(row)

print("Done.")
