# https://github.com/makandat/CGI
#   CGI libraries

# CGI365Lib
* Python3 CGI Library
* For middle size CGI program.
* Support multipart/form-data.

## Sample 1 echo.cgi
```
#!C:/Python3/python.exe
import CGI365Lib as CGI

HTML = "./templates/echo.html"

# GET method
def on_GET(req, res):
  message = req.getParam("message")
  res.sendHtml(HTML, embed={"message":message})
  return

# Main
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
```

## sample 2 Cheetah template
```
#!C:/Python3/python.exe
import CGI365Lib as CGI

# GET method
def on_GET(req, res):
  res.sendCheetah("./templates/test_cheetah.cheetah", embed={"title":"Cheetah test", "data":["One", "Two", "Three"]})
  return


# Start
if __name__ == '__main__':
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
```

## sample 3 
```
#!C:/Python3/python.exe
import os
import CGI365Lib as CGI

if CGI.isWindows():
  SAVEDIR = "D:/temp"
else:
  SAVEDIR = "/var/www/data"

# POST method
def on_POST(req, res):
  filename = req.getParam("filename-file1")
  chunk = req.getParam("chunk-file1")
  path = f"{SAVEDIR}/{filename}"
  try:
    with open(path, mode="wb") as f:
      f.write(chunk)
    res.sendHtml("./templates/file_upload.html", embed={"message":f"'{filename}' was saved to '{SAVEDIR}'"})
  except Exception as e:
    res.sendHtml("./templates/file_upload.html", embed={"message":str(e)})

# GET method
def on_GET(req, res):
  res.sendHtml("./templates/file_upload.html", embed={"message":""})
  return

# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())

  if req.method == "POST":
    on_POST(req, res)
  elif req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
```

## sample 4 post_form.cgi
```
#!C:/Python3/python.exe
import CGI365Lib as CGI

# POST mthod
def on_POST(req, res):
  text1 = req.getParam("text1")
  check1 = req.getParam("check1")
  radiogroup1 = req.getParam("radiogroup1")
  select1 = req.getParam("select1")
  message = f"text1='{text1}'; "
  message += f"check1 ='{check1}'; "
  message += f"radiogroup1 ='{radiogroup1}'; "
  message += f"select1 ='{select1}';"
  res.sendHtml("./templates/post_form.html", embed={"result":message})

# GET mthod
def on_GET(req, res):
  res.sendHtml("./templates/post_form.html", embed={"result":""})
  return

# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())

  if req.method == "POST":
    on_POST(req, res)
  elif req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
```

## sample 5 fetch_formdata.cgi
```
#!C:/Python3/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def on_POST(req, res):
  CGI.log("on_POST")
  headers = ""
  for k, v in req.headers.items():
    headers += k + ": " + v + "\n"
  CGI.log(headers)
  data = req.body.decode().replace("\r", "")
  CGI.log(data)
  res.sendString(headers + "\n" + data)
  return

# GET method
def on_GET(req, res):
  res.sendHtml("./html/fetch_formdata.html")
  return

# Start
req, res = (CGI.Request(True), CGI.Response())

if req.method == "GET":
  on_GET(req, res)
elif req.method == "POST":
  on_POST(req, res)
else:
  CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
```

## sample 6 get_video.cgi
```
#!C:/Python3/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

path = req.getParam("path")
res.sendVideo(path)
```

## sample 7 get_image.cgi
```
#!C:/Python3/python.exe
import CGI365Lib as CGI

# get_image.cgi
req, res = (CGI.Request(), CGI.Response())

path = req.getParam("path")
res.sendImage(path)
```

## sample 8 get_pictures.cgi
```
#!C:/Python3/python.exe
import CGI365Lib as CGI
import MariaDB as maria

req, res = (CGI.Request(), CGI.Response())

criteria = req.getParam("criteria")

sql = "SELECT id, album, title, creator, path, media, mark, info, fav, date FROM Pictures"
if len(criteria) > 0:
  sql += f" WHERE {criteria}"
db = maria.MariaDB()
resultset = db.query(sql)

table = "<table class=\"table\">\n"
table += "<tr><th>id</th><th>album</th><th>title</th><th>creator</th><th>path</th><th>media</th><th>mark</th><th>info</th><th>fav</th><th>date</th></tr>\n"
for row in resultset:
  table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td><td>{row[9]}</td></tr>\n"
table += "</table>\n" 
res.sendString(table)
```

