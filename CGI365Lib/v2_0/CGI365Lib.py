# CGI356Lib.py v2.0.5  2024-09-22
import os, sys, datetime, io
import subprocess
from subprocess import PIPE
import urllib.parse as urlp
import pathlib
import json
from pprint import pprint

# ---------------- 定数 ----------------------
# 文字コード
ENC = 'utf-8'

# デバッグ用ログファイル Debug log file def to be modified
if os.name == 'nt':
  LOG = "C:/temp/CGI365Lib.log"
  #LOG = ""
else:
  LOG = ""

# ステータスコード
OK = "200 OK"
BAD_REQUEST = "400 Bad Request"
FORBIDDEN = "403 Forbidden"
NOT_FOUND = "404 Not Found"
METHOD_NOT_ALLOWED = "405 Method Not Allowed"
INTERNAL_SERVER_ERROR = "500 Internal Server Error"
NOT_IMPLEMENTED = "501 Not Implemented"

# --------------- コンソールデバッグ支援 --------------

# GET デバッグ 判別
def _isDebugGET():
  ret = False
  if len(sys.argv) > 1 :
    if sys.argv[1] == "debug_get":
      ret = True
    else:
      pass
  return ret

# POST デバッグ 判別
def _isDebugPOST():
  ret = False
  if len(sys.argv) > 1 :
    if sys.argv[1] == "debug_post":
      ret = True
    else:
      pass
  return ret

# デバッグかどうか
def _isDebug():
  return _isDebugGET() or _isDebugPOST()

# デバッグ用ログ出力
def info(obj, name=""):
  if LOG == "":
    return
  now = datetime.datetime.now()
  strnow = now.isoformat()
  stobj = str(obj)
  with open(LOG, mode="at") as f:
    f.write(f"{strnow} {name}: {stobj}\n")
  return

def log(obj, name=""):
  info(obj, name)
  return

# ---------------- HTML タグ作成 -----------------------
# タグで囲む。
def tag(t, s, c=""):
  tg = f"<{t}"
  if c == "":
    tg += ">"
  else:
    tg += f" class=\"{c}\">"
  tg += f"{s}</{t}>\n"
  return tg

# Anchor で囲む
def anchor(url, s, target=""):
  an = f"<a href=\"{url}\""
  if target == "":
    an += ">"
  else:
    an += f" target=\"{target}\">"
  an += f"{s}</a>"
  return an
  
# Windows 判別
def isWindows():
  return os.name == 'nt'



