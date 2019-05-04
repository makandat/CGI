# -*- code=utf-8 -*-
# Version 2.01  2019-04-23  Text クラス廃止
from typing import List, Tuple
import re

# 文字列のリスト
StrList = List[str]
StrTuple = Tuple[str]

# 文字列の長さ
def length(s:str) -> int:
  return len(s)

# 文字列の結合
def concat(str1:str, str2:str) -> str:
  return str1 + str2

# start から長さ length の部分文字列を返す。
def substring(text:str, start:int, length:int=-1) ->str:
  if length < 0 :
    return text[start:len(text)]
  else :
    return text[start:start+length]

# start から end までの部分文字列を返す。
def substr(text:str, start:int, end:int) ->str:
  return text[start:end+1]

# 先頭から長さ length の部分文字列を返す。
def left(text, length:str) -> str:
  return text[0 : length]

# 最後から長さ length の部分文字列を返す。
def right(text:str, length:int) -> str:
  n = len(text)
  begin = n - length
  return text[begin : n]

# 文字列 c を n 回繰り返した文字列をこのオブジェクトの値とする。
def times(c:str, n:int) -> str:
  return c * n

# 数字を判別
def isdigit(a: str) -> str:
  return a.isdigit()

# アルファベットを判別
def isalpha(a: str) -> str:
  return a.isalpha()

# 区切りを判別
def isdelim(a: str) -> str:
  return not a.isalnum()

# 表示可能かを判別
def isprint(a:str) ->bool:
  return a.isprintable()

# 小文字に変換
def tolower(s:str) -> bool:
  return s.lower()

# 大文字に変換
def toupper(s: str) -> bool:
  return s.upper()

# 前後の空白を取り除く
def trim(s: str) -> str:
  return s.strip()

# 後ろのCRやLFを取り除く
def chomp(s: str) -> str:
  if len(s) < 2 :
    return s
  last = len(s) - 1
  if s[last] == '\n' or s[last] == '\r' :
    s = s[0:last]
    last -= 1
    if s[last] == '\r' :
      s = s[0:last]
  return s

# 文字 c で文字列 s を分割してリストとして返す。
def split(c:bytes, s:str) -> StrList:
  return s.split(c)

# リスト array の要素を文字 c で連結する。
def join(c:str, array:list) -> str:
  strarray = []
  for a in array :
    if a == None :
      strarray.append("")
    else :
      strarray.append(str(a))
  return c.join(strarray)

# 文字列 s の中に部分文字列 p が含まれているか判別する。
def contain(p:str, s:str) -> bool:
  return (p in s)

# 文字列 s の中に部分文字列 p が含まれていればその位置を返す。
def indexOf(p:str, s:str) -> int:
  return s.find(p)

# 文字列 s に部分文字列 old が含まれていれば、それを new に置き換える。
def replace(old:str, new:str, s:str) -> str:
  return s.replace(old, new)

# 書式を含む文字列 form を *args (可変個数のパラメータ) で置き換える。
def format(form:str, *args: StrTuple) :
 return form.format(*args)

# 文字列 s を整数に変換する。
def parseInt(s:str) -> int:
 return int(s)

# 文字列 s を浮動小数点数に変換する。
def parseDouble(s:str) -> float:
 return float(s)

# 256未満の整数を文字に変換する。
def char(n:int) -> str:
 return chr(n)

# 文字を256未満の整数に変換する。
def asc(a:str) -> int:
  return ord(a)

#    正規表現を使う静的メソッド
# 正規表現 rstr が文字列 s に含まれるか判別する。
def re_contain(rstr:str, s:str) -> bool :
  ro = re.compile(rstr)
  m = ro.match(s)
  return m != None

# 正規表現 rstr が文字列 s に含まれていれば、その一致した部分文字列の集合を返す。
def re_search(rstr:str, s:str) -> re.match :
  ro = re.compile(rstr)
  m = ro.search(s)
  return m

# 正規表現 rstr が文字列 s に含まれていれば、その部分文字列で分割してリストとして返す。
def re_split(rstr:str, s:str) -> StrList :
  m = re.split(rstr, s)
  return m

# 正規表現 rstr が文字列 s に含まれていれば、その部分文字列を c で置き換える。
def re_replace(rstr:str, c:str, s:str) -> str :
  ro = re.compile(rstr)
  return ro.sub(c, s)

# 数(整数または浮動小数点数) d に3桁ごとにカンマを挿入した文字列を返す。
def money(d:float) -> str :
  m = '{0:,}'.format(d)
  return m

# bytes(バイト列)を文字列に変換する。
def b2s(b: bytes) -> str :
  return b.decode()

# 文字列(utf-8)をバイト列に変換する。
def s2b(s: str) -> bytes :
  return s.encode()

