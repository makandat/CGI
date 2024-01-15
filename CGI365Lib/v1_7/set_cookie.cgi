#!D:/python312/python.exe
import CGI365Lib as CGI

# Get req.cookies
def getRequestCookies(req):
  cookies = req.Cookies
  s = "<ul>"
  for k, v in cookies.items():
    s += CGI.tag("li", f"{k}={v}")
  s += "</ul>\n"
  return s

# GET method handler
def onGet(req, res):
  cookies = getRequestCookies(req)
  res.sendHtml("./templates/set_cookie.html", embed={"cookies":cookies, "message":""})
  return

# POST method handler
def onPost(req, res):
  req.parseFormBody()
  cookies = getRequestCookies(req)
  s = req.getParam("cookie")
  kv = s.split("=", 1)
  name = kv[0]
  value = kv[1]
  cookies += CGI.tag("li", f"{name}={value}")
  hc = dict()
  hc[name] = value
  res.setCookie(hc)
  message = f"Add or updated a cookie {name}='{value}'"
  res.sendHtml("./templates/set_cookie.html", embed={"cookies":cookies, "message":message})
  return


# Start
req, res = (CGI.Request(), CGI.Response())

if req.Method == "POST":
  onPost(req, res)
else:
  onGet(req, res)
