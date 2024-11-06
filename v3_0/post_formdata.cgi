#!C:/Python3/python.exe
import CGI365Lib as CGI
import SQLite3

# POST method
def on_POST(req, res):
  db = req.getParam("db")
  name = req.getParam("table")
  desc = SQLite3.getValue(db, f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{name}'")
  res.sendJSON({"message":"OK", "result":desc})
  return

# GET method
def on_GET(req, res):
  htmlfile = "./html/post_formdata.html"
  res.sendHtml(htmlfile)
  return

# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  elif req.method == "POST":
    on_POST(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