# --------------------------------------------------------------------
#   Request class
# --------------------------------------------------------------------
class Request:
  def __init__(self, parse=False):
    self.__Body = self._getBody()       #  POST で受け取った生データ (bytes)
    self.__QueryString = self._getQueryString()  #  GET で受け取った環境変数 QUERY_STRING (str)
    self.__Method = self._getMethod()   #  HTTP メソッド 'GET', 'POST' (str)
    self.__Headers = self._getHeaders() #  リクエストヘッダ辞書 (dict[str, str])
    self.__Dispositions = self._getDispositions() # マルチパートフォームのブロックのリスト (list[bytes])
    self.__Query = dict()  # GET メソッドの時のパラメータ dict[str, str]
    self.__Form = dict()  # POST or GET メソッドの時のパラメータ dict[str, str]
    self.__Files = list() # マルチパートデータにファイルが含まれていた場合のファイル情報 (list[(name, filename, chunk)]
    self._parser()       #  パラメータ 辞書を作成する。
    self.__Cookies = self._getCookies()   #  クッキー 辞書 (dict[str, str])
    return
  
  # 環境変数 QUERY_STRING を得る。  
  def _getQueryString(self) -> str:
    if _isDebugGET():
      print("Enter QUERY_STRING > ", end="")
      s = input()
      return s
    else:
      return os.getenv("QUERY_STRING", "")

  # HTTP メソッドを得る。
  def _getMethod(self) -> str:
    method = ""
    if _isDebugGET():
      method = "GET"
    elif _isDebugPOST():
      method = "POST"
    else:
      method = os.getenv("REQUEST_METHOD", "")
    return method
    
  # リクエストヘッダを得る。
  def _getHeaders(self) -> dict:
    headers = dict()
    if _isDebug():
      print("Enter Request Headers > ", end="")
      s = input()
      if s != "":
        headers = json.loads(s)
    else:
      keys = os.environ.keys()
      for key in keys:
        val = os.getenv(key)
        if key.startswith("HTTP_"):
          k = key[5:].lower()
          headers[k] = val
        if key.startswith("CONTENT_TYPE"):
          headers["content_type"] = val
    return headers
    
  # リクエストクッキーを得る。
  def _getCookies(self) -> dict:
    cookies = dict()
    http_cookie = ""
    if _isDebug():
      print("Enter request Cookie > ", end="")
      http_cookie = input()
    else:
      http_cookie = os.getenv("HTTP_COOKIE", "")
    cookielist = http_cookie.split('; ')
    for item in cookielist:
      kv = item.split('=', 1)
      if len(kv) == 2:
        k = kv[0]
        v = urlp.unquote(kv[1])
        cookies[k] = v
    return cookies
     
  # POST body を得る。
  def _getBody(self) -> bytes:
    buffer = b""
    if _isDebugGET(): # デバッグ GET メソッドの場合は戻り
      return buffer
    elif _isDebugPOST(): # デバッグ POST の場合はキー入力またはファイル入力
      print("Enter BODY 1-line or from @file_path > ", end="")
      s = input()
      if s.startswith("@"):  # ファイルから読む。
        filepath = s[1:]
        with open(filepath, "r") as f:
          buffer = f.read()
      else:
        buffer = s.encode()  
    else: # ノーマルの場合は標準入力を読む。
      buffer = sys.stdin.buffer.read()
    return buffer

  # マルチパートボディか判別する。
  def _isMultipart(self):
    b = self.content_type.find("multipart") >= 0
    return b

  # マルチパートデータを境界線で区切ったブロックのリストを得る。
  def _getDispositions(self) -> list[bytes]:
    if not self._isMultipart():
      return list()
    blocks = self.__Body.split(self.boundary)
    if blocks[len(blocks) - 1] == b"--\r\n":
      blocks.pop()
    if blocks[0] == b"":
      blocks.pop(0)
    return blocks

  # リクエストデータが JSON かどうかを返す。
  def _isJSON(self):
    return self.content_type.startswith("application/json")
      
  # リクエストデータが BLOB (octed-stream) かどうかを返す。
  def _isBLOB(self):
    return self.content_type.startswith("application/octed-stream")
  

  # x-www-urlencoded 形式のデータを辞書化する。_parseQuery で使用。
  def _getQuery(self, src=None):
    if src is None:
      src = self.__QueryString
    data = dict()
    exprs = src.split("&")
    for e in exprs:
      kv = e.split("=", 1)
      if len(kv) == 2:
        key = kv[0]
        val = urlp.unquote_plus(kv[1])
        if key in data:
          data[key] += f",{val}"
        else:
          data[key] = val
    return data

  # クエリーデータ (x-www-urlencoded) を辞書に変換して self.__Query と self.__Form に格納する。(POSTの場合も可能)
  def _parseQuery(self):
    if self._isJSON() or self._isBLOB():
      return  dict()
    src = ""
    if self.method == "POST" and self._isMultipart() == False:
      src = self.body.decode()
    elif self.method == "GET":
      src = self.__QueryString
    else:
      return dict()
    if src == "":
      return dict()
    self.__Query = self._getQuery(src)
    self.__Form = self.__Query
    return

  # Body が JSON の場合、辞書に変換して self.__Form に格納する。
  def _parseJSON(self):
    s = self.body.decode()
    self.__Form = json.loads(s)
    return

  # マルチパートのブロックにファイルが含まれているか？
  def _isChunkBlock(self, block) -> bool:
    lines = block.split(b"\r\n", 3)
    if lines[0] == b"":
      lines.pop(0)
    b = lines[0].startswith(b"Content-Disposition: ") and lines[0].find(b"filename=") > 0
    return b
    
  # マルチパートのブロックに単純な文字列 (データ) が含まれているか？
  def _isValueBlock(self, block) -> bool:
    lines = block.split(b"\r\n", 2)
    if lines[0] == b"":
      lines.pop(0)
    return lines[0].startswith(b"Content-Disposition: ") and lines[0].find(b"filename=") < 0
    
  # マルチパートのブロックの name を得る。
  def _getBlockName(self, block) -> str:
    lines = block.split(b"\r\n", 2)
    if lines[0] == b"":
      lines.pop(0)
    ss = lines[0].split(b'name="')
    s = ss[1]
    p = s.find(b'"')
    name = s[0:p].decode()
    return name

  # マルチパートのブロックの filename を得る。
  def _getBlockFileName(self, block) -> str:
    lines = block.split(b"\r\n", 2)
    if lines[0] == b"":
      lines.pop(0)
    ss = lines[0].split(b'; filename="')
    s = ss[1]
    p = s.find(b'"')
    filename = s[0:p].decode()
    return filename

  # マルチパートのブロックの chunk を得る。
  def _getBlockChunk(self, block) -> bytes:
    lines = block.split(b"\r\n", 3)
    if lines[0] == b"":
      lines.pop(0)
    chunk = lines[2]
    if chunk.startswith(b"\r\n"):
      chunk = chunk[2:]
    if chunk.endswith(b"\r\n"):
      chunk = chunk[0:-2]
    return chunk

  # マルチパートのブロックの value を得る。
  def _getBlockValue(self, block) -> str:
    lines = block.split(b"\r\n", 3)
    if lines[0] == b"":
      lines.pop(0)
    value = lines[2]
    if value.endswith(b"\r\n"):
      value = value[0:-2].decode()
    return value

  # マルチパートフォームデータ (multipart/form-data) を辞書 (self.form) とアップロードファイル (self.files) に変換する。
  def _parseMultipartBody(self):
    if self.method != "POST":
      return
    if self._isMultipart() == False or self._isJSON() or self._isBLOB():
      return
    self.__Form.clear()
    blocks = self.__Dispositions
    for block in blocks:
      if self._isChunkBlock(block):
        name = self._getBlockName(block)
        filename = self._getBlockFileName(block)
        chunk = self._getBlockChunk(block)
        g = (name, filename, chunk)
        self.__Files.append(g)
      elif self._isValueBlock(block):
        name = self._getBlockName(block)
        value = self._getBlockValue(block)
        self.__Form[name] = value
      else:
        pass
    return

  # POST された body からパラメータの辞書を作成する。
  def _parser(self) -> dict:
    if self._isBLOB():
      return
    if self._isMultipart():
      self._parseMultipartBody() # multipart/form-data
    elif self._isJSON():
      self._parseJSON() # application/json
    else:
      self._parseQuery() # application/x-www-urlencoded
    return

  # POST された body からアップロードファイルのリストを作成する。(type="file"の場合)
  def _getFiles(self) -> list[tuple]:
    files = list()
    for block in self.__Dispositions:
      if self._isChunkBlock():
        name = self._getBlockName(block)
        filename = self._getBlockFileName(block)
        chunk = self._getBlockChunk(block)
        files.append((name, filename, chunk))
    return files
    
  # 
  # CGI パラメータを得る。キーが存在しないときは空文字を返す。
  def getParam(self, key:str, unEsc=True, plus=False) -> str:
    if self.method == "GET":
      if key in self.query:
        val = self.query[key]
        if isWindows():
          val = val.replace("\\", "\\\\")
        if unEsc == True and plus == True:
          return urlp.unquote_plus(val)
        elif unEsc == True and plus == False:
          return urlp.unquote(val)
        else:
          return val
      else:
        return ""
    elif self.method == "POST" and self._isMultipart() == False:  # x-www-urlencoded
      if key in self.form.keys():
        val = self.form[key]
        if isWindows():
          val = val.replace("\\", "\\\\")
        if unEsc == True and plus == True:
          return urlp.unquote_plus(val)
        elif unEsc == True and plus == False:
          return urlp.unquote(val)
        else:
          return val
      else:
        return ""
    else:  # multipart/form-data
      if "-" in key:  # type="file"
        parts = key.split("-", 1)
        element = parts[0]
        name = parts[1]
        for fi in self.files:  # ファイルの場合 (複数ファイル不可)
          if fi[0] == name:
            if element == "filename":
              return fi[1]
            elif element == "chunk":
              return fi[2]
            else:
              return ""
      else:  # 普通のデータの場合
        if key in self.form.keys():
           return self.form[key]
        else:
           return ""
      return ""

  # クッキーを得る。
  def getCookie(self, key:str) -> str:
    val = ""
    if key in self.cookies:
      val = self.cookies[key]
    return val

  # パラメータがあるかどうか？
  def isPostback(self):
    if self.method == "GET":
      return len(self.queryString) > 0
    elif self.method == "POST":
      return len(self.form) > 0
    else:
      return False
    
  # HTTP Method (str)
  @property
  def method(self):
    return self.__Method

  # Request Headers (dict of (key:str, value:str))
  @property
  def headers(self) -> dict:
    return self.__Headers

  # Request Cookies(dict of (key:str, value:str))
  @property
  def cookies(self) -> dict:
    return self.__Cookies
    
  # QueryString (bytes)
  @property
  def queryString(self) -> bytes:
    return self.__QueryString
    
  # Posted Body (bytes)
  @property
  def body(self) -> bytes:
    return self.__Body
    
  # GET form (dict of (key:str, value:str))
  @property
  def query(self) -> dict:
    return self.__Query
    
  # POST form (dict of (key, value))
  @property
  def form(self) -> dict:
    return self.__Form

  # POST multipart form files (list of (name:str, filename:str, chunk:bytes))
  @property
  def files(self) -> list[tuple]:
    return self.__Files
    
  # Content-Type (when POST) (str)
  @property
  def content_type(self) -> str:
    ct = ""
    if self.method == "POST":
      if "content_type" in self.headers:
        ct = self.headers["content_type"]
    return ct

  # Boundary of multipart data (bytes)
  @property
  def boundary(self) -> bytes:
    border = b""
    if "boundary=" in self.content_type:
      p = self.content_type.split("boundary=")
      p1 = p[1]
      border = b"--" + p1.encode(encoding="utf-8", errors="replace")
    return border





