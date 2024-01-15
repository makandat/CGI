#!D:/python312/python.exe
import os
import CGI365Lib as CGI

if os.name == "nt":
  LOG = "D:/temp/CGI365Lib.log"
  SAVEDIR = "D:/temp"
else:
  LOG = "/var/www/data/CGI365Lib.log"
  SAVEDIR = "/var/www/data"
LOG = "" # Disable to output log.

# POST mthod
def onPost(req, res):
  req.parseFormBody()
  filename = req.getParam("filename-file1")
  chunk = req.getParam("chunk-file1")
  path = f"{SAVEDIR}/{filename}"
  with open(path, mode="wb") as f:
    f.write(chunk)
  res.sendHtml("./templates/file_upload.html", embed={"message":f"'{filename}' was saved to '{SAVEDIR}'"})

# GET mthod
def onGet(req, res):
  res.sendHtml("./templates/file_upload.html", embed={"message":""})
  return

# Start
req, res = (CGI.Request(), CGI.Response())

if req.Method == "POST":
  try:
    onPost(req, res)
  except Exception as e:
    CGI.info(e)
else:
  onGet(req, res)

