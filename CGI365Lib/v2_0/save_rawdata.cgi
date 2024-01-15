#!D:/python312/python.exe
import os
import CGI365Lib as CGI

if os.name == "nt":
  SAVEPATH = "D:/temp/save_rawdata.bin"
else:
  SAVEPATH = "/var/www/data/save_rawdata.bin"

# GET method handler
def onGet(req, res):
  res.sendHtml("./templates/save_rawdata.html", embed={"headers":"", "data":"", "message":""})
  return

# POST method handler
def onPost(req, res):
  headers = ""
  for k, v in req.Headers.items():
    headers += k + ": " + v + "\n"
  body = req.Body.decode().replace("\r", "")
  req.saveRawData(SAVEPATH)
  n = len(req.Body)
  message = f"Request.Body length = {n}. Saved as '{SAVEPATH}'"
  res.sendHtml("./templates/save_rawdata.html", embed={"headers":headers, "data":body, "message":message})
  return

# Start
req, res = (CGI.Request(), CGI.Response())

if req.Method == "POST":
  onPost(req, res)
else:
  onGet(req, res)
