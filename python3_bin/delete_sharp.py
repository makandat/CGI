#!/usr/bin/env python3
from Py365Lib import Common, FileSystem as fs
#  ファイル名に含まれる #, + を削除する。

#  ファイル名からシャープとプラスを削除
def delete_badchars(folder) :
  # 画像ファイル一覧を得る。
  print(folder)
  files = fs.listFiles(folder, asstr=True)
  # 画像ファイルをリネーム
  for fpath in files :
    #fpath = Common.from_bytes(f)
    ext = fs.getExtension(fpath).lower()
    if ext == ".jpg" or ext == ".png" or ext == ".gif" :
      fpath_new = fpath.replace("#", "").replace("+", "")
      if fpath != fpath_new :
        print("mv -v '" + fpath + "' '" + fpath_new + "'")
    else :
      print("Non image passed: " + fpath)
  return  



#  スタート
if Common.count_args() == 0 :
  folder = Common.readline("対象の画像フォルダを入力します。")
else :
  folder = Common.args(0)

if not fs.isDirectory(folder) :
  Common.stop(1, folder + " は正しいディレクトリではありません。")

# 指定されたフォルダのファイルパスからシャープとプラスを削除
delete_badchars(folder)

print("正常終了。")

