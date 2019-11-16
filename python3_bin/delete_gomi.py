#!/usr/bin/env python3
#  再帰的にゴミファイル (Thumbs.db, Desktop.ini) を削除する。
from Py365Lib import Common, FileSystem as fs

# パラメータを得る。
print("== 再帰的にゴミファイル (Thumbs.db, Desktop.ini) を削除する。==")
# 対象のフォルダを得る。
if Common.count_args() == 0 :
  Common.stop(9, "フォルダを指定してください。")
folder = Common.args(0)
a = Common.readline(folder + "に対して再帰的にゴミファイルを削除します。よろしいですか？ (y/n)")
if a != "y" :
  Common.stop(1, "実行を中止しました。")

# 実行する。
files = fs.listFilesRecursively(folder, asstr=True)
for f in files:
  if fs.getFileName(f) == "Thumbs.db" or fs.getFileName(f) == "Desktop.ini" :
    print("rm -v " + f)
  else :
    print(f)

print("終了。")
