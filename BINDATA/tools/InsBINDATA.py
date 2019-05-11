#!/usr/bin/env python3
#  バイナリーファイルをテーブル BINDATA に挿入する。
#  *.png, *.jpg などを使えるようにした。
import Common
import FileSystem as fs
from MySQL import MySQL
import Text
from pprint import pprint

INSERT = "INSERT INTO BINDATA(`title`, `original`, `datatype`, `data`, `info`, `size`) VALUES('{0}', '{1}', '{2}', {3}, '', {4})"

# バイナリーファイル filePath をテーブル BINDATA に挿入する。
def insertBinaries(filePath) :
  ext = fs.getExtension(filePath)
  size = fs.getFileSize(filePath)
  fileName = fs.getFileName(filePath)
  filePath = filePath.replace("\\", "/")
  filePath = filePath.replace("'", "''")
  hexa = bin2hex(filePath)
  sql = Text.format(INSERT, fileName, filePath, ext, hexa, size)
  client = MySQL()
  client.execute(sql)
  return

# バイナリーファイルをヘキサに変換する。
def bin2hex(filePath) :
  buff = "0x"
  b = fs.readBinary(filePath)
  buff += b.hex()
  return buff
  
# メイン
if Common.count_args() == 0 :
  Common.stop("ファイルを指定してください。ワイルドカードを指定するときは ' で囲ってください。")

# ファイルパスを得る。
filePath = Common.args(0)
if "*" in filePath :
  # ワイルドカードを指定したとき、ファイル一覧を取得
  dirPath = fs.getDirectoryName(filePath)
  wildcard = fs.getFileName(filePath)
  files = fs.listFiles(dirPath, wildcard)
  for file in files :
    filename = file.decode('utf-8')
    print(filename)
    insertBinaries(filename)
else :
  # 単一ファイルのとき
  if fs.exists(filePath) :
    insertBinaries(filePath)
    print('Done. ' + filePath)
  else :
    Common.esc_print("red", filePath + ' does NOT exists.')
