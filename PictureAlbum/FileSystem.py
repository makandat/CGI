# FileSystem.py
# Version 1.21  2019-04-21
import os, io, sys
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
    with open(file, "a", encoding="utf-8") as f :
      f.write(text)
  else :
    with open(file, "w", encoding="utf-8") as f :
      f.write(text)
  return

# ファイルを読んで行の配列として返す。
def readLines(file: str, encode='utf-8') :
  lines = list()
  with open(file, mode='r', encoding=encode) as f:
    line = f.readline().rstrip()
    while line :
      lines.append(line)
      line = f.readline().rstrip()
  return lines
    
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
  shutil.copy(src.encode('utf-8'), dest.encode('utf-8'))
  return

# ファイルを移動する(名前の変更)
def move(src:str, dest:str) -> None:
  shutil.move(src.encode('utf-8'), dest.encode('utf-8'))
  return

# ファイルやリンクを削除する。
def unlink(file:str) -> None:
  os.unlink(file.encode('utf-8'))
  return

# ファイルやディレクトリが存在するか調べる。
def exists(file:str) -> bool:
  return os.path.exists(file.encode('utf-8'))

# ファイルが存在するか調べる。
def isFile(file:str) -> bool:
  return os.path.isfile(file.encode('utf-8'))

# ディレクトリが存在するか調べる。
def isDirectory(dir:str) -> bool:
  return os.path.isdir(dir.encode('utf-8'))

# リンクかどうか調べる。
def isLink(path:str) -> bool:
  return os.path.islink(path.encode('utf-8'))

# ファイルサイズを得る。
def getFileSize(path) :
  return os.path.getsize(path.encode('utf-8'))


# ファイルやディレクトリの属性を得る。
def getAttr(path:str) -> int:
  return os.stat(path.encode('utf-8')).st_mode

# ファイルやディレクトリの最終更新日時を得る。
def getLastWrite(path:str, utc:bool=True) -> str:
  mtime = os.stat(path.encode('utf-8')).st_mtime
  JST = timezone(timedelta(hours=+9), 'JST')
  if utc :
    time = datetime.fromtimestamp(mtime, timezone.utc)
  else :
    time = datetime.fromtimestamp(mtime, JST)
  stime = time.strftime("%Y-%m-%d %H:%M:%S")
  return stime

# ファイルやディレクトリのオーナーを得る。
def getOwner(path:str) -> str:
  uid = os.stat(path.encode('utf-8')).st_uid
  name = pwd.getpwuid(uid).pw_name
  return name

# ファイルやディレクトリのグループを得る。
def getGroup(path:str) -> str:
  gid = os.stat(path.encode('utf-8')).st_gid
  name = grp.getgrgid(gid).gr_name
  return name

# カレントディレクトリを変更する。
def chdir(dir:str) -> None:
  os.chdir(dir.encode('utf-8'))
  return

# ディレクトリを作成する。
def mkdir(dir:str) -> None:
  try :
    os.mkdir(dir.encode('utf-8'))
  except :
    os.makedirs(dir.encode('utf-8'))
  return

# ディレクトリを削除する。
def rmdir(dir:str) -> None:
  try :
    os.rmdir(dir.encode('utf-8'))
  except :
    shutil.rmtree(dir.encode('utf-8'))
  return

# ファイル内の文字列を検索する。(行番号のリストを返す)
def grep(str:str, file:str) -> List:
  result = []
  with open(file.encode('utf-8')) as f :
    for i, line in enumerate(f) :
      if str in line :
        result.append(i)
  return result

# 指定したワイルドカードでディレクトリ内を検索する。
def listFiles(dir:str, wildcard:str="*") -> List:
  diru8 = dir.encode('utf-8')
  list = glob.glob(diru8 + b"/" + wildcard.encode('utf-8'))
  result = []
  for item in list :
    if os.path.isfile(item) :
      result.append(item)
  return result

# ディレクトリ一覧を得る。
def listDirectories(dir:str) -> List:
  diru8 = dir.encode('utf-8')
  list = os.listdir(diru8)
  result = []
  for item in list :
    fpath = bytearray(diru8) + b"/" + item
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

# フルパスの中から一番下のディレクトリを得る。
def getThisDirectory(path:str) -> str :
  path1 = path.decode('utf-8')
  parts = path1.split('/')
  n = len(parts)
  if n <= 1 :
    return path1
  else :
    return parts[n-1]

# カレントディレクトリを得る。
def getCurrentDirectory() -> str:
  return os.getcwd()

# ホームディレクトリを得る。
def getHomeDirectory() -> str :
  return str(Path.home())

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
