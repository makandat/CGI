#!/usr/bin/env python3
#  ファイル一覧を PictureAlbum テーブルへインポートできるように CSV ファイルにする。
import FileSystem as fs
import Common

# START
# パラメータ確認
if Common.count_args() < 2 :
  Common.stop("Usage : fl2csv.py filelist csvfile")
filelist = Common.args(0)
csvfile = Common.args(1)
#  ファイルリストを読む。
lines = fs.readLines(filelist)
csvlines = ""
for line in lines :
  s = "NULL,0,title," + line + ",creator,,0,0\n"
  csvlines += s
# CSV ファイルに書く。
fs.writeAllText(csvfile, csvlines)
print("Done.")
 
