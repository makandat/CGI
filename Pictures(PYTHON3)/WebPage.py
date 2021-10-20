# -*- coding:utf-8 -*-
# WebPage.py Version 2.07  2021-10-20
import os, sys, io, base64
import cgi
import json
import re
import Common
import http.cookies as Cookie
#import urllib.parse
#if os.name != 'nt' :
#  from syslog import syslog
from jinja2 import Environment, Template, FileSystemLoader

#
#  WebPage クラス
# ================
class WebPage :
  APPCONF = "AppConf.ini"

    # コンストラクタ
  def __init__(self, template="", conf=APPCONF) :
    #Common.init_logger()
    self.headers = ["Content-Type: text/html"] # HTTP ヘッダーのリスト
    self.vars =    {}  # HTML 埋め込み変数
    self.params =  {}  # HTTP パラメータ
    self.conf =    {}  # AppConf.ini の値
    self.cookies = {}  # Cookie の値
    # stdin, stdout のコードを UTF-8 にする。デフォルトは ASCII になっているので文字化けする。
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # HTML テンプレートを設定する。
    self.html = ""
    try :
      with open(template, encoding='utf-8') as f :
        self.html = f.read()
    except :
      pass
    # AppConf.ini を読む。
    if conf :
      self.readConf(conf)
    # HTTP パラメータを得る。
    self.form = cgi.FieldStorage()
    for k in self.form.keys() :
      self.params[k] = self.form[k]
    # クッキーを得る。※ 長いクッキーの処理ができないので注意。
    if "HTTP_COOKIE" in os.environ :
      cc = Cookie.SimpleCookie()
      cc.load(os.environ["HTTP_COOKIE"])
      for k, v in cc.items() :
        self.cookies[k] = v
    else :
      pass
    return

  # HTTP メソッドを返す。
  def getMethod(self) :
    return os.environ["REQUEST_METHOD"]

  # テンプレートを読み込む。
  def loadTemplate(self, template) :
    try :
      with open(template, encoding='utf-8') as f :
        self.html = f.read()
    except :
      pass
    return

  # コンテンツを送信する。
  def echo(self, jinja=False) :
    # クッキーをヘッダーに追加
    for k, v in self.cookies.items() :
      self.headers.append("Set-Cookie: " + k + "=" + str(v))
    # ヘッダーを送信
    self.header()
    # 埋め込み変数を処理
    if not jinja :
      for k, v in self.vars.items() :
        self.html = self.html.replace("(*" + k + "*)", str(v))
    # HTML を送信
    print(self.html)
    return

  # テンプレートを Jinja2 としてコンテンツを送信する。
  def render(self, filename, data) :
    env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'))
    template = env.get_template(filename)
    self.html = template.render(data)
    self.echo(jinja=True)

  # HTTP ヘッダーを送信する。
  def header(self) :
    for s in self.headers :
      print(s)
    print()

  # プレースホルダに値を設定する。
  def setPlaceHolder(self, key, value, esc=False) :
    if esc :
      value = WebPage.escHtml(value)
    self.vars[key] = value

  # プレースホルダの値を得る。
  def getPlaceHolder(self, key) :
    if key in self.vars.keys() :
      return self.vars[key]
    else :
      return ""

  # 連想配列で与えられたキーと値をプレースホルダに値を設定する。
  def embed(self, hashtable, esc=False) :
    for key, value in hashtable.items() :
      if esc :
        value = WebPage.escHtml(value)
      self.vars[key] = value
    return

  # パラメータ key があるかどうかを返す。
  def isParam(self, key) :
    return key in self.params.keys()

  # 外部から来る引数の値を得る。
  def getParam(self, key, default="") :
    if self.isParam(key) :
      #return self.params[key].value
      return self.form.getvalue(key)
    else :
      return default

  # クッキー key の有無を返す。
  def isCookie(self, key) :
    return key in self.cookies.keys()

  # クッキーを得る。
  def getCookie(self, key, default="") :
    if self.isCookie(key) :
      c = self.cookies[key]
      if type(c) == str :
        return c
      else :
        return c.value
    else :
      return default

  # クッキーを登録する。
  def setCookie(self, key, value) :
    self.cookie(key, value)

  # クッキーを登録する。(Alias)
  def cookie(self, key, value) :
    self.cookies[key] = value

  # AppConf.ini or AppConf.json を読む。
  def readConf(self, filename = APPCONF) :
    self.conf = {}
    if not os.path.exists(filename) :
      return
    root, ext = os.path.splitext(filename)
    if ext == '.ini' :
      with open(filename) as f :
        for line in f :
          if line[0] =='#' or line[0] == '[' or len(line) == 0:
            continue
          kv = line.split('=')
          if len(kv) == 2 :
            key = kv[0].strip()
            value = kv[1].strip()
            self.conf[key] = value
    elif ext == '.json' :
      with open(filename) as f :
        s = f.read()
        self.conf = json.loads(s)
    else :
      pass
    return

  # アップロードされたファイルを保存する。
  def saveFile(self, key, dir) :
    filename = os.path.basename(self.params[key].filename)
    with open(f"{dir}/{filename}", "wb") as f :
      f.write(self.params[key].file.read())

  # リダイレクト
  def redirect(self, url, wait=1) :
    html = '''<html>
<head>
<meta charset="utf-8" />
<title>redirect</title>
<meta http-equiv="refresh" content="{1};{0}" />
</head>
<body>
<div style="margin-left:25%;margin-top:50px;">
<a href="{0}">ジャンプしないときはここをクリックしてください。Click here</a>
</div>
</body>
</html>
'''
    if type(url) is str :
      self.html = html.format(url, wait)
    else :
      self.html = html.format(url.value, wait)
    self.cookies = {}

  # タグ作成
  @staticmethod
  def tag(name:str, s, attr="") -> str:
    if s == None :
      s = ""
    ss = str(s)
    if attr == "" :
      tag = f"<{name}>{ss}</{name}>"
    else :
      tag = f"<{name} {attr}>{ss}</{name}>"
    return tag

  # テーブル行を作成
  @staticmethod
  def table_row(iter) :
    buff = "<tr>";
    for s in iter :
      buff += "<td>"
      buff += str(s)
      buff += "</td>"
    buff += "<tr>\n"
    return buff

  # テーブル表題行を作成
  @staticmethod
  def table_header(fields) :
    buff = "<tr>";
    for s in fields :
      buff += "<th>"
      buff += str(s)
      buff += "</th>"
    buff += "<tr>\n"
    return buff

  # タグを取る。
  @staticmethod
  def stripTag(s) :
    p = re.compile(r"<[^>]*?>")
    return p.sub("", s)

  # HTML エスケープ文字を変換
  @staticmethod
  def escHtml(str) :
    return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

  # URL エスケープ文字を変換
  @staticmethod
  def escUrl(str) :
    return str.replace(' ', '%20').replace('&', '%26').replace('?', '%3F').replace('=', '%3D').replace('%', '%25').replace('#', '%23').replace('+', '%2B')

  # 画像を送信する。v2.0
  @staticmethod
  def sendImage(file) :
    ext = os.path.splitext(file)[1].lower().decode()
    if ext == '.jpg' :
      type = b"jpeg"
    elif ext == '.png' :
      type = b'png'
    elif ext == '.gif' :
      type = b'gif'
    elif ext == '.svg' :
      type = b'svg+xml'
    else:
      return
    with open(file.decode(), "rb") as f :
      b = f.read()
    buff = b"Content-Type: image/" + type + b"\n\n" + b
    sys.stdout.buffer.write(buff)
    return

  # 音声を送信する。v2.0
  @staticmethod
  def sendAudio(file) :
    ext = os.path.splitext(file)[1].lower()
    if ext == '.mp3' :
      type = b"mpeg"
    elif ext == '.m4a' :
      type = b'aac'
    elif ext == '.ogg' :
      type = b'ogg'
    elif ext == '.wav':
      type = b'wav'
    else :
      return
    with open(file, "rb") as f :
      b = f.read()
    buff = b"Content-Type: image/" + type + b"\n\n" + b
    #buff = b"Content-Type: image/png\n\n" + b
    sys.stdout.buffer.write(buff)
    return

  # 動画を送信する。v2.0
  @staticmethod
  def sendVideo(file) :
    ext = os.path.splitext(file)[1].lower()
    if ext == '.mp4' :
      type = b"mpeg"
    elif ext == '.webm' :
      type = b'webm'
    elif ext == '.ogv' :
      type = b'ogv'
    elif ext == '.3gpp' :
      type = b'3gpp'
    else :
      return
    with open(file, "rb") as f :
      b = f.read()
    buff = b"Content-Type: image/" + type + b"\n\n" + b
    sys.stdout.buffer.write(buff)
    return

  # JSON テキストを送信
  @staticmethod
  def sendJSON(data) :
    print("Content-Type: application/json\n")
    s = data
    if not Common.is_str(data) :
      s = json.dumps(data)
    print(s, end="")
    return

  # プレーンテキストを送信
  @staticmethod
  def sendText(str) :
    print("Content-Type: text/plain\n")
    print(str, end="")
    return

  # HTML を送信 v2.0
  @staticmethod
  def sendHTML(str) :
    print("Content-Type: text/html\n\n" + str, end="")
    return

  # HTML ファイルを送信 v2.0
  @staticmethod
  def sendHTMLFile(file) :
    with open(file, "r") as f :
      buff = f.read()
      print("Content-Type: text/html\n\n" + buff, end="")
    return

  # MIME を指定して送信 v2.0  (mtype例) "application/pdf"
  @staticmethod
  def sendBLOB(mtype, data) :
    buff = b"Content-Type: " + mtype.encode() + b"\n\n" + data
    sys.stdout.buffer.write(buff)
    return

# ファイルダウンロード
  @staticmethod
  def download(mtype, filename, data):
    buff = b"Content-Type: " + mtype.encode() + b'\nContent-Disposition: attachment; filename="' + filename.encode() + b'"' + b"\n\n" + data
    sys.stdout.buffer.write(buff)
    return

  # 内部エラーステータスを返す。
  @staticmethod
  def internalError() :
    sys.stdout.buffer.write(b"500 Internal Server Error")
    return

  # リソースが存在しないエラーを返す。
  @staticmethod
  def notFound() :
    sys.stdout.buffer.write(b"404 Not Found")
    return

#from cgi import FieldStorage

def parse_multipart_form(headers, body):
    fp = io.BytesIO(base64.b64decode(body))
    environ = {'REQUEST_METHOD': 'POST'}
    headers = {
        'content-type': headers['Content-Type'],
        'content-length': headers['Content-Length']
    }
    fs = cgi.FieldStorage(fp=fp, environ=environ, headers=headers)
    #for f in fs.list:
    #    print(f.name, f.filename, f.type, f.value)
    return fs
