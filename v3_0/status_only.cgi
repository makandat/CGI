#!C:/Python3/python.exe
import CGI365Lib as CGI

req, res = (CGI.Request(), CGI.Response())

status = req.getParam("status")
if status == "":
  status = "400"  # Bad Request
message = "OK from status_only.cgi"
if CGI.BAD_REQUEST.startswith(status):
  message = CGI.BAD_REQUEST
elif CGI.FORBIDDEN.startswith(status):
  message = CGI.FORBIDDEN
elif CGI.METHOD_NOT_ALLOWED.startswith(status):
  message = CGI.METHOD_NOT_ALLOWED
elif CGI.INTERNAL_SERVER_ERROR.startswith(status):
  message = CGI.INTERNAL_SERVER_ERROR
elif CGI.NOT_IMPLEMENTED.startswith(status):
  message = CGI.NOT_IMPLEMENTED
else:
  pass

CGI.Response.status(status, message)