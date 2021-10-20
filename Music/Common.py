# -*- coding: utf-8 -*-
# Common.py
#   ver 2.70  2021-09-18
import sys, os, io, time, json
import linecache
import subprocess
import logging
if not os.name == 'nt' :
  import syslog
from typing import List, Any, Callable
from pprint import pprint

# ログファイルの名前
LOGFILE = 'Py365Lib.log'
logger = None

# 端末エスケープシーケンス指定コード
ESC_NORMAL = "\x1b[0m"
ESC_BOLD = "\x1b[1m"
ESC_DIM = "\x1b[2m"
ESC_ITALIC = "\x1b[3m"
ESC_UNDERLINE = "\x1b[4m"
ESC_BLINK = "\x1b[5m"
ESC_HBLINK = "\x1b[6m"
ESC_REVERSE = "\x1b[6m"
ESC_FG_BLACK = "\x1b[30m"
ESC_BG_BLACK = "\x1b[40m"
ESC_FG_RED = "\x1b[31m"
ESC_BG_RED = "\x1b[41m"
ESC_FG_GREEN = "\x1b[32m"
ESC_BG_GREEN = "\x1b[42m"
ESC_FG_YELLOW = "\x1b[33m"
ESC_BG_YELLOW = "\x1b[43m"
ESC_FG_BLUE = "\x1b[34m"
ESC_BG_BLUE = "\x1b[44m"
ESC_FG_MAGENTA = "\x1b[35m"
ESC_BG_MAGENTA = "\x1b[45m"
ESC_FG_CYAN = "\x1b[36m"
ESC_BG_CYAN = "\x1b[46m"
ESC_FG_WHITE = "\x1b[37m"
ESC_BG_WHITE = "\x1b[47m"

# 文字列のリスト
StrList = List[str]


# ロガー初期化
def init_logger(filename=None, level=logging.DEBUG):
  global logger
  if filename == None :
    filename = LOGFILE
  logger = logging.getLogger('Py365Lib')
  logger.setLevel(level)
  # ファイルハンドラを作成
  fh = logging.FileHandler(filename)
  fh.setLevel(logging.DEBUG)
  # フォーマッタを作成して、ハンドラに結び付ける。
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  # ロガーにハンドラを結びつける。
  logger.addHandler(fh)
  logger.info("=== Start Logging ====")
  return


# コマンド引数のリストを返す。
def args(ix=-1) -> StrList:
  n = len(sys.argv)
  a = []
  if n > 1 :
    for i in range(1, n) :
      a.append(sys.argv[i])
  if ix < 0 :
    return a
  else :
    return a[ix]

# コマンド引数の数
def count_args() -> int:
  return len(sys.argv) - 1

# プログラムの実行を停止する。
def stop(code:int = 0, message:str ="", color:str="") -> None :
  if message != "" :
    esc_print(color, message)
  exit(code)

# コマンドを起動する。(cmd は配列)
def exec(cmd:StrList) -> int:
  if type(cmd) is str :
    cmd_a = [cmd]
  else :
    cmd_a = cmd
  return subprocess.check_call(cmd_a)

# コマンドを起動して、その結果を返す。(cmd は配列)
def shell(cmd:StrList) -> str:
  if type(cmd) is str :
    cmd_a = [cmd]
  else :
    cmd_a = cmd
  return subprocess.check_output(args=cmd_a)

# ログ情報出力
def log(msg:str) -> None:
  logger.info(str(msg))

# ログエラー出力
def error(msg:str) -> None:
  logger.error(str(msg))

# 例外発生時の詳細情報
def errorInfo() :
  exc_type, exc_obj, tb = sys.exc_info()
  f = tb.tb_frame
  lineno = tb.tb_lineno
  filename = f.f_code.co_filename
  linecache.checkcache(filename)
  line = linecache.getline(filename, lineno, f.f_globals)
  return (filename, lineno, line.strip(), exc_obj)

# 変数が有効かどうか
def isset(v:Any) -> bool:
  return v != None

# 変数が無効かどうか
def isnull(v:Any) -> bool :
  return v == None

# 変数が文字列かどうか
def is_str(x:Any) -> bool:
  return (type(x) is str)

# 変数が整数かどうか
def is_int(x:Any) -> bool:
  return (type(x) is int)

# 変数が浮動小数点数かどうか
def is_float(x:Any) -> bool:
  return (type(x) is float)

# 変数がブール数かどうか
def is_bool(x:Any) -> bool:
  return (type(x) is bool)

# syslog
def syslog_out(msg: str) -> None:
  syslog.syslog(msg)

# タイマー
def set_timeout(sec:float, handler:Callable) -> None :
  time.sleep(sec)
  handler()

# スリープ
def sleep(sec:float) -> None :
  time.sleep(sec)

# 環境変数
def get_env(key:str) -> str:
  return os.environ[key]

# OS 判別 (実行環境が Windows なら True)
def is_windows() -> bool:
  return os.name == 'nt'

# バイト列と文字列変換
def to_bytes(s:str) -> bytes:
  return s.encode(encoding='utf-8')

# バイト列から文字列に変換
def from_bytes(b:bytes) -> str :
  return b.decode(encoding='utf-8')

# エスケープシーケンス出力
def esc_print(code:Any, text:str, reset:bool=True) -> None:
  if is_str(code) and code != "" :
    if code == "red" :
      code = ESC_FG_RED
    elif code == "green" :
      code = ESC_FG_GREEN
    elif code == "blue" :
      code = ESC_FG_BLUE
    elif code == "cyan" :
      code = ESC_FG_CYAN
    elif code == "magenta" :
      code = ESC_FG_MAGENTA
    elif code == "yellow" :
      code = ESC_FG_YELLOW
    elif code == "bold" :
      code = ESC_BOLD
    elif code == "underline" :
      code = ESC_UNDERLINE
    elif code == "reverse" :
      code = ESC_REVERSE
    else :
      pass
  else :  # code はタプルとする。
    cc = ""
    for x in code :
      cc += x
    code = cc
  text = str(text)
  if reset :
    print(code + text + "\x1b[m")
  else :
    print(code + text)
  return

# 文字列入力
def readline(message:str=None) -> str :
  if isset(message) :
    print(message)
  s = input()
  return s

# json データをオブジェクトに変換する。
def from_json(jsonText:str) -> Any:
  d = json.loads(jsonText)
  return d

# オブジェクトを json データに変換する。
def to_json(obj: Any) -> str:
  text = json.dumps(obj, indent=4)
  return text

# ファイル内容を表示する。
def printFile(filePath, code="utf-8") :
  try :
    with open(filePath, "r", encoding=code) as f :
      text = f.read()
      print(text)
  except :
    print("ファイルを開けません。")
  return

# 配列や連想配列を表示する。
def printArray(arr) :
  pprint(arr, indent=2, width=150)
  return

# オブジェクトの文字列表現を返す。
def get_objstring(obj) :
  buff = io.StringIO()
  pprint(obj, stream=buff)
  s = buff.getvalue()
  return s


# ----------------------------------------------------
# メインとして実行しようとしたとき
# ----------------------------------------------------
if __name__ == "__main__" :
	pass
