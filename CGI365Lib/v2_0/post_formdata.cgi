#!D:/python312/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def onPOST(req, res):
  req.parseFormBody()
  db = req.getParam("db")
  name = req.getParam("table")
  desc = SQLite3.getValue(db, f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{name}'")
  res.sendJSON({"message":"OK", "result":desc})
  return

# GET method
def onGET(req, res):
  htmlfile = "./html/post_formdata.html"
  res.sendHtml(htmlfile)
  return

# Start
req, res = (CGI.Request(), CGI.Response())

if req.Method == "POST":
  onPOST(req, res)
else:
  onGET(req, res)
