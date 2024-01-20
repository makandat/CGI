#!D:/python312/python.exe
import os
import CGI365Lib as CGI

if CGI.isWindows():
  SAVEPATH = "D:/temp/save_rawdata.bin"
else:
  SAVEPATH = "/var/www/data/save_rawdata.bin"

# GET method handler
def on_GET(req, res):
  res.sendHtml("./templates/save_rawdata.html", embed={"headers":"", "data":"", "message":""})
  return

# POST method handler
def on_POST(req, res):
  headers = ""
  for k, v in req.headers.items():
    headers += k + ": " + v + "\n"
  with open(SAVEPATH, "wb") as f:
    f.write(req.body)
  n = len(req.body)
  body = req.body.decode().replace("\r", "")
  message = f"Request.Body length = {n}. Saved as '{SAVEPATH}'"
  res.sendHtml("./templates/save_rawdata.html", embed={"headers":headers, "data":body, "message":message})
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
