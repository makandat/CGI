#!/usr/binpython3
#  Pixiv3 と BINDATA の同じタイトルのレコードを Pixiv3.BINDATA に BINDATA.id を設定して結合する。
from MySQL import MySQL
import Common

# 開始
if Common.count_args() < 2 :
  Common.stop(9, "Usage: JoinPixiv3.py <from> <to>. from, to is id of BINDATA.")

# 変更対象の範囲
idfrom = Common.args(0)
idto = Common.args(1)

# MySQL オブジェクトを作成
client = MySQL()

SELECT_JOIN = "SELECT B.id bid, P.id pid FROM BINDATA B INNER JOIN Pixiv3 P ON B.title = P.Title WHERE B.id BETWEEN {0} AND {1}"
UPDATE = "UPDATE Pixiv3 SET BINDATA = {1} WHERE id = {0}"

# 対象のレコードを抽出する。
sql = SELECT_JOIN.format(idfrom, idto)
#print(sql)
rows = client.query(sql)
if len(rows) == 0 :
  Common.stop(1, "対象のレコードがありません。")

# Pixiv3 のデータを更新する。
for row in rows :
  bid = row[0]  # BINDATA の id
  pid = row[1]  # Pixiv3 の id
  sql = UPDATE.format(pid, bid)
  print(sql)
  client.execute(sql)

# 終わり
print("正常終了。")
