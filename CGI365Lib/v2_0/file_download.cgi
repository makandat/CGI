#!D:/python312/python.exe
# file_download.cgi
import CGI365Lib as CGI
import os

HTML = "./templates/file_download.html"

# GET method
def on_GET(req, res):
  res.sendHtml(HTML)
  return
  
# POST method
def on_POST(req, res):
  path = req.getParam("path")
  if path == "":
    CGI.Response.status(400, CGI.BAD_REQUEST)
  else:
    name = os.path.basename(path)
    res.sendFile(path, filename=name)
  return

# Main
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  
  if req.method == "GET":
    on_GET(req, res)
  elif req.method == "POST":
    on_POST(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
