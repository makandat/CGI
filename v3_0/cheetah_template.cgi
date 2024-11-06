#!C:/Python3/python.exe
import CGI365Lib as CGI

# GET method
def on_GET(req, res):
  res.sendCheetah("./templates/test_cheetah.cheetah", embed={"title":"Cheetah test", "data":["One", "Two", "Three"]})
  return


# Start
if __name__ == '__main__':
  req, res = (CGI.Request(), CGI.Response())
  if req.method == "GET":
    on_GET(req, res)
  else:
    CGI.Response.status(405, CGI.METHOD_NOT_ALLOWED)
