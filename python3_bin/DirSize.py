#!/usr/bin/env python3
#  ディレクトリ内のファイルサイズの合計と最新及び最古のファイルの日付を得る。(サブディレクトリは含まない)
import sys, os, datetime


# 対象ディレクトリを得る。
path = "."
if len(sys.argv) == 1 :
  print("使い方： python DirSize.py 対象のディレクトリ\n")
  exit(9)
else :
  path = sys.argv[1]

# 対象ディレクトリ内のファイル一覧を得る。
files = os.listdir(path)
only_files = [f for f in files if os.path.isfile(os.path.join(path, f))]
# ファイルサイズの合計を得る。
sum_of_sizes = 0
newest_date = datetime.datetime(2000, 1, 1).timestamp()
oldest_date = datetime.datetime(2050, 1, 1).timestamp()
newest_file = ""
oldest_file = ""
# ディレクトリに含まれるファイルすべてに対して繰り返す。
for f in only_files :
  # ファイルサイズを合計
  file = path + "/" + f
  sum_of_sizes += os.path.getsize(file)
  # ファイルの日付を得る。
  file_date = os.path.getmtime(file)
  # 最古ファイルを得る。
  if file_date < oldest_date :
    oldest_date = file_date
    oldest_file = f
  # 最新ファイルを得る。
  if file_date > newest_date :
    newest_date = file_date
    newest_file = f
# 結果を表示する。
if sum_of_sizes == 0 :
  print(path + " ファイルがありません。")
else :
  bytes = "{:,}".format(sum_of_sizes)
  print(f"{path} total {bytes} bytes {datetime.datetime.fromtimestamp(oldest_date)} {datetime.datetime.fromtimestamp(newest_date)}")