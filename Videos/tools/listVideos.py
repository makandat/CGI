#!/usr/bin/python3
from Py365Lib import Common, FileSystem as fs
import pathlib
import os

# ビデオ拡張子一覧
VExts = ['.mp4', '.avi', '.mpg', '.wmv', '.mov', '.mkv', '.flv', '.3gp']

# Videos テーブルのフィールド
VTF = "INSERT INTO Videos VALUES(NULL,'{0}','{1}','不明','','','', 0, 0, 0, 0);"

# パラメータチェック
if Common.count_args() == 0 :
  folder = Common.readline('検索対象のフォルダを指定してください。')
else :
  folder = Common.args(0)

# ディレクトリの存在チェック
if not fs.isDirectory(folder) :
  Common.stop(1, folder + " が見つかりません。")

#print('OK')

# 再帰的にファイルを取得する。
pobj = pathlib.Path(folder)  # Generator を取得
files = pobj.glob('**/*.*')  # PosixPath のコレクション
for f in files :
  if f.is_file() and fs.getExtension(f) in VExts :
    path = str(f).replace("\\", "/").replace("'", "''")
    title = fs.getFileName(f).split('.')[0].replace("'", "''")
    # SQL を表示 (リダイレクトを使ってファイル保存)
    print(VTF.format(title, path))

# print("終わり")
