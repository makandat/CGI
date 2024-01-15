#!D:/python312/python.exe
import os.path
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

filename = req.getParam("file")
if filename == "":
  res.status(400, "400 BAD REQUEST: No file parameter!")
  exit(1)
path = f"./html/{filename}"
if not os.path.exists(path):
  res.status(400, f"400 BAD REQUEST: '{path}' does not exists.")
  exit(1)

res.sendHtml(path)
