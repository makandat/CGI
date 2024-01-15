#!D:/python312/python.exe
import CGI365Lib as CGI

# POST method
def onPOST(req, res):
  bindata = req.getRawData()
  s = ""
  for b in bindata:
    s += "{:02x}".format(b)
    s += " "
  result = {"message":"OK", "data":s[0:len(s)-1]}
  res.sendJSON(result)
  return

# GET method
def onGET(req, res):
  htmlfile = "./html/post_arraybuffer.html"
  res.sendHtml(htmlfile)
  return


# Start
req, res = (CGI.Request(), CGI.Response())
if req.Method == "POST":
  onPOST(req, res)
else:
  onGET(req, res)