# --------------------------------------------------------------------
# Response class
# --------------------------------------------------------------------
class Response:
  def __init__(self):
    # Windows の場合はデフォルトの文字コードが Shift JIS なので、これがないと文字化けする。
    if os.name == 'nt':
      sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=ENC)
    self.Cookies = list()
    self.Headers = list()
    return

  # クッキーをセットする。cookies は辞書オブジェクト。
  def setCookie(self, cookies:dict):
    for key, value in cookies.items():
      self.Cookies.append(f"{key}={value}")
    return

  # Set-Cookie: を作成する。
  def makeCookie(self):
    if len(self.Cookies) == 0:
      return ""
    buff = ""
    for s in self.Cookies:
      buff += f"Set-Cookie: {s}\n"
    return buff

  # 文字列を応答として返す。s はその文字列。
  def sendString(self, s:str, content_type="text/html", charset="utf-8", cookie=True, headers=True, embed=None, crlf=""):
    if type(s) is not str:
      s = str(s)
    if isinstance(embed, dict):
      for k, v in embed.items():
         s = s.replace("{{ " + k + " }}", str(v))
    buff = ""
    if cookie:
      buff = self.makeCookie()
    if headers and len(self.Headers) > 0:
      for h in self.Headers:
        buff += h + "\n"
    if charset == "":
      buff += f"Content-Type: {content_type}\n\n{s}"
    else:
      buff += f"Content-Type: {content_type}; charset={charset}\n\n{s}"
    print(buff, end=crlf)
    return

  # 単純な文字列を返す。
  def sendSimple(self, s:str, charset="", crlf='', content_type="text/plain"):
    if charset == "":
      print(f"Content-Type: {content_type}\n\n{s}", end=crlf)
    else:
      print(f"Content-Type: {content_type}; charset={charset}\n\n{s}", end=crlf)
    return

  # pprint でオブジェクトを文字列にして返す。(for Debug)
  def sendPPrint(self, obj, charset=""):
    if charset == "":
      print("Content-Type: text/plain\n")
    else:
      print(f"Content-Type: text/plain; charset={charset}\n")
    pprint(obj)
    return

  # バイナリーデータを返す。
  def sendBinData(self, data:bytes):
    sys.stdout.buffer.write(b"Content-Type: application/octet-stream\n\n" + data)
    return

  # データを JSON に変換し応答として返す。
  def sendJSON(self, data:dict(), charset=""):
    buff = ""
    if charset == "":
      buff += "Content-Type: application/json\n\n"
    else:
      buff += f"Content-Type: application/json; charset={charset}\n\n"
    buff += json.dumps(data)
    print(buff)
    return

  # テキストファイルを応答として返す。path はそのパス名。
  def sendText(self, path:str, charset=""):
    if charset == "":
      buff = f"Content-Type: text/plain\n\n"
    else:
      buff = f"Content-Type: text/plain; charset={charset}\n\n"
    with open(path, mode="rt", encoding="utf-8") as f:
      buff += f.read()
      print(buff)
    return

  # HTMLファイルを応答として返す。path はそのパス名。
  def sendHtml(self, path:str, charset="", cookie=True, headers=True, embed=None):
    buff = ""
    if headers and len(self.Headers) > 0:
      for h in self.Headers:
        buff += h + "\n"
    if charset == "":
      buff += f"Content-Type: text/html\n"
    else:
      buff += f"Content-Type: text/html; charset={charset}\n"
    if cookie:
      buff += self.makeCookie()
    buff += "\n"
    with open(path, mode="rt", encoding="utf-8") as f:
      buff += f.read()
      if isinstance(embed, dict):
        for k, v in embed.items():
          buff = buff.replace("{{" + k + "}}", str(v)).replace("{{ " + k + " }}", str(v))
      print(buff)
    return

  # 画像ファイルを応答として返す。path はそのパス名。
  def sendImage(self, path:str):
    p = pathlib.Path(path)
    if p.suffix == '.jpg':
      img = b'jpeg'
    elif p.suffix == '.png':
      img = b'png'
    elif p.suffix == '.svg':
      img = b'svg+xml'
    else:
      img = b'gif'
    if p.suffix == '.svg':
      with open(path, mode="rt") as f:
        svg = f.read()
        buff = b"Content-Type: image/" + img + b"\n\n" + svg.encode()
        if _isDebug():
          pprint(buff)
        else:
          print(buff)
    else:
      with open(path, mode="rb") as f:
        b = f.read()
        buff = b"Content-Type: image/" + img + b"\n\n" + b
        if _isDebug():
          pprint(buff)
        else:
          sys.stdout.buffer.write(buff)
    return

  # 動画ファイルを応答として返す。path はそのパス名。
  def sendVideo(self, path):
    p = pathlib.Path(path)
    if p.suffix == '.mp4':
      video = b"mp4"
    elif p.suffix == '.webm':
      video = b"webm"
    else:
      video = b"ogv"
    with open(path, mode="rb") as f:
      b = f.read()
      buff = b"Content-Type: video/" + video + b"\n\n" + b
      if _isDebug():
        pprint(buff)
      else:
        sys.stdout.buffer.write(buff)
    return

  # 音声ファイルを応答として返す。path はそのパス名。
  def sendAudio(self, path):
    p = pathlib.Path(path)
    if p.suffix == '.mp3':
      audio = b"mp3"
    elif p.suffix == '.m4a':
      audio = b"aac"
    elif p.suffix == '.wav':
      audio = b"wav"
    else:
      audio = b"ogg"
    with open(path, mode="rb") as f:
      b = f.read()
      buff = b"Content-Type: audio/" + audio + b"\n\n" + b
      if _isDebug():
        pprint(buff)
      else:
        sys.stdout.buffer.write(buff)
    return

  # その他の形式のファイルを応答として返す。mime は ZIP="application/zip", PDF="application/pdf" など
  def sendFile(self, path, mime="application/octed-stream", filename=""):
    buff = b""
    with open(path, mode="rb") as f:
      b = f.read()
      if filename != "":
        buff += b"Content-Disposition: attachment; filename=" + filename.encode() + b"\n"
      buff += b"Content-Type: " + mime.encode() + b"\n\n" + b
      if _isDebug():
        pprint(buff)
      else:
        sys.stdout.buffer.write(buff)
    return

  # リダイレクト
  @staticmethod
  def redirect(url):
    print("Location: " + url + "\n")

  # HTTP ヘッダを出力 (headersはリスト)
  @staticmethod
  def header(headers):
    s = ""
    for h in headers:
      s += h + "\n"
    s += "\n"
    print(s)
    return

  # HTTP レスポンス・ステータスコードを返す。code は "500 Internal Server Error" のようにする。
  @staticmethod
  def status(code, message=""):
    if message == "":
      print("Status: " + str(code) + "\n" + "Content-Type: text/html; charset=utf-8\n\n" + code)
    else:
      print("Status: " + str(code) + "\n" + "Content-Type: text/html; charset=utf-8\n\n" + message)
    return

