#!/usr/bin/env python3
#  バイナリーデータを取り出す。
import FileSystem as fs
import MySQL as mysql
import Common
import Text

SELECT = "SELECT hex(data) FROM BINDATA WHERE id={0}"

# バイナリーデータ取り出してファイル保存する。
def extract(id:int, filePath:str) -> None:
  client = mysql.MySQL()
  sql = Text.format(SELECT, id)
  rows = client.query(sql)
  data = rows[0][0]
  write_bindata(filePath, data)
  return

# ヘキサ文字列をバイナリーファイルに保存する。
def write_bindata(filePath:str, data:str) -> None :
  i = 0
  buff =  list()
  with open(filePath, "wb") as f :
    for c in data :
      if  i % 2 == 1 :
        b = 16 * nibble(c0) + nibble(c)
        buff.append(b)
      else :
        c0 = c
      i += 1
    f.write(bytes(buff))
  return

# ニブルに変換する。
def nibble(c) :
  n = ord(c)
  if n >= 0x3a :
    n -= 0x41
    n += 10
  else :
    n -= 0x30
  return n


# メイン
if Common.count_args() < 2 :
  Common.stop("id と 保存先のファイル名を指定します。")

id = Common.args()[0]
filePath = Common.args()[1]

try :
  extract(id, filePath)
except Exception as e :
  Common.esc_print("red", str(e))

print('Done.')
