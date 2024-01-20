#!D:/python312/python.exe
import CGI365Lib as CGI

HTML = "./templates/echo.html"

# GET method
def on_GET(req, res):
  message = req.getParam("message")
  res.sendHtml(HTML, embed={"message":message})
  return

# Main
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)