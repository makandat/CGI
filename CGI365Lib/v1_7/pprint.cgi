#!D:/python312/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

def onGET(req, res):
  obj = req.getParam("object")

  if obj == "":
    res.sendHtml("./templates/pprint.html")
  elif obj == "Request.Method":
    res.sendPPrint(req.Method)
  elif obj == "Request.QueryString":
    res.sendPPrint(req.QueryString)
  elif obj == "Request.Body":
    res.sendPPrint(req.Body)
  elif obj == "Request.Cookies":
    res.sendPPrint(req.Cookies)
  elif obj == "Request.Query":
    res.sendPPrint(req.Query)
  elif obj == "Request.Headers":
    res.sendPPrint(req.Headers)
  elif obj == "Request.Form":
    res.sendPPrint(req.Form)
  else:
    res.status(400, CGI.BAD_REQUEST)

onGET(req, res)
