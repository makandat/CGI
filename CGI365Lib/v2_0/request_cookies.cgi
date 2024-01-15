#!D:/python312/python.exe
import CGI365Lib as CGI

HTML = "./templates/request_cookies.html"

# GET method
def on_GET(req, res):
  cookie_list = list()
  for k, v in req.cookies.items():
    cookie_list.append(f"{k}: {v}")
  html_list = ""
  if len(cookie_list) == 0:
    html_list = "<p class=\"text-danger\">No cookies was found.</p>"
  else:
    html_list = CGI.Utility.htmlList(cookie_list)
  res.sendHtml(HTML, embed={"html_list":html_list, "title":"HTTP Request Cookies"})
  return

# Main
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, METHOD_NOT_ALLOWED)
