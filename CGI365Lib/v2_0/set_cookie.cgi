#!D:/python312/python.exe
import CGI365Lib as CGI

HTML = "./templates/set_cookie.html"

# Get req.cookies and to HTML string
def getRequestCookies(req) -> str:
  n = len(req.cookies)
  if n == 0:
    return ""
  s = ""
  for k, v in req.cookies.items():
    s += CGI.tag("li", f"{k}={v}")
  return s

# GET method handler
def on_GET(req, res):
  CGI.info("onGET")
  cookies = getRequestCookies(req)
  res.sendHtml(HTML, embed={"cookies":cookies, "message":""})
  return

# POST method handler
def on_POST(req, res):
  cookies = getRequestCookies(req)
  s = req.getParam("cookie")
  kv = s.split("=", 1)
  if len(kv) == 2:
    name = kv[0]
    value = kv[1]
    cookies += CGI.tag("li", f"{name}={value}")
    cookies = CGI.tag("ul", cookies)
    hc = dict()
    hc[name] = value
    res.setCookie(hc)
    message = f"Add or updated a cookie {name}='{value}'"
  else:
    message = "Error: The cookie format is bad."
  res.sendHtml(HTML, embed={"cookies":cookies, "message":message})
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
