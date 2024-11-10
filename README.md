# https://github.com/makandat/CGI
#   CGI libraries

# CGI365Lib
* Python3 CGI Library
* For middle size CGI program.
* Support multipart/form-data.
* Support Cheetah template from v3.0.

## Request class
Processes requests sent from the client and processes them so that they can be easily handled by CGI. <br>
The following requests can be handled.

* Only "GET" and "POST" request methods are supported.
* Request parameters support JSON, FormData, and BLOB in addition to the usual formats.
Cookies are supported.
* Request class fields

### Fields
The Request class has the following fields. <br>
Users should not use these fields directly, but should use the corresponding properties. For example, use the self.method property instead of self.__Method. However, self.__Dispositions is only used internally, so no property is provided for it.

* self.__Body = self._getBody() # Raw data received by POST (bytes)
* self.__QueryString = self._getQueryString() # Environment variable received by GET QUERY_STRING (string)
* self.__Method = self._getMethod() # HTTP method 'GET', 'POST'... (str)
* self.__Headers = self._getHeaders() # Request header dictionary (dict[str, str])
* self.__Dispositions = self._getDispositions() # List of multipart form blocks (list[bytes])
* self.__Query = dict() # Parameters for GET method dict[str, str]
* self.__Form = dict() # Parameters for POST or GET method dict[str, str]
* self.__Files = list() # File information if file is included in multipart data (list[(name, filename, chunk)]
* self.__Cookies = self._getCookies() # Cookie dictionary (dict[str, str])

### Using forms
Using forms

If the form's method attribute is "GET" or "POST", it is the same as "Using the HTTP GET method". <br>

* For JSON: self.parseJSON()
* For BLOB and ArrayBuffer: self.getRawData()

### Using multipart forms
A multipart form is a form with enctype="multipart/form-data" and is used when uploading files.<br>
The data format sent in such a form is completely different from that of a normal form, but the data format is identified and processed in the self.parseFormData() method.<br>
However, for controls other than the input[type="file"] control, parameters can be obtained using self.getParam(name). For the input[type="file"] control, the name attribute can be obtained using self.getParam(name), but the file name and file contents can be obtained as follows.

* File name: "filename-name"
* File contents: "chunk-name"

For example, if the name attribute of the input[type="file"] control is "file1", the value can be obtained as follows.

* File name: self.getParam("filename-file1")
* File contents: self.getParam("chunk-file1")

### Using JSON parameters
When using the Fetch API on the client, you can send JSON as a parameter to the server. <br>
In this case, the data format is different from the form, so use the self.parseJSON() method instead of the self.parseFormBody() method.<br>
The self.parseJSON() method parses the sent data as JSON, converts it to a dictionary, and returns it as a function value.

### Using the FormData parameter
The FormData object wraps a form and is used when submitting a form with JavaScript (Fetch API).

### Using BLOB parameters

BLOBs are file-content-like objects, supported by the JavaScript Blob object. <br>
BLOBs are raw data, so no parsing is required. To get a BLOB, use the self.getRawData() method.

### Using Cookies

Cookies are stored in a member variable called self.Cookie, which is a dictionary keyed by cookie name.

### File saving methods

These methods are provided to save the contents of an uploaded file on the server side. 
These methods use the data (self.RawData) sent by the POST method, 
so they should be used after the self.getRawData() methods.

* saveRawData(self, savePath): Saves the contents of self.RawData as a binary file in the file specified by savePath. Use this when creating a debug file, etc.
* saveAsRawString(self, path): Saves the contents of self.RawData as a byte string in the file specified by savePath.
* saveAsBLOB(self, path): Saves the contents of self.RawData as a BLOB in the file specified by savePath.
* saveFile(self, name, savedir, binary=False): Almost the same as saveRawData(self, savePath), but allows you to specify whether to save as a string. Used to save the uploaded file on the server side.







## Response class

### Overview of the Response class

The Response class is a collection of methods for returning responses to the client via HTTP, and has the following methods:

* Output strings
* Output files
* Output cookies
* Output headers

### Response class fields

The Response class has the following fields.

* self.Cookie = list(): A list of cookies, containing strings in the "key=value" format.
* self.Headers = list(): A list of header strings that can be output as is.

### Outputting a string

The following methods output a string. self.sendString(s:str, mime="", cookie=True, headers=True, embed=None) not only outputs a string, but also outputs headers including cookies. You can also specify the MIME type (character code can be set). Furthermore, if the string contains a pattern "{{ key }}", the pattern is replaced with the value of key contained in the dictionary called embed.

* self.sendSimple(s:str, charset=""): Outputs the string s. If charset="", the character code depends on the environment.
* self.sendString(s:str, mime="", cookie=True, headers=True, embed=None): Outputs cookies and other headers before outputting the string. If mime is not a null string, it is added to "Content-Type: " and output. embed is a dictionary, and if s contains the string "{{ key }}", it is replaced with the value corresponding to key.
* self.sendJSON(data, charset=""): Converts dictionary data to a JSON string and outputs it. If charset="", the character code will depend on the environment.
* self.self.sendPPrint(obj, charset=""): Outputs object obj as an easy-to-read string. Mainly used for debugging.

