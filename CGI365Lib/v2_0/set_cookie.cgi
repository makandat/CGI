#!D:/python312/python.exe
import CGI365Lib as CGI

HTML = "./templates/set_cookie.html"

# Get req.cookies
def getRequestCookies(req):
  n = len(req.cookies.items())
  if n == 0:
    return ""
  for k, v in req.cookies.items():
    s += CGI.tag("li", f"{k}={v}")
  return s

# GET method handler
def onGet(req, res):
  cookies = getRequestCookies(req)
  res.sendHtml(HTML, embed={"cookies":cookies, "message":""})
  return

# POST method handler
def onPost(req, res):
  cookies = getRequestCookies(req)
  s = req.getParam("cookie")
  kv = s.split("=", 1)
  name = kv[0]
  value = kv[1]
  cookies += CGI.tag("li", f"{name}={value}")
  cookies = CGI.tag("ul", cookies)
  hc = dict()
  hc[name] = value
  res.setCookie(hc)
  message = f"Add or updated a cookie {name}='{value}'"
  res.sendHtml(HTML, embed={"cookies":cookies, "message":message})
  return


# Start
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())

  if req.method == "POST":
    onPost(req, res)
  else:
    onGet(req, res)
