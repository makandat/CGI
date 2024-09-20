# for_cgi.py
import enum, os, sys, json
import urllib.parse as urlp

VERSION = "1.1.0"

# デバッグ用記録ファイル
DEBUGFILE = 'C:/temp/cgi_debug.txt'

# メッセージ (str) 記録 改行付き
def info(message:str):
  if DEBUGFILE == "":
    return
  if type(message) is not str:
    message = str(message)
  with open(DEBUGFILE, 'a', encoding='utf-8') as f:
    f.write(message + "\n")  
  return

# HTML ヘッダ部分
HTML_HEAD = '''
<!DOCTYPE html>
<html>
<head>
 <!-- <meta charset="utf-8" /> -->
 <title>{0}</title>
 <link rel="stylesheet" href="/css/style.css" />
</head>
<body>
'''

# HTML テイル部分
HTML_TAIL = '''
 <p>&nbsp;</p>
 <p>&nbsp;</p>
</body>
</html>
'''


# MIME タイプ
class Mime(enum.Enum):
  HTML = 1
  TEXT = 2
  JPEG = 3
  PNG  = 4
  GIF  = 5
  JSON = 6
  
# ステータス
class Status(enum.Enum):
  OK = 200
  NOT_MODIFIED = 304
  BAD_REQUEST = 400
  NOT_FOUND = 404
  METHOD_NOT_ALLOWED = 405
  INTERNAL_SERVER_ERROR = 500
  SERVICE_UNAVAILABLE = 503

# content-type 出力
def content_type(ctype=Mime.HTML, cookie=""):
  mime = ""
  match ctype:
    case Mime.HTML:
      mime = 'text/html; encoding=utf-8\n'
    case Mime.TEXT:
      mime = 'text/plain'
    case Mime.JPEG:
      mime = 'image/jpeg'
    case Mime.PNG:
      mime = 'image/png'
    case Mime.GIF:
      mime = 'image/gif'
    case Mime.JSON:
      mime = 'application/json'
    case _:
      raise "Not implement."
  output = "Content-Type: " + mime + cookie + "\n"
  print(output)
  return
  
# HTML 出力
def send_html(html:str, cookies:dict=None):
  if cookies == None:
    content_type(ctype=Mime.HTML)
  else:
    str_cookie = makeCookie(cookies)
    content_type(ctype=Mime.HTML, cookie=str_cookie)
  print(html)
  return
  
# 画像ファイル出力
def send_image(path:str):
  ext = os.path.splitext(path)[1]
  mime = Mime.PNG
  match ext.lower():
    case '.png':
      mime = b'image/png\n\n'
    case '.jpg':
      mime = b'image/jpeg\n\n'
    case '.gif':
      mime = b'image/gif\n\n'
    case _:
      pass
  with open(path, "rb") as f:
    buff = f.read()
    sys.stdout.buffer.write(b'Content-Type: ' + mime)
    sys.stdout.buffer.write(buff)
    return
    
# JSON 出力
def send_json(data):
  if data is str:
    s = data
  else:
    s = json.dumps(data, ensure_ascii=False)
  jsdata = s.encode()
  sys.stdout.buffer.write(b'Content-Type: application/json\n\n' + jsdata)
  return
  
# QUERY_STRING のセット (デバッグ用)
def set_querystring(params:str|dict[str, str]):
  envdata = params
  if type(params) is dict:
    envdata = urlp.urlencode(params)
  os.environ['QUERY_STRING'] = envdata
  return
  
# QUERY_STRING があるか？
def qs_exists():
  a = 'QUERY_STRING' in os.environ.keys()
  b = 0
  if a:
    b = len(os.environ['QUERY_STRING']) > 0
  return (a and b)

# QUERY_STRING を分解してパラメータの辞書を返す。
def get_params():
  qstring = os.environ['QUERY_STRING']
  params = urlp.parse_qs(qstring)
  m = dict()
  for k in params.keys():
    v = params[k]
    m[k] = v[0]
  return m

# HTTP リクエストメソッドの取得
def get_method():
  return os.getenv("REQUEST_METHOD", "")

# HTTP レスポンスステータスを返す。
def send_status(code:int, message=""):
  if message == "":
    print("Status: " + str(code.value) + "\n" + "Content-Type: text/html; charset=utf-8\n\n" + str(code.value))
  else:
    print("Status: " + str(code.value) + "\n" + "Content-Type: text/html; charset=utf-8\n\n" + message)
  return  
  
# POST されたフォームデータからパラメータ辞書を得る。(multipart/form-data でない場合)
def get_body():
  body = sys.stdin.buffer.read()
  body_uq = urlp.unquote(body)
  params = urlp.parse_qs(body_uq)
  data = dict()
  for key in params:
    data[key] = params[key][0]
  return data

# リクエストクッキーを取得する。(v1.1.0 で追加)
def get_cookies():
  http_cookie = os.getenv("HTTP_COOKIE", "")
  cookielist = http_cookie.split('; ')
  cookies = dict()
  for item in cookielist:
    kv = item.split('=', 1)
    if len(kv) == 2:
      k = kv[0]
      v = urlp.unquote(kv[1])
      cookies[k] = v
  return cookies
  
# Set-Cookie: を作成する。
def makeCookie(cookies):
  buff = ""
  for k in cookies.keys():
    v = urlp.quote(str(cookies[k]))
    buff += f"Set-Cookie: {k}={v}\n"
  return buff
  
