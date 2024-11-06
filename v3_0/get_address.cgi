#!C:/Python3/python.exe
import CGI365Lib as CGI

# Start (GET method)
req, res = (CGI.Request(), CGI.Response())

address_list = list()
for key, val in req.Address.items():
  address_list.append(f"{key}: {val}")
address = CGI.Utility.htmlList(address_list, ul="ms-5", li="fs-5")

res.sendHtml("./templates/get_address.html", embed={"address":address})
