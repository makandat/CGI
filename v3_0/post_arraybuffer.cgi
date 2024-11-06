#!C:/Python3/python.exe
import CGI365Lib as CGI

# POST method
def on_POST(req, res):
  bindata = req.body
  s = ""
  for b in bindata:
    s += "{:02x}".format(b)
    s += " "
  result = {"message":"OK", "data":s[0:len(s)-1]}
  res.sendJSON(result)
  return

# GET method
def on_GET(req, res):
  htmlfile = "./html/post_arraybuffer.html"
  res.sendHtml(htmlfile)
  return


# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  elif req.method == "POST":
    on_POST(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
