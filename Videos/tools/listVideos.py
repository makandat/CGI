#!/usr/bin/python3
from Py365Lib import Common, FileSystem as fs
import pathlib

# ビデオ拡張子一覧
VExts = ['.mp4', '.avi', '.mpg', '.wmv', '.mov', '.mkv', '.flv']

# Videos テーブルのフィールド
VTF1 = "INSERT INTO Videos VALUES(NULL,'TITLE','"
VTF2 = "','','','','', 0, 0, 0, 0);"

# パラメータチェック
if Common.count_args() == 0 :
  folder = Common.readline('検索対象のフォルダを指定してください。')
else :
  folder = Common.args(0)

# ディレクトリの存在チェック
if not fs.isDirectory(folder) :
  Common.stop(1, folder + " が見つかりません。")

print('OK')

# 再帰的にファイルを取得する。
pobj = pathlib.Path(folder)  # Generator を取得
files = pobj.glob('**/*.*')  # PosixPath のコレクション
for f in files :
  if f.is_file() and fs.getExtension(f) in VExts :
    print(VTF1 + str(f) + VTF2)

print("終わり")
