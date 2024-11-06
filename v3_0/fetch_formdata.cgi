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
