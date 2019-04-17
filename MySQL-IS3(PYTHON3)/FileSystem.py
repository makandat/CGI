# FileSystem.py
# Version 1.12  2018-12-14
import os
import shutil
import glob
from pathlib import Path
import tempfile
import pwd
import grp
import csv
import json
from typing import Callable, List, Dict, Any

StrList = List[str]

# テキストファイルを読んでその内容を返す。
def readAllText(file: str) -> str :
  f = open(file, mode="r", buffering=-1, encoding="utf8")
  s = f.read()
  f.close()
  return s

# テキストをファイルに書く。
def writeAllText(file: str, text: str, append:bool=False) -> None:
  if append == True :
    with open(file, "a") as f :
      f.write(text)
  else :
    with open(file, "w") as f :
      f.write(text)
  return

# ファイルを１行づつ読んで callback で処理する。
def readAllLines(file: str, callback: Callable) -> None:
  with open(file) as f :
    for line in f:
      callback(line.rstrip())
  return

# バイナリーファイルを読む。
def readBinary(file: str) -> bytes:
  b = None
  with open(file, "rb") as f :
    b = f.read()
  return b

# バイナリーファイルを書く。
def writeBinary(file: str, data: bytes) :
  with open(file, mode='wb') as f :
    f.write(data)
  return

# INI ファイルを読む。
def readIni(file: str) -> Dict:
  map = {}
  with open(file) as f :
    for s in f :
      if not ("=" in s) :
        continue
      kv = s.split('=')
      key = kv[0].strip()
      value = kv[1].strip()
      map[key] = value
  return map

# ファイルをコピーする。
def copy(src: str, dest:str) ->None:
  shutil.copy(src, dest)
  return

# ファイルを移動する(名前の変更)
def move(src:str, dest:str) -> None:
  shutil.move(src, dest)
  return

# ファイルやリンクを削除する。
def unlink(file:str) -> None:
  os.unlink(file)
  return

# ファイルやディレクトリが存在するか調べる。
def exists(file:str) -> bool:
  return os.path.exists(file)

# ファイルが存在するか調べる。
def isFile(file:str) -> bool:
  return os.path.isfile(file)

# ディレクトリが存在するか調べる。
def isDirectory(dir:str) -> bool:
  return os.path.isdir(dir)

# リンクかどうか調べる。
def isLink(path:str) -> bool:
  return os.path.islink(path)

# ファイルやディレクトリの属性を得る。
def getAttr(path:str) -> int:
  return os.stat(path).st_mode

# ファイルやディレクトリのオーナーを得る。
def getOwner(path:str) -> str:
  uid = os.stat(path).st_uid
  name = pwd.getpwuid(uid).pw_name
  return name

# ファイルやディレクトリのグループを得る。
def getGroup(path:str) -> str:
  gid = os.stat(path).st_gid
  name = grp.getgrgid(gid).gr_name
  return name

# カレントディレクトリを変更する。
def chdir(dir:str) -> None:
  os.chdir(dir)
  return

# ディレクトリを作成する。
def mkdir(dir:str) -> None:
  try :
    os.mkdir(dir)
  except :
    os.makedirs(dir)
  return

# ディレクトリを削除する。
def rmdir(dir:str) -> None:
  try :
    os.rmdir(dir)
  except :
    shutil.rmtree(dir)
  return

# ファイル内の文字列を検索する。(行番号のリストを返す)
def grep(str:str, file:str) -> List:
  result = []
  with open(file) as f :
    for i, line in enumerate(f) :
      if str in line :
        result.append(i)
  return result

# 指定したワイルドカードでディレクトリ内を検索する。
def listFiles(dir:str, wildcard:str="*") -> List:
  list = glob.glob(dir + "/" + wildcard)
  result = []
  for item in list :
    if os.path.isfile(item) :
      result.append(item)
  return result

# ディレクトリ一覧を得る。
def listDirectories(dir:str) -> List:
  list = os.listdir(dir)
  result = []
  for item in list :
    fpath = dir + "/" + item
    if os.path.isdir(fpath) :
      result.append(fpath)
  return result

# パス名の中でファイル名部分を返す。
def getFileName(path:str) -> str:
  return os.path.basename(path)

# パス名の中でディレクトリ名部分を返す。
def getDirectoryName(path:str) -> str:
  return os.path.dirname(path)

# パス名の中で拡張子部分を返す。
def getExtension(path: str) -> str:
 p = os.path.splitext(path)
 if len(p) >= 2 :
   ext = p[1]
 else :
   ext = ""
 return ext

# 拡張子を変更する。(ext は新しい拡張子。先頭はドットであること)
def changeExt(path:str, ext:str) -> str:
  p = os.path.splitext(path)
  return p[0] + ext

# 相対パスから絶対パスを得る。
def getAbsolutePath(path:str) -> str:
  return os.path.abspath(path)

# 親のディレクトリを得る。
def getParentDirectory(path:str) -> str:
  return Path(path).parent

# カレントディレクトリを得る。
def getCurrentDirectory() -> str:
  return os.getcwd()

# 一時ファイル(パス名)を得る。
def getTempFile() -> str:
  return tempfile.NamedTemporaryFile().name

# CSV ファイルを読む。
def readCsv(path:str, header:bool=True, delim:str=",", lterm:str="\n") -> List[StrList]:
  rows = []
  with open(path, "r") as fcsv :
    f = csv.reader(fcsv, delimiter=delim , doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    if header :
      next(f)  # ヘッダー読み飛ばし
    for row in f :
       rows.append(row)
  return rows

# JSON ファイルを読む。
def readJson(path:str) -> Any:
  data = None
  with open(path, "r") as f :
    str = f.read()
    data = json.loads(str)
  return data

# JSON ファイルに書く。
def writeJson(path:str, data:Any, pretty:bool=False) -> None:
  if pretty :
    str = json.dumps(data, sort_keys=True, indent=2)
  else :
    str = json.dumps(data)
  with open(path, "w") as f :
    f.write(str)
  return
