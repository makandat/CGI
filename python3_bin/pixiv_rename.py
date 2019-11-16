#!/usr/bin/python3
from Py365Lib import Common, FileSystem as fs, Text

# 指定されたフォルダの画像ファイルを同じ長さにリネームする。
def rename_files(folder) :
  # 画像ファイル一覧を得る。
  print(folder)
  files = fs.listFiles(folder, asstr=True)
  # 画像ファイルをリネーム
  for fpath in files :
    #fpath = Common.from_bytes(f)
    ext = fs.getExtension(fpath).lower()
    if ext == ".jpg" or ext == ".png" or ext == ".gif" :
      fname = fs.getFileName(fpath)
      ff = Text.split("_", fname)
      if len(ff) != 2 :
        print("Skipped " + fname)
        continue
      sf = ff[1]
      if len(ff[1]) == 6 and ff[1].startswith('p') :
        sf = "p0" + Text.substring(ff[1], 1)
        newname = folder + "/" + ff[0] + "_" + sf
        fs.move(fpath, newname)
        print("Renamed: " + newname)
      else :
        print("Passed: " + fpath)
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

# 指定されたフォルダの画像ファイルを同じ長さにリネームする。
rename_files(folder)

print("正常終了。")
