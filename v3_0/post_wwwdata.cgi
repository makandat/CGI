#!C:/Python3/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def on_POST(req, res):
  db = req.getParam("db")
  CGI.info(db)
  command = req.getParam("command")
  CGI.info(command)
  if db == "" or command == "":
    res.sendSimple(CGI.BAD_REQUEST)
    return
  try:
    SQLite3.execute(db, command)
  except Exception as e:
    res.sendSimple(str(e))
    return
  res.sendSimple("OK")
  return

# GET method
def on_GET(req, res):
  htmlfile = "./html/post_wwwdata.html"
  res.sendHtml(htmlfile)
  return

# Start
req, res = (CGI.Request(True), CGI.Response())

if req.method == "GET":
  on_GET(req, res)
elif req.method == "POST":
  on_POST(req, res)
else:
  CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
