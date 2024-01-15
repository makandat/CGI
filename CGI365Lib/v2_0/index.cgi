#!D:/python312/python.exe
# index.cgi
import CGI365Lib as CGI

# GET method
def on_GET(req, res):
  res.sendHtml("./html/index.html")

# Main
if __name__ == '__main__':
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