### Outputting a file

The methods for outputting a file are as follows.

* self.sendHtml(path, charset="", cookie=True, embed=None) not only outputs HTML, but also outputs cookies at the same time. Furthermore, if there is a pattern "{{ key }}" in the HTML file, if a dictionary is set in embed, the pattern will be replaced with the value for the key in the dictionary.
* self.sendFile(path, mime, filename) is mainly used for downloading files. path is the path of the file to be downloaded, while filename is the name of the file to be attached and is displayed in the file save dialog.
* self.sendText(self, path, charset=""): Outputs the text file specified by path.
* self.sendHtml(path, charset="", cookie=True, embed=None): Outputs the HTML file specified by path. If cookie=True, the cookie will also be output. If embed=None is not set, it will be treated as a dictionary, and if the string "{{ key }}" is found, it will be replaced with the value corresponding to the key.
* self.sendImage(path): Outputs the image file specified by path. Image files include SVG.
* self,sendVideo(path): Outputs the video file specified by path.
* self.sendFile(path, mime, filename="")

### Outputting cookies

Cookies are sent together with HTML when it is sent. In other words, this is the case when cookie=True is specified in the sendString(s:str, mime="", cookie=True, headers=True, embed=None) method, or when cookie=True is specified in self.sendHtml(path, charset="", cookie=True, embed=None).
To output cookies, the contents of the cookies must be set in a list called self.Cookie with key:value pairs. This is done with the method called self.setCookie(cookie). The parameter cookie of this method is a dictionary whose key is the cookie name and whose value is the cookie string.
The self.makeCookie() method is mainly used internally, and when outputting HTML, it converts the contents of self.Cookie into a Set-Cookie statement and adds it to the header.

### Outputting headers

If you add complete headers to the list member variable self.Headers, when you execute the self.sendString() method, the headers will be sent before the string itself is output.

The self.header(headers) method outputs headers directly. <br>
The parameter headers is a list of complete headers. <br>
In addition, a special method self.redirect(url) is provided for redirection, which redirects to the URL specified by the parameter url.







## Utility class

The Utility class contains the following methods. These are all static methods, so there is no need to instantiate the Utility class.

* htmlTable(data, header, table="", tr="", th="", td=""): Creates an HTML table and returns it as the function value. data is the row data of the table, header is the first row data of the table, and the others are the class specifications of each element.
* htmlList(data, list="ul", ul="", li=""): Creates an HTML list and returns it as the function value. data is the list data, list is the list type, and the others are the class specifications of the elements.
* svg(shape, size=32, borderWidth=1, borderColor="black", bgColor="white): Creates an SVG (but only circles and squares) and returns it as a string. Only "circle" and "square" are valid shapes.
* startProcess(cmd, *arg): Starts a child process. cmd is the command, and *arg is a variable-length parameter list for the command.

## Debugging

If you start CGI with the parameter "debug", it will run as a console application. In that case, a prompt will be displayed and you can enter the value to be set in the QUERY_STRING environment variable for the GET method. For the POST method, you can also enter parameters from the keyboard.

If you specify a file path name instead of "debug", the data read from that file will be used as the POSTed parameters.

You can create such file contents manually, but if the contents are long, it is a good idea to create a simple CGI that simply saves self.RawData to create the file.


## Logging

If you set the constant CGI365Lib.LOG to a valid file path, you can output a string to that file using the CGI365Lib.info(message) function. CGI365Lib.LOG is set to "" by default, in which case CGI365Lib.info(message) does not work.

### Constants

The following constants are defined in the CGI365Lib module.

* ENC = "utf-8" : Output encoding for Windows
* LOG : Log output destination (D:\temp\CGI365Lib.log for Windows, /var/www/data/CGI365Lib.log for non-Windows). Setting this to "" will disable log output.
* OK = "200 OK" 
* BAD_REQUEST = "400 Bad Request"
* FORBIDDEN = "403 Forbidden"
* NOT_FOUND = "404 Not Found"
* METHOD_NOT_ALLOWED = "405 Method Not Allowed"
* INTERNAL_SERVER_ERROR = "500 Internal Server Error"
* NOT_IMPLEMENTED = "501 Not Implemented"

## Templates

### Simple HTML template
HTML file which have "{{variable}}" marker string.<br>
This marker replaced by Response.sendString() or Response.sendHtml()'s embed paramater.<br>
This embed parameter is dict and the key is "variable" and value is the value to be replaced.

```
<!DOCTYPE html>
<html>
<head>
 <title>{{title}}</title>
</head>
 ....
</html>
```

### Cheetah template (from v3.0)

[Cheetah](https://pypi.org/project/CT3/) is a light weight template language for Python.
This template is available from version 3.0.



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

## sample 3 file_upload.cgi
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