# for_cgi
* Python3 very simple and light weight CGI Library.
* For small CGI program.
* Not support multipart/form-data.

## sample 1 hello.cgi
```
#!C:/Python3/python.exe

print('Content-Type: text/html; encoding=utf-8\n')

HTML = '''<!DOCTYPE html>
<html>
  <head>
<!--
   <meta charset='utf-8' />
-->
   <title>hello</title>
   <style>
    h1 {
      text-align:center;
      margin:20px;
      color:crimson;
    }
    h2 {
     text-align:center;
    } 
   </style>
 </head>
 <bodu>
  <h1>Hello, World!</h1>
  <h2>こんにちわ</h2>
  <p style="text-align:center;margin-top:40px;"><a href="index.cgi">Index</a></p>
 </body>
</html>
'''

print(HTML)
```

## sample 2 get_form.cgi
```
#!C:/Python3/python.exe
# get_form.cgi
import for_cgi as cgi, os

HTML_BODY = '''<h1>get_form.cgi</h1>
<hr>
<p style="padding:10px;"><a href="/cgi-bin/for_cgi/index.cgi">index.cgi へもどる</a></p>
<form styl="margin-left:10%; margin-top:20px;" method="GET">
 <fieldset style="margin-top:20px; padding:8px;">
  <legend>名前と年齢を入力</legend>
  <div style="margin-top:10px">
    <label>名前 <input type="text" name="name" id="name" value="{0}" /></label>
  </div>
  <div style="margin-top:10px; margin-bottom:20px;">
    <label>年齢 <input type="number" name="age" id="age" value="{1}" /></label>
  </div>
 </fieldset>
 <div style="margin-top:20px;"><button type="submit">送信する</button></div>
</form>
<p id="message" class="message">{2}</p>
'''

# QUERY_STRING があるか？
if cgi.qs_exists():
  # パラメータを取得してメッセージを埋め込む。
  params = cgi.get_params()
  name = params['name']
  age = params['age']
  message = f'{name}さんは{age}歳です。'
  body = HTML_BODY.format(name, age, message) 
else:
  # フォームのみを表示。
  body = HTML_BODY.format('', '', '')
# レスポンスを返す。
cgi.send_html(cgi.HTML_HEAD.format('get_form') + body + cgi.HTML_TAIL)
```

## sample 3 post_form.cgi
```
#!C:/Python3/python.exe
# post_form.cgi
import for_cgi as cgi, os

HTML_BODY = '''<h1>post_form.cgi</h1>
<hr>
<p style="padding:10px;"><a href="/cgi-bin/for_cgi/index.cgi">index.cgi へもどる</a></p>
<form styl="margin-left:10%; margin-top:20px;" method="POST">
 <fieldset style="margin-top:20px; padding:8px;">
  <legend>名前と年齢を入力</legend>
  <div style="margin-top:10px">
    <label>名前 <input type="text" name="name" id="name" value="{0}" /></label>
  </div>
  <div style="margin-top:10px; margin-bottom:20px;">
    <label>年齢 <input type="number" name="age" id="age" value="{1}" /></label>
  </div>
 </fieldset>
 <div style="margin-top:20px;">
  <button type="submit">送信する</button>
 </div>
</form>
<p id="message" class="message">{2}</p>
'''

# メソッドは POST か？
if cgi.get_method() == 'POST':
  # パラメータを取得してメッセージを埋め込む。
  params = cgi.get_body()
  name = params['name']
  age = params['age']
  message = f'{name}さんは{age}歳です。'
  body = HTML_BODY.format(name, age, message) 
else:
  # フォームのみを表示。
  body = HTML_BODY.format('', '', '')
# レスポンスを返す。
cgi.send_html(cgi.HTML_HEAD.format('post_form') + body + cgi.HTML_TAIL)
```
