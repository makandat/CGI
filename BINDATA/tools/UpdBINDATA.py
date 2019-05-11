#!/usr/bin/env python3
#  Binaries テーブルのバイナリデータ更新
import MySQL as mysql
import Text, Common
import FileSystem as fs
from pprint import pprint

UPDATE = "UPDATE BINDATA SET datatype='{1}', original='{2}', data={3} WHERE id={0}"

# バイナリーファイル filePath の内容でテーブル Binaries の data を更新する。
def updateBinaries(id, filePath) :
  ext = fs.getExtension(filePath)
  hexa = bin2hex(filePath)
  sql = Text.format(UPDATE, id, ext, filePath, hexa)
  client = mysql.MySQL()
  client.execute(sql)
  return

# バイナリーファイルをヘキサに変換する。
def bin2hex(filePath) :
  buff = "0x"
  b = fs.readBinary(filePath)
  buff += b.hex()
  return buff

# メイン
client = mysql.MySQL()
if Common.count_args() == 0 :
  id = Common.readline("対象の id を入力します。")
  if id == "" :
    Common.stop(1, "実行を中止しました。")
  filePath = Common.readline("画像ファイルのフルパス名を入力します。")
  if filePath == "" :
    Common.stop(1, "実行を中止しました。")
else :
  id = Common.args(0)
  filePath = Common.args(1)
if fs.exists(filePath) :
  updateBinaries(id, filePath)
  print("Done. " + filePath)
else :
  Common.esc_print("red", filePath + ' does NOT exists.')
