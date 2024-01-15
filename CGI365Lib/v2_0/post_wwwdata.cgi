#!D:/python312/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def onPOST(req, res):
  # req.parseFormBody()
  db = req.getParam("db")
  command = req.getParam("command")
  if db == "" or command == "":
    res.sendSimple(CGI.BAD_REQUEST)
    return
  try:
    SQLite3.execute(db, command)
  except:
    res.sendSimple(CGI.INTERNAL_SERVER_ERROR)
    return
  res.sendSimple("OK")
  return

# GET method
def onGET(req, res):
  htmlfile = "./html/post_wwwdata.html"
  res.sendHtml(htmlfile)
  return

# Start
req, res = (CGI.Request(True), CGI.Response())

if req.Method == "POST":
  onPOST(req, res)
else:
  onGET(req, res)
