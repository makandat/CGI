#!D:/python312/python.exe
import os
import CGI365Lib as CGI

if os.name == "nt":
  SAVEDIR = "D:/temp"
else:
  SAVEDIR = "/var/www/data"


# POST mthod
def on_POST(req, res):
  filenames = ""
  for fp in req.files:
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
def on_GET(req, res):
  res.sendHtml("./templates/multi_files_upload.html", embed={"message":""})
  return

# Start
if __name__ == '__main__':
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  elif req.method == "POST":
    on_POST(req, res)
  else:
    CGI.status(405, CGI.Response.METHOD_NOT_ALLOWED)

