#!D:/python312/python.exe
# pprint.cgi
import CGI365Lib as CGI

HTML = "./templates/pprint.html"

# GET method
def on_GET(req, res):
  if req.isPostback():
    obj = req.getParam("object")
    if obj == "Request.Method":
      res.sendSimple(req.method)
    elif obj == "Request.QueryString":
      res.sendSimple(req.queryString)
    elif obj == "Request.Body":
      res.sendSimple("(Empty)")
    elif obj == "Request.Headers":
      headers = ""
      for k, v in req.headers.items():
        headers += f"{k}: {v}\n"
      res.sendSimple(headers)
    elif obj == "Request.Cookies":
      cookies = ""
      for k, v in req.cookies.items():
        cookies += f"{k}: {v}\n"
      res.sendSimple(cookies)
    elif obj == "Request.Query":
      query = ""
      for k, v in req.query.items():
        query += f"{k}: {v}\n"
      res.sendSimple(query)
    elif obj == "Request.Form":
      form = ""
      for k, v in req.form.items():
        form += f"{k}: {v}\n"
      res.sendSimple(form)
    else:
      CGI.Response.status(400, BAD_REQUEST)
  else:
    res.sendHtml(HTML)

# Main
if __name__ == "__main__":
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
