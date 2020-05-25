#!/usr/bin/env python3
#  ~/bin フォルダのコマンドを Apps テーブルに挿入する。v1.1.0
from Py365Lib import Common, MySQL as my, FileSystem as fs
import os

S_IXUSR = 0o0100
S_IXGRP = 0o0010
S_IXOTH = 0o0001

# path が(オーナーが)実行可能か？
def isExecutable(path) :
  ret = False
  if Common.is_windows() :
    ret = path.endswith(".exe") or path.endswith(".bat") or or path.endswith(".ps1") or or path.endswith(".vbs")
  else :
    stinfo = os.stat(path)
    ret = stinfo.st_mode & S_IXUSR
  return ret

# path を テーブル Apps に挿入する。
def insertToApps(path) :
  title = fs.getFileName(path)
  platform = "linux"
  if Common.is_windows() :
    platform = "windows"
  sql = f"INSERT INTO Apps VALUES(NULL, '{title}', '{path}', '', '{platform}', '', '', CURRENT_DATE())"
  mysql.execute(sql)
  return

# START Program
settings = fs.readJson(fs.getCurrentDirectory() + '/InsApps.json')
binfolder = settings["binfolder"]

mysql = my.MySQL()

files = fs.listFiles2(binfolder)
for f in files :
  if isExecutable(f) :
    print(f)
    insertToApps(f)

print("終わり。")