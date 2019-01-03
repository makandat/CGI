# coding:utf-8
# Version 1.00  2018-12-12 bug fix
#   参考 http://cgi.tutorial.codepoint.net/intro
import os, sys, io
import cgi
import locale
import http.cookies as Cookie
import urllib.parse

#
#  WebPage クラス
# ================
class WebPage :
  APPCONF = "AppConf.ini"
        
    # コンストラクタ
  def __init__(self, template="") :
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
    self.readConf()
    # HTTP パラメータを得る。
    form = cgi.FieldStorage()
    for k in form.keys() :
      self.params[k] = form[k]
    # クッキーを得る。
    if "HTTP_COOKIE" in os.environ :
      cc = Cookie.SimpleCookie()
      cc.load(os.environ["HTTP_COOKIE"])
      for k, v in cc.items() :
        self.cookies[k] = v

  # コンテンツを送信する。
  def echo(self) :
    # クッキーをヘッダーに追加
    for k, v in self.cookies.items() :
      self.headers.append("Set-Cookie: " + k + "=" + str(v))
    # ヘッダーを送信
    self.header()
    # 埋め込み変数を処理
    for k, v in self.vars.items() :
      self.html = self.html.replace("(*" + k + "*)", str(v))
    # HTML を送信
    print(self.html)
    return
             
  # HTTP ヘッダーを送信する。
  def header(self) :
    for s in self.headers :
      print(s)
    print()

  # クッキーを登録する。
  def cookie(self, key, value) :
      self.cookies[key] =value
  
  # AppConf.ini を読む。
  def readConf(self) :
    self.conf = {}
    if not os.path.exists(WebPage.APPCONF) :
      return
    with open(WebPage.APPCONF) as f :
      for line in f :
        if line[0] =='#' or line[0] == '[' or len(line) == 0:
          continue
        kv = line.split('=')
        if len(kv) == 2 :
          key = kv[0].strip()
          value = kv[1].strip()
          self.conf[key] = value
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
  def tag(name, str) :
    return "<" + name + ">" + str + "</" + name + ">"

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

  # HTML エスケープ文字を変換
  @staticmethod
  def escape(str) :
    return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

  # 画像を送信する。
  @staticmethod
  def sendImage(file) :
    ext = os.path.splitext(file)[1].lower()
    if ext == '.jpg' :
      type = b"jpeg"
    elif ext == '.png' :
      type = b'png'
    else :
      type = b'gif'
    with open(file, "rb") as f :
      b = f.read()
    buff = b"Content-Type: image/" + type + b"\n\n" + b
    #buff = b"Content-Type: image/png\n\n" + b
    sys.stdout.buffer.write(buff)

  # JSON テキストを応答
  @staticmethod
  def sendJson(json) :
    print("Content-Type: application/json\n")
    print(json)

  # プレーンテキストを応答
  @staticmethod
  def sendText(str) :
    print("Content-Type: text/plain\n")
    print(str)
