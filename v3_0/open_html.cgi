#!C:/Python3/python.exe
import os.path
import CGI365Lib as CGI

# GET method
def on_GET(req, res):
  filename = req.getParam("file")
  if filename == "":
    CGI.Response.status(400, "400 BAD REQUEST: No file parameter!")
    return
  path = f"./html/{filename}"
  if not os.path.exists(path):
    CGI.Response.status(400, f"400 BAD REQUEST: '{path}' does not exists.")
    return
  res.sendHtml(path)

# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())

  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
