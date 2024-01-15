# CGI356Lib.py v1.7.13  2024-01-12
import os, sys, datetime, io
import subprocess
from subprocess import PIPE
import urllib.parse as urlp
import pathlib
import json
from pprint import pprint

# 文字コード
ENC = 'utf-8'
# デバッグ用ログファイル
if os.name == 'nt':
  LOG = "D:/temp/CGI365Lib.log"
else:
  LOG = "/var/www/data/CGI365Lib.log"

# デバッグ用 判別
def _isDebug():
  ret = False
  if len(sys.argv) > 1 :
    if sys.argv[1] == "debug" or sys.argv[1] == "debug_get":
      os.environ["REQUEST_METHOD"] = "GET"
      ret = True
    elif sys.argv[1] == "debug_post":
      os.environ["REQUEST_METHOD"] = "POST"
      ret = True
    else:
      pass
  return ret

# デバッグ用 QUERY_STRING 設定
def setQueryString(qs):
  if _isDebug():
    os.environ["QUERY_STRING"] = qs

# デバッグ用 HTTP_COOKIE 設定
def setHttpCookie(cookie):
  if _isDebug():
    os.environ["HTTP_COOKIE"] = cookie

# デバッグ用 REQUEST_METHOD 設定
def setRequestMethod(method):
  if _isDebug():
    os.environ["REQUEST_METHOD"] = method

# デバッグ用ログ出力
def info(obj):
  if LOG == "":
    return
  now = datetime.datetime.now()
  strnow = now.isoformat()
  with open(LOG, mode="at") as f:
    f.write(strnow + " " + str(obj) + "\n")

# ステータスコード
OK = "200 OK"
BAD_REQUEST = "400 Bad Request"
FORBIDDEN = "403 Forbidden"
NOT_FOUND = "404 Not Found"
METHOD_NOT_ALLOWED = "405 Method Not Allowed"
INTERNAL_SERVER_ERROR = "500 Internal Server Error"
NOT_IMPLEMENTED = "501 Not Implemented"

# タグで囲む。
def tag(t, s, c=""):
  tg = f"<{t}"
  if c == "":
    tg += ">"
  else:
    tg += f" class=\"{c}\">"
  tg += f"{s}</{t}>\n"
  return tg

