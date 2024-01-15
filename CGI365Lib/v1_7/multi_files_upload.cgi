#!D:/python312/python.exe
import os
import CGI365Lib as CGI

if os.name == "nt":
  LOG = "D:/temp/CGI365Lib.log"
  SAVEDIR = "D:/temp"
else:
  LOG = "/var/www/data/CGI365Lib.log"
  SAVEDIR = "/var/www/data"

#LOG = "" # Disable to output log.

# POST mthod
def onPOST(req, res):
  filenames = ""
  req.parseFormBody()
  for fp in req.Files:
    name, filename, chunk = fp
    filenames += f"{filename}, "
    if chunk is None:
      res.sendHtml("./templates/multi_files_upload.html", embed={"message":"Error: Bad name or filename."})
      return
    path = f"{SAVEDIR}/{filename}"
    with open(path, mode="wb") as f:
      f.write(chunk)
  res.sendHtml("./templates/multi_files_upload.html", embed={"message":f"'{filenames}' was saved to '{SAVEDIR}'"})
  return

# GET mthod
def onGET(req, res):
  res.sendHtml("./templates/multi_files_upload.html", embed={"message":""})
  return

# Start
if __name__ == '__main__':
  req, res = (CGI.Request(), CGI.Response())
  if req.Method == "GET":
    onGET(req, res)
  elif req.Method == "POST":
    onPOST(req, res)
  else:
    CGI.status(405, METHOD_NOT_ALLOWED)

