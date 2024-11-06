#!C:/Python3/python.exe
import CGI365Lib as CGI

# POST mthod
def on_POST(req, res):
  text1 = req.getParam("text1")
  check1 = req.getParam("check1")
  radiogroup1 = req.getParam("radiogroup1")
  select1 = req.getParam("select1")
  message = f"text1='{text1}'; "
  message += f"check1 ='{check1}'; "
  message += f"radiogroup1 ='{radiogroup1}'; "
  message += f"select1 ='{select1}';"
  res.sendHtml("./templates/post_form.html", embed={"result":message})

# GET mthod
def on_GET(req, res):
  res.sendHtml("./templates/post_form.html", embed={"result":""})
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
