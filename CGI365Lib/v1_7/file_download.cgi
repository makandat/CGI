#!D:/python312/python.exe
import CGI365Lib as CGI
import os, mimetypes

req, res = (CGI.Request(), CGI.Response())

# GET
def onGET(req, res):
  res.sendHtml("./templates/file_download.html")
  return

# POST
def onPOST(req, res):
  req.parseFormBody()
  path = req.getParam("path")
  if path == "":
    res.sendHtml("./templates/file_download.html")
  else:
    extpair = os.path.splitext(path)
    filename = os.path.basename(path)
    ext = ""
    if len(extpair) >= 2:
      ext = extpair[1]
      mimetypes.init()
      mimetypes.knownfiles
      if ext in mimetypes.types_map:
        mime = mimetypes.types_map[ext]
        res.sendFile(path, mime, filename)
      else:
        res.status(501, CGI.NOT_IMPLEMENTED)
    else:
      res.status(500, CGI.INTERNAL_SERVER_ERROR)
  return

# Start
if req.Method == "GET":
  onGET(req, res)
else:
  onPOST(req, res)