# ---------------------------------------------------------------------------
#  ユーティリティ
# ---------------------------------------------------------------------------
class Utility:
  # HTML テーブルを作成する。
  @staticmethod
  def htmlTable(data, header=None, table="", tr="", th="", td=""):
    html = ""
    if table == "":
      html += "<table>\n"
    else:
      html += f"<table class=\"{table}\">\n"
    if isinstance(header, list):
      html += "<tr>\n"
      for col in header:
        if th == "":
          html += f"<th>{col}</th>"
        else:
          html += f"<th class=\"{th}\">{col}</th>"
      html += "</tr>\n"
    for row in data:
      if tr == "":
        html += "<tr>"
      else:
        html += f"<tr class=\"{tr}\">\n"
      for col in row:
        if td == "":
          html += f"<td>{col}</td>"
        else:
          html += f"<td class=\"{td}\">{col}</td>"
      html += "</tr>\n"
    html += "</table>\n"
    return html

  # HTML リストを作成する。
  @staticmethod
  def htmlList(data, list="ul", ul="", li=""):
    html = ""
    if ul == "":
      html += f"<{list}>"
    else:
      html += f"<{list} class=\"{ul}\">"
    for item in data:
      if li == "":
        html += "<li>"
      else:
        html += f"<li class={li}>"
      html += f"{item}</li>\n"
    html += f"</{list}>\n"
    return html

  # SVG を作成する。(円 'circle' と正方形 'square' のみ)
  @staticmethod
  def svg(shape, size=32, borderWidth=1, borderColor="black", bgColor="white"):
    svg = "<svg width=\"{0}\" height=\"{0}\">\n".format(size)
    if shape == "circle":
      x = size / 2
      y = size / 2
      r = size / 2
      svg += f"<circle cx=\"{x}\" cy=\"{y}\" r=\"{r}\" stroke-width=\"{borderWidth}\" stroke=\"{borderColor}\" fill=\"{bgColor}\" />\n"
    elif shape == "square":
      svg += f"<rect x=\"0\" y=\"0\" width=\"{size}\" height=\"{size}\" stroke-width=\"{borderWidth}\" stroke=\"{borderColor}\" fill=\"{bgColor}\" />\n"
    else:
      svg += "<text x=\"0\" y=\"0\" stroke=\"red\" font-size=\"30\">Error: Bad shape</svg>"
    svg += "</svg>\n"
    return svg

  # プロセスを起動する。
  @staticmethod
  def startProcess(cmd, *args):
    for a in args:
      cmd += " " + a
    proc = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    result = proc.stdout
    return result

  # JSON ファイル (構成ファイル) を読む。
  @staticmethod
  def readConf(filePath):
    conf = dict()
    with open(filePath, "r") as f:
      conf = json.load(f)
    return conf
