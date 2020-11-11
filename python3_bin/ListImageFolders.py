#!/usr/bin/env python3
#  画像ファイル (.jpg, .png, .gif) が含まれるディレクトリをリストアップする。(再帰的検索)
import os, sys, glob

# コマンドを先頭に付けるときは、下記の cmd を修正する。
cmd = ""
# 対象のディレクトリを得る。
path = ""
if len(sys.argv) == 1 :
  print("検索対象のディレクトリを指定してください。")
  exit(9)
else :
  path = sys.argv[1]
# ディレクトリ内を検索する。
print("Searching ..")
files = glob.glob(path + "/**", recursive=True)
dirset = set()
for f in files :
  if os.path.isfile(f) :
    p = os.path.splitext(f)
    if len(p) < 2 :
      pass
    else :
      ext = p[1].lower()
      if ext == ".jpg" or ext == ".png" or ext == ".gif" :
        dirset.add(cmd + os.path.dirname(f).replace("\\", "/"))
      else :
        pass
for d in dirset :
  print(d)
print("DONE.")