# a タグで囲む
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
    # Windows の場合はデフォルトの文字コードが Shift JIS なので、これがないと文字化けする。
    if os.name == 'nt':
      sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding=ENC)
    self.Body = b""                #  POST で受け取った生データ (バイト列または文字列)
    self.QueryString = ""             #  GET で受け取った環境変数 QUERY_STRING (文字列)
    self.Method = self._getMethod()   #  HTTP メソッド 'GET', 'POST'...
    self.Address = self._getAddress() #  アドレス 辞書 キーは 'Server', 'Client', 'Host'
    self.Query = self._getQuery()     #  GET のパラメータ 辞書
    self.Form = dict()                #  POST のパラメータ 辞書
    self.Files = list()               #  アップロードされた tuple (コントロール名、ファイル名, chunk) のリスト
    self.Cookies = self._getCookies()   #  クッキー 辞書
    self.Headers = self._getHeaders() #  リクエストヘッダ辞書
    if _isDebug() and b"cookie" in self.Headers:
      vals = self.Headers[b"cookie"]
      p = vals.split(b"; ")
      if len(p) > 0:
        for kv in p:
          q = kv.split(b"=", 1)
          self.Cookies[q[0]] = q[1]
    (debug, filePath) = self._getDebug()
    if self.Method == "POST" and debug == False:
      self.Body = sys.stdin.buffer.read()
    if self.Method == "POST" and parse:
      self.parseFormBody()
    if "PATH_INFO" in os.environ:
      self.PathInfo = os.environ["PATH_INFO"]   # リクエストパス
    else:
      self.PathInfo = ""
    return

  # CGI パラメータを得る。キーが存在しないときは空文字を返す。
  def getParam(self, key, unEsc=True):
    if self.Method == "GET":
      if key in self.Query:
        if unEsc:
          return urlp.unquote_plus(self.Query[key]).replace("\\", "\\\\")
        else:
          return self.Query[key]
      else:
        return ""
    elif self.Method == "POST" and type(self.Form) == dict:  # x-www-urlencoded
      if key in self.Form:
        if unEsc:
          return urlp.unquote_plus(self.Form[key]).replace("\\", "\\\\")
        else:
          return self.Form[key]
      else:
        return ""
    else:  # multipart/form-data
      for block in self.Form:
        if key in block:
          return block[key]
        else:
          continue
      return ""

  # クッキーを得る。
  def getCookie(self, key):
    val = ""
    if key in self.Cookies:
      val = self.Cookies[key]
    return val

  # x-www-urlencoded された Request body を dict にする。
  def _parseBody(self, body):
    h = dict()
    if type(body) is bytes:
      body = body.decode()
    # '&' で body を分割する。
    exprs = body.split("&")
    for e in exprs:
      # 最初の '=' で exprs を分割
      kv = e.split("=", 1)
      if len(kv) == 2:
        key = kv[0]
        val = kv[1]
        h[key] = urlp.unquote(val)
      else:
        h[e] = ""
    return h

  # 複数ファイルアップロードのとき、ファイル内容を取得する。
  def getFileBody(self, name, filename):
    for a in self.Files:
      if a[0] == name and a[1] == filename:
        return a[2]
    return None

  # POST データを解析する。
  def parseFormBody(self):
    TYPE_FILE = 0
    TYPE_TEXT = 1
    OTHER = 2
    
    # コンソールアプリとしてデバッグするか？
    buff = b""
    (debug, filePath) = self._getDebug()
    if debug:
      # デバッグモード
      if filePath == '':
        print("Enter posted data (1-line) > ", end='')
        s = input()
        s = urlp.unquote(s)
        buff = s.encode("utf-8", errors="replace")
      else:
        with open(filePath, "rb") as f:
          buff = f.read()
    else:
      buff = self.Body
    name = ""
    value = ""
    paramlist = list()
    boundary = self._getBoundary()
    if boundary != b"" and buff.startswith(boundary):
      # multipart/form-data を境界でブロックに分ける。
      blocks = self._parseMultiPart(buff, boundary)
      params = dict()
      state = TYPE_FILE
      # multipart/form-data のブロックごとに処理する。
      for block in blocks:
        # lines (行) と chunk (バイナリーデータ) に分ける。
        (lines, chunk) = block
        # 行ごとの処理
        for line in lines:
          # 空行は読み飛ばす。
          if line == b'':
            pass
          elif state == TYPE_FILE and line.find(b"Content-Disposition: form-data;") == 0:
            # Content-Disposition 行の処理
            line = line[len(b"Content-Disposition: form-data;"):]
            p = line.find(b"name=\"")
            if p < 0:
              pass
            else:
              # name="..." から name 属性を取得する。
              line = line[p + 6:]
              p = line.find(b"\"")
              name = line[:p].decode()
              params["element-name"] = name
              line = line[p+2:]
              # ファイルアップロードの時は filename="..." があるのでファイル名を取得する。
              p = line.find(b"filename=\"")
              if p < 0:
                state = 1  # input[type="file"] でない場合
              else:
                # input[type="file"] の場合
                line = line[p+10:]
                p = line.find(b"\"")
                filename = line[:p].decode()
                params[f"filename-{name}"] = filename
                self.Files.append((name, filename, chunk))
                state = OTHER
          elif line == boundary + b"--":  # 最後の境界
            info("最後の境界")
            break
          elif state == TYPE_TEXT:
            # input[type="file"] でない場合 name に対する値を取得する。
            value = line.decode()
            params[name] = value
            state = OTHER  # 次の Content-Disposition へ
          elif state == OTHER:
            if line.find(b'Content-Type: ') == 0:
              # input[type="file"] の場合、Content-Type の内容を取得する。
              line = line[len(b'Content-Type: '):]
              params["type"] = line.decode()
              params[f"chunk-{name}"] = chunk  # アップロードされたファイル内容
              state = TYPE_FILE
            elif line.find(b'Content-Disposition: form-data;') == 0:
              # テキストデータ
              state = TYPE_TEXT
              line = line[len(b"Content-Disposition: form-data;"):]
              p = line.find(b"name=\"")
              if p < 0:
                pass
              else:
                # name="..." から name 属性を取得する。
                line = line[p + 6:]
                p = line.find(b"\"")
                name = line[:p].decode()
                params["element-name"] = name
            else:
              break
          else:
            state = TYPE_FILE
          # End of block loop
        paramlist.append(params)
        params = dict()
      # パラメータ一覧を self.Form に代入 (ブロックが終わったので結果を保存)
      self.Form = paramlist
    else:
      # 普通のフォーム（マルチでない）
      self.Form = self._parseBody(buff)
    #info(self.Form) # <== DELETED
    return

  # マルチパートのブロックを行に分割する。
  def _makeLines(self, block:bytes) -> tuple:
    lines = list()
    chunk = b''
    while True:
      p = block.find(b"\r\n") # 行末 CR+LF を見つける。
      if p < 0:
        break  # 行末がないときはループを抜ける。
      line = block[0:p]
      lines.append(line)
      if b"Content-Type:" in line:
        chunk = block[p+4:-2] # chunk の前には２つの CR+LF があるので +4、chunk の後には CR+LF があるので -2
        break # chunk のあるブロックは最後なのでループを抜ける。
      block = block[p+2:]  # 次のブロックへ +2 は CR+LF の分。
    return (lines, chunk)

  # マルチパートフォームデータを解析する。
  def _parseMultiPart(self, buff: bytes, boundary: bytes) -> list:
    # ブロックのリスト
    blocks = list()
    # 最初のブロックを得る。
    lenb = len(boundary)
    p = lenb + 2 # 2 は行末の CR+LF の分
    buff = buff[p:]
    # 境界線で生データ全体を分割する。
    while True:
      # 次の境界線を探す。
      p = buff.find(boundary)
      if p < 0:
        break
      (lines, chunk) = self._makeLines(buff[:p])  # lines はブロックの chunk 以外の行。
      blocks.append((lines, chunk))
      p += lenb + 2  # 2 は行末の CR+LF の分
      buff = buff[p:]
    return blocks

  # クライアントから受け取った生データ文字列をJSON とみなし辞書を作成する。
  def parseJSON(self):
    # コンソールアプリとしてデバッグするか？
    (debug, filePath) = self._getDebug()
    if debug == True:
      if filePath == '':
        print("Enter JSON Data > ", end='')
        s = input()
        s = urlp.unquote(s)
      else:
        with open(filePath, "r") as f:
          s = f.read()
    else:
      pass
    result = json.loads(self.Body)
    return result

  # クライアントから受け取った生データを BLOB とみなし、self.Body に格納する。
  def getRawData(self):
    # コンソールアプリとしてデバッグするか？
    (debug, filePath) = self._getDebug()
    if debug == True:
      if filePath == '':
        print("Enter Raw Data > ", end='')
        s = input()
        s = urlp.unquote(s)
        self.Body = s.encode("utf-8", errors="replace")
      else:
        with open(filePath, "rb") as f:
          self.Body = f.read()
    else:
      pass
    return self.Body

  # クライアントから受け取った生データを BLOB とみなし、self.Body に格納する。
  # さらに path が "" でないならファイルのパスとみなしファイル保存する。
  def saveAsBLOB(self, path):
    self.Body = sys.stdin.buffer.read()
    with open(path, "wb") as f:
      f.write(self.Body)
    return

  # Request.Body を保存する。(self.Body が取得済みであること)
  def saveRawData(self, savePath):
    with open(savePath, "wb") as f:
      f.write(self.Body)
    return

  # クライアントから受け取った生データを UTF-8 文字列とみなし、self.Body に格納する。
  def getRawString(self):
    self.Body = sys.stdin.read()
    return self.Body

  # クライアントから受け取った生データを UTF-8 文字列とみなし、self.Body に格納する。
  # さらに path が "" でないならファイルのパスとみなしファイル保存する。
  def saveAsRawString(self, path):
    self.Body = sys.stdin.read()
    with open(path, "w") as f:
      f.write(self.Body)
    return

  # アップロードされたファイルをファイル保存する。(request.parseFormBody()を事前に実行しておくこと)
  def saveFile(self, name, savedir, binary=False):
    chunk = self.getParam("chunk-" + name)
    filename = self.getParam("filename-" + name)
    if filename == "":
      return False
    path = savedir + "/" +filename
    mode = "wt"
    if binary:
      mode = "wb"
    else:
      chunk = chunk.decode()
    with open(path, mode) as f:
      f.write(chunk)
    return True

  # フォームデータを文字列にする。(デバッグ用)
  def formdataToString(self):
    s = ""
    for block in self.Form:
      for k, v in block.items():
        s += f"{k}:{v}, "
    return s

  # 環境変数 QUERY_STRING から変数名をキーとする辞書を作成する。
  def _getQuery(self) -> dict:
    result = dict()
    if _isDebug():
      self.Method = os.environ["REQUEST_METHOD"]
      if self.Method != "GET":
        return
      (debug, filePath) = self._getDebug()
      if filePath == "":
        print("Enter QUERY_STRING >")
        s = input()
        self.QueryString = urlp.unquote(s)
      elif filePath != "":
        with open(filePath, "rt") as f:
          self.QueryString = f.read()
      else:
        self.QueryString = os.environ["QUERY_STRING"] if "QUERY_STRING" in os.environ else ""
      self.Body = self.QueryString.encode()
      params = urlp.parse_qs(self.QueryString)
      try:
        for key in params:
          result[key] = params[key][0]
      except Exception as e:
        result["error"] = str(e)
    else:
      try:
        self.QueryString = os.environ["QUERY_STRING"] if "QUERY_STRING" in os.environ else ""
        params = urlp.parse_qs(self.QueryString)
        for key in params:
          result[key] = params[key][0]
      except Exception as e:
        result["error"] = str(e)
    return result

  # 環境変数 REQUEST_METHOD から HTTP メソッド名を返す。
  def _getMethod(self) -> str:
    method = ""
    if "REQUEST_METHOD" in os.environ:
      method = os.environ["REQUEST_METHOD"]
    return method

  # 環境変数 HTTP_COOKIE からクッキー名をキーとする辞書を返す。
  def _getCookies(self) -> dict:
    cookies = dict()
    try:
      if _isDebug() == False:
        http_cookie = os.environ["HTTP_COOKIE"]
        if http_cookie == "":
          http_cookie = req.Headers["cookie"]
        cookielist = http_cookie.split('; ')
        for item in cookielist:
          kv = item.split('=', 1)
          k = kv[0]
          v = urlp.unquote(kv[1])
          cookies[k] = v
    except:
      pass
    return cookies

  # リクエストヘッダ一覧を取得する。
  def _getHeaders(self) -> dict:
    headers = dict()
    if _isDebug():
      print("Enter REQUEST HEADERS (1-line, JSON)>")
      s = input()
      if len(s) > 2:
        s = urlp.unquote(s)
        headers1 = json.loads(s)
        for k, v in headers1.items():
          headers[k.encode()] = v.encode()
    else:
      keys = os.environ.keys()
      for key in keys:
        v = os.getenv(key)
        if key.startswith("HTTP_"):
          k = key[5:].lower()
          headers[k] = v
        if key.startswith("CONTENT_TYPE"):
          headers["content_type"] = v
    return headers


  # 環境変数から self.Address の内容を作成する。
  def _getAddress(self) -> dict:
    address = dict()
    try:
      address['Server'] = os.environ["SERVER_ADDR"] + ":" + os.environ["SERVER_PORT"]
      address['Client'] = os.environ["REMOTE_ADDR"] + ":" + os.environ["REMOTE_PORT"]
      address['Host'] = os.environ["HTTP_HOST"]
    except:
      pass
    return address

  # マルチパートデータの境界線を得る。
  def _getBoundary(self) -> bytes:
    boundary = b""
    if "CONTENT_TYPE" in os.environ:
      content_type = os.environ["CONTENT_TYPE"]
      if "boundary=" in content_type:
        p = content_type.split("boundary=")
        boundary = b"--" + p[1].encode(encoding="utf-8", errors="replace")
    return boundary

  # filename と chunk を得る。
  def _getChunk(self, name, filename=None):
    fstr = b"form-data; name=\"" + name.encode() + b"\""
    data = self.Body
    p = data.find(fstr)
    if p >= 0:
        data1 = data[p:]
        p = data1.find(b"filename=\"")
        data1 = data1[p+10:]
        q = data1.find(b"\"")
        filename = data1[0:q].decode()
        data1 = data1[q+1:]
        p = data1.find(b"Content-Type:")
        data1 = data1[p+13:]
        p = data1.find(b"\r\n\r\n")
        data1 = data1[p+4:]
        q = data1.find(b"-----")
        chunk = data1[0:q-2]
        return (filename, chunk)
    else:
        return (b"", b"")

  # デバッグ用のファイルを得る。
  def _getDebug(self):
    dbg = False
    filePath = ""
    if len(sys.argv) > 1:
      if sys.argv[1] == "debug":
        self.Method = "GET"
        dbg = True
      else:
        if sys.argv[1] == "debug_get":
          self.Method = "GET"
          dbg =True
          if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
            filePath =sys.argv[2]
          else:
            pass
        elif sys.argv[1] == "debug_post":
          self.Method = "POST"
          dbg = True
          if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
            filePath = sys.argv[2]
          else:
            pass
        else:
          pass
    return (dbg, filePath)

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
  def sendBinData(self, data):
    sys.stdout.buffer.write(b"Content-Type: application/octet-stream\n\n" + data)
    return

  # データを JSON に変換し応答として返す。
  def sendJSON(self, data, charset=""):
    buff = ""
    if charset == "":
      buff += "Content-Type: application/json\n\n"
    else:
      buff += f"Content-Type: application/json; charset={charset}\n\n"
    buff += json.dumps(data)
    print(buff)
    return

  # テキストファイルを応答として返す。path はそのパス名。
  def sendText(self, path, charset=""):
    if charset == "":
      buff = f"Content-Type: text/plain\n\n"
    else:
      buff = f"Content-Type: text/plain; charset={charset}\n\n"
    with open(path, mode="rt", encoding="utf-8") as f:
      buff += f.read()
      print(buff)
    return

  # HTMLファイルを応答として返す。path はそのパス名。
  def sendHtml(self, path, charset="", cookie=True, headers=True, embed=None):
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
  def sendImage(self, path):
    p = pathlib.Path(path)
    if p.suffix == '.jpg':
      img = b'jpeg'
    elif p.suffix == '.png':
      img = b'png'
    elif p.suffix == '.svg':
      img = 'svg+xml'
    else:
      img = b'gif'
    if p.suffix == '.svg':
      with open(path, mode="rt") as f:
        svg = f.read()
        buff = "Content-Type: image/" + img + "\n\n" + svg
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
  def sendFile(self, path, mime, filename=""):
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
