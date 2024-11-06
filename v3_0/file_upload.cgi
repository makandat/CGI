#!C:/Python3/python.exe
import os
import CGI365Lib as CGI

if CGI.isWindows():
  SAVEDIR = "D:/temp"
else:
  SAVEDIR = "/var/www/data"

# POST method
def on_POST(req, res):
  filename = req.getParam("filename-file1")
  chunk = req.getParam("chunk-file1")
  path = f"{SAVEDIR}/{filename}"
  try:
    with open(path, mode="wb") as f:
      f.write(chunk)
    res.sendHtml("./templates/file_upload.html", embed={"message":f"'{filename}' was saved to '{SAVEDIR}'"})
  except Exception as e:
    res.sendHtml("./templates/file_upload.html", embed={"message":str(e)})

# GET method
def on_GET(req, res):
  res.sendHtml("./templates/file_upload.html", embed={"message":""})
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

